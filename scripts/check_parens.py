from pathlib import Path
p = Path('clips/knowledge_base.clp')
s = p.read_text()
stack = []
bad = None
for i, ch in enumerate(s):
    if ch == '(':
        stack.append(i+1)
    elif ch == ')':
        if not stack:
            bad = ('unmatched_right', i+1)
            break
        stack.pop()
if bad:
    print(bad)
elif stack:
    print('unmatched_left_positions_count', len(stack))
else:
    print('balanced')
