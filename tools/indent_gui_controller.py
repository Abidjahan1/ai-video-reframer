import io
path = r'O:\pythonproject\smart-video-reframer\gui\controller.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

in_class = False
for i, line in enumerate(lines):
    if 'class GUIController' in line:
        in_class = True
        continue
    if in_class:
        if line.startswith('def ') and not line.startswith('    '):
            lines[i] = '    ' + line

with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Indented GUIController methods to inside-class scope')
