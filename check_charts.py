import json
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()
    # Find chart canvas elements
    import re
    canvases = re.findall(r"id=["']([^"']*(Chart|chart)[^"']*)["']" , content)
    print("Found canvas elements:")
    for c in set(canvases):
        print(f"  - {c[0]}")
