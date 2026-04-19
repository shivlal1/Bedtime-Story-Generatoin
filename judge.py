import json
from llm import call_model


def judge(story):
    prompt = f"""You're a children's book editor. Score this bedtime story on each dimension 1-10.
Don't inflate scores -- a mediocre story is a 5 or 6.

Dimensions: age_appropriateness, story_arc_clarity, language_quality,
moral_integration, sleep_readiness, engagement, safety

Safety Instructions:
- no harmful, scary, violent, inappropriate, or disturbing content for children.
- Return zero for all dimensions if you even remotely feel that the story is not appropriate for children.

Return JSON only:
{{
  "scores": {{"age_appropriateness": int, "story_arc_clarity": int, "language_quality": int,
             "moral_integration": int, "sleep_readiness": int, "engagement": int,
             "safety": int}},
  "average": float,
  "weakest_dimension": str,
  "improvement_instructions": str
}}

Story:
{story}
"""
    raw = call_model(prompt, max_tokens=400, temperature=0.2)
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"scores": {}, "average": 0.0, "weakest_dimension": "unknown",
                "improvement_instructions": "Improve the story overall."}