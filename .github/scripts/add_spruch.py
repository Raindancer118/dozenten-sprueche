"""Hängt einen Spruch aus einem GitHub-Issue an README.md an.

Aufruf in der Action: ISSUE_BODY=... python add_spruch.py <datei>
Exit-Code 0 = hinzugefügt, 3 = Duplikat, 2 = kein Spruch gefunden.
"""
import html
import os
import re
import sys

FIELD_HEADING = "### Spruch"


def extract_spruch(body):
    if not body:
        return None
    body = body.replace("\r\n", "\n")
    if FIELD_HEADING in body:
        body = body.split(FIELD_HEADING, 1)[1]
        body = re.split(r"^### ", body, maxsplit=1, flags=re.MULTILINE)[0]
    value = body.strip()
    if not value or value == "_No response_":
        return None
    return value


def escape(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    escaped = html.escape("<br>".join(lines), quote=False)
    escaped = escaped.replace("&lt;br&gt;", "<br>")
    escaped = escaped.replace("{", "&#123;").replace("}", "&#125;")
    # Block-Syntax am Zeilenanfang (#, >, -, 1.) würde den Listenpunkt sprengen
    return re.sub(r"^([#>+\-*]|\d+\.)", lambda m: "".join(f"&#{ord(c)};" for c in m.group(1)), escaped)


def _normalise(text):
    return " ".join(text.split()).casefold()


def add_spruch(path, spruch):
    entry = escape(spruch)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    existing = {_normalise(line[2:]) for line in content.splitlines() if line.startswith("- ")}
    if _normalise(entry) in existing:
        return False
    if content and not content.endswith("\n"):
        content += "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{content}- {entry}\n")
    return True


def main():
    spruch = extract_spruch(os.environ.get("ISSUE_BODY"))
    if spruch is None:
        return 2
    return 0 if add_spruch(sys.argv[1], spruch) else 3


if __name__ == "__main__":
    sys.exit(main())
