# Fix indentation in preview.py
import re

path = r'O:\pythonproject\smart-video-reframer\gui\preview.py'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix the methods - they need 4 spaces of class indentation
lines = content.split('\n')
fixed = []

for i, line in enumerate(lines):
    # If line starts with def at wrong indentation level
    stripped = line.lstrip()
    leading = len(line) - len(stripped)
    
    if stripped.startswith('def pause') or stripped.startswith('def seek') or stripped.startswith('def step_forward') or stripped.startswith('def step_backward') or stripped.startswith('def close'):
        # Should be 4 spaces inside class
        if leading == 0:
            line = '    ' + stripped
    
    fixed.append(line)

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed))

print('Fixed')