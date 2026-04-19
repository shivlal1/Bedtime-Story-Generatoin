"""Before submitting the assignment, describe here in a few sentences
    what you would have built next if you spent 2 more hours on this project:

- I would have added a personalization layer that remembers the stories a child liked
  and uses them as examples for future story generation. This can be implemented by
  storing user feedback and past stories in a vector database (e.g., ChromaDB) using embeddings,
  and retrieving relevant preferences at generation time to augment the prompt.

- Since text-to-speech is already integrated,
  I would build a simple prototype application with a UI (using Gradio or a lightweight React frontend)
  to make the system interactive. This would include features like story playback controls,
  user feedback collection, and session-based state management to improve the overall user experience.
"""

from story import classify, write_story, refine, apply_changes
from judge import judge
from display import print_story, print_scores
from tts import speak_story

MAX_ROUNDS = 3
PASS_SCORE = 7.5

example_requests = "A story about a girl named Alice and her best friend Bob, who happens to be a cat."


def main():
    user_input = input("What kind of story do you want to hear? ")
    if not user_input.strip():
        user_input = example_requests

    print("\nClassifying...")
    classification = classify(user_input)
    print(f"  genre={classification['genre']}  tone={classification['tone']}")

    print("Writing story...")
    story = write_story(user_input, classification)

    for i in range(MAX_ROUNDS):
        print(f"\nJudging (round {i+1})...")
        result = judge(story)
        print_scores(result)

        avg = result.get("average", 0.0)
        if avg >= PASS_SCORE:
            print(f"  Passed ({avg:.1f} >= {PASS_SCORE})")
            break

        print(f"  Score {avg:.1f} below threshold, refining...")
        story = refine(story, result.get("improvement_instructions", ""))

    print_story(story)

    while True:
        changes = input("\nAny changes? (enter to quit) > ").strip()
        if not changes:
            if input("Read the story out loud? (y/n) > ").strip().lower() == "y":
                speak_story(story)
            print("Goodnight!")
            break
        story = apply_changes(story, changes)
        print_story(story)


if __name__ == "__main__":
    main()