import os
import json
import spacy
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# --- Load NLP Model ---
# This model understands skill similarities
nlp = spacy.load("en_core_web_md")

# --- Connect to MongoDB Atlas ---
# NOTE: Set your CONNECTION_STRING in Codespaces Secrets!
# In Codespaces terminal, run: gh secret set MONGODB_URI
# Then paste your connection string.
connection_string = os.environ.get("MONGODB_URI")
client = MongoClient(connection_string)
db = client.skillmatch_db # Use a database named skillmatch_db
users_collection = db.users # and a collection named users

# --- Helper Function for Skill Similarity ---
def get_skill_similarity(skill1, skill2):
    """Calculates similarity between two skills using spaCy."""
    # Process skills into nlp docs
    doc1 = nlp(skill1.lower())
    doc2 = nlp(skill2.lower())
    return doc1.similarity(doc2)

# --- The Upgraded Matching Function ---
def calculate_match_score(user_a, user_b):
    score = 0
    reasons = []

    # 1. Skill Match (Max 60 points) - Now with NLP!
    best_teach_swap_score = 0
    for a_skill in user_a['skills_to_teach']:
        for b_skill in user_b['skills_to_learn']:
            similarity = get_skill_similarity(a_skill, b_skill)
            if similarity > best_teach_swap_score:
                best_teach_swap_score = similarity

    best_learn_swap_score = 0
    for b_skill in user_b['skills_to_teach']:
        for a_skill in user_a['skills_to_learn']:
            similarity = get_skill_similarity(b_skill, a_skill)
            if similarity > best_learn_swap_score:
                best_learn_swap_score = similarity
    
    # Perfect match if both sides have a > 0.8 similarity
    if best_teach_swap_score > 0.8 and best_learn_swap_score > 0.8:
        score += 60
        reasons.append("Perfect skill swap: You have highly relevant skills to teach each other.")
    else:
        # Partial match score based on the best similarity found
        total_similarity_score = (best_teach_swap_score + best_learn_swap_score) / 2
        partial_score = int(total_similarity_score * 40) # Scale it to a max of 40 points
        if partial_score > 10:
            score += partial_score
            reasons.append(f"Good partial match with a skill relevance of {int(total_similarity_score * 100)}%.")

    # The other scores remain the same (Language, Timezone, Experience)
    if any(lang in user_b['languages'] for lang in user_a['languages']):
        score += 15
        reasons.append("You share a common language.")

    # You can add the Timezone and Experience logic here as before...

    # Convert user_b['_id'] to string for JSON serialization
    user_b['_id'] = str(user_b['_id'])
    
    return score, reasons

# --- API Endpoint to find matches ---
@app.route('/match', methods=['POST'])
def find_matches():
    current_user = request.json
    matches = []
    
    # Find all users in the database except the current one
    all_other_users = users_collection.find({"user_id": {"$ne": current_user['user_id']}})

    for other_user in all_other_users:
        score, reasons = calculate_match_score(current_user, other_user)
        if score > 30:
            matches.append({
                "matched_user_id": other_user['user_id'],
                "skills_they_teach": other_user['skills_to_teach'],
                "why_they_are_a_good_match": ". ".join(reasons),
                "match_score": min(score, 100) # Cap score at 100
            })
            
    sorted_matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
    return jsonify(sorted_matches)

# --- API Endpoint to add a new user ---
@app.route('/user', methods=['POST'])
def add_user():
    user_data = request.json
    result = users_collection.insert_one(user_data)
    return jsonify({"message": "User added successfully", "id": str(result.inserted_id)}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)