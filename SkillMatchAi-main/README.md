# SkillMatchAi



Workarounds

Use curl in CMD / terminal (works perfectly).

Use Postman / REST client browser extension.

Use a small HTML page with a button + JavaScript to send POST (works in any browser).




Command to Test Matching with a Dummy User

curl -X POST "https://skillmatchai-jw02.onrender.com/match" -H "Content-Type: application/json" -d "{\"user_id\":\"dummy123\",\"name\":\"Test User\",\"skills_to_teach\":[\"Python\",\"Java\"],\"skills_to_learn\":[\"React\",\"Spring Boot\"],\"languages\":[\"English\",\"Telugu\"]}"



output:-----


[
  {
    "match_score": 75,
    "matched_user_id": "u102",
    "skills_they_teach": ["React","JavaScript"],
    "why_they_are_a_good_match": "Perfect skill swap: You have highly relevant skills to teach each other.. You share a common language."
  },
  {
    "match_score": 75,
    "matched_user_id": "u102",
    "skills_they_teach": ["React","JavaScript"],
    "why_they_are_a_good_match": "Perfect skill swap: You have highly relevant skills to teach each other.. You share a common language."
  },
  {
    "match_score": 43,
    "matched_user_id": "user123",
    "skills_they_teach": ["Python","Java"],
    "why_they_are_a_good_match": "Good partial match with a skill relevance of 70%.. You share a common language."
  },
  {
    "match_score": 35,
    "matched_user_id": "u107",
    "skills_they_teach": ["Java","Spring Boot"],
    "why_they_are_a_good_match": "Good partial match with a skill relevance of 51%.. You share a common language."
  },
  {
    "match_score": 34,
    "matched_user_id": "u101",
    "skills_they_teach": ["Python","Data Analysis"],
    "why_they_are_a_good_match": "Good partial match with a skill relevance of 49%.. You share a common language."
  },
  {
    "match_score": 33,
    "matched_user_id": "u109",
    "skills_they_teach": ["SQL","PostgreSQL"],
    "why_they_are_a_good_match": "Good partial match with a skill relevance of 46%.. You share a common language."
  }
]
