import textwrap


def print_story(story):
    print("\n" + "=" * 60)
    for line in story.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("[TITLE]"):
            title = s.replace("[TITLE]", "").strip()
            print(f"\n  *** {title.upper()} ***\n")
        elif s.startswith("[") and s.endswith("]"):
            print(f"\n  [{s.strip('[]')}]\n")
        else:
            print(textwrap.fill(s, width=68, initial_indent="  ", subsequent_indent="  "))
    print("\n" + "=" * 60)


def print_scores(result):
    print("\n  Judge scores:")
    for dim, score in result.get("scores", {}).items():
        print(f"    {dim:<25} {'#' * score}{'.' * (10-score)}  {score}/10")
    print(f"    {'average':<25} {result.get('average', 0):.1f}/10")