from pathlib import Path
p = Path('clips/knowledge_base.clp')
for i, line in enumerate(p.read_text().splitlines(), start=1):
    if 100 <= i <= 130:
        print(f"{i:3}: {line!r}")
