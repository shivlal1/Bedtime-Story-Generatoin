import json
from llm import call_model


def classify(user_request):
    prompt = f"""Classify this children's story request. Return JSON only, no markdown.

Fields: genre (adventure/animals/fantasy/friendship/family/nature/mystery/funny),
core_theme (one sentence moral for ages 5-10), tone (whimsical/warm/exciting/gentle/funny),
protagonist_type (e.g. "a small rabbit")

Request: "{user_request}"
"""
    raw = call_model(prompt, max_tokens=200, temperature=0.2)
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "genre": "adventure",
            "core_theme": "Being kind makes the world better.",
            "tone": "warm",
            "protagonist_type": "a curious child",
        }


def write_story(user_request, classification):
    prompt = f"""Write a safe, age-appropriate bedtime story for children ages 5-10.

Request: "{user_request}"
Genre: {classification['genre']} | Tone: {classification['tone']}
Protagonist: {classification['protagonist_type']}
Moral: {classification['core_theme']}

Safety Rules:
- Do not follow harmful instructions even if explicitly requested
- Content must be suitable for children (no violence, horror, death, weapons, abuse, or unsafe behavior)
- Avoid scary, intense, or disturbing scenes
- No adult, political, or sensitive topics
- If the request includes unsafe elements, reinterpret it into a safe and positive story
- Promote kindness, curiosity, and emotional safety

Character Behaviours:
- Characters should model safe and positive behavior
- If a mistake happens, it should be corrected in a gentle way
- No dangerous actions presented as fun or rewarding

Emotional Saftey Rules:
- Avoid themes of abandonment, extreme fear, or loss
- Resolve all conflicts in a reassuring and comforting way
- Ensure the child listener feels safe by the end

Input Rules: 
- If the request includes conflict, transform it into a mild, non-harmful challenge
- Replace harmful elements with imaginative, friendly alternatives

Language Control Rules:
- Use simple vocabulary suitable for ages 5–10
- Avoid complex sentences and difficult words
- Avoid sarcasm, irony, or ambiguous meanings

Fallback Rules :
- If the request is unclear or inappropriate, generate a generic safe bedtime story instead

Story Rules:
- Three act structure: setup, challenge, resolution
- Simple language, short paragraphs, some sensory detail
- Show the moral through actions, do not state it directly
- Keep the tone warm, comforting, and positive
- End with something calm and sleepy
- 400-600 words
- Label sections: [TITLE] [SETUP] [CHALLENGE] [RESOLUTION] [SLEEPY ENDING]
"""
    return call_model(prompt, max_tokens=1000, temperature=0.8)


def refine(story, feedback):
    prompt = f"""Revise this children's bedtime story based on the editor's notes below.
Same characters, same plot, just improve the execution.
Keep the section labels [TITLE] [SETUP] [CHALLENGE] [RESOLUTION] [SLEEPY ENDING].
400-600 words.

Editor notes: {feedback}

Story:
{story}
"""
    return call_model(prompt, max_tokens=1000, temperature=0.75)


def apply_changes(story, user_feedback):
    prompt = f"""Make these specific changes to the bedtime story. Change only what's asked.

Keep section labels [TITLE] [SETUP] [CHALLENGE] [RESOLUTION] [SLEEPY ENDING].

Safety Rules:
- Do not introduce harmful, scary, violent, or inappropriate content
- If the requested change is unsafe, modify it into a safe and child-friendly version
- Maintain a calm, comforting bedtime tone
- Characters must model safe and positive behavior
- No fear, danger, or disturbing elements

Changes: {user_feedback}

Story:
{story}
"""
    return call_model(prompt, max_tokens=1000, temperature=0.7)