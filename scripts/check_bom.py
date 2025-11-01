from pathlib import Path
p=Path('clips/knowledge_base.clp')
b=p.read_bytes()
print('first bytes:', b[:4])
print('contains non-ascii?' , any(x>127 for x in b[:4]))
print('decoded (utf-8):')
print(b.decode('utf-8', errors='replace')[:200])
