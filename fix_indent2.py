content = open(r'O:\pythonproject\smart-video-reframer\gui\controller.py', 'r', encoding='utf-8').read()
lines = content.split('\n')

# Methods that are incorrectly indented at 4 spaces inside another method
# They should be at 0 (top-level in the class)
incorrect_methods = [
    '_on_step_forward',
    '_on_step_backward',
    '_on_next_video',
    '_on_previous_video',
    '_on_fullscreen',
    '_on_mute_toggle',
    '_on_key_press',
]

# Find the start and end of each method
in_method = False
method_start = -1
method_name = ''
method_lines = []

for i, line in enumerate(lines):
    stripped = line.lstrip()
    leading = len(line) - len(stripped)
    
    if stripped.startswith('def ') and any(m in stripped for m in incorrect_methods) and leading == 4:
        if in_method and method_start >= 0:
            # End of previous method - fix it
            for j in range(method_start, i):
                if lines[j].startswith('    '):
                    lines[j] = lines[j][4:]
                elif lines[j] == '':
                    pass  # Keep empty lines
            print(f'Fixed method {method_name} at lines {method_start+1}-{i}')
        method_start = i
        method_name = stripped.split('(')[0].strip()
        in_method = True
        method_lines.append(i)
    elif in_method and stripped.startswith('def ') and leading == 0:
        # Hit next top-level method
        for j in range(method_start, i):
            if lines[j].startswith('    '):
                lines[j] = lines[j][4:]
            elif lines[j] == '':
                pass
        print(f'Fixed method {method_name} at lines {method_start+1}-{i}')
        in_method = False
        method_start = -1

# Fix last method if still open
if in_method and method_start >= 0:
    for j in range(method_start, len(lines)):
        if lines[j].startswith('    '):
            lines[j] = lines[j][4:]
    print(f'Fixed method {method_name} at lines {method_start+1}-{len(lines)}')

open(r'O:\pythonproject\smart-video-reframer\gui\controller.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Done')