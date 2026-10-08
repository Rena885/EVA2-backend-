import re

def fix_indentation(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # We want to find blocks of """ ... """ and align them to the NEXT line of code.
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == '"""':
            # Found start of docstring
            start_idx = i
            end_idx = i + 1
            while end_idx < len(lines) and lines[end_idx].strip() != '"""':
                end_idx += 1
                
            if end_idx < len(lines):
                # Found end of docstring. Find next code line to get its indent.
                next_code_idx = end_idx + 1
                while next_code_idx < len(lines) and lines[next_code_idx].strip() == '':
                    next_code_idx += 1
                    
                if next_code_idx < len(lines):
                    next_line = lines[next_code_idx]
                    target_indent = len(next_line) - len(next_line.lstrip())
                    
                    # Now adjust the docstring block to match target_indent
                    space = ' ' * target_indent
                    for j in range(start_idx, end_idx + 1):
                        lines[j] = space + lines[j].lstrip()
            
            i = end_idx + 1
        else:
            i += 1
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

for file in ['api/views.py', 'api/urls.py', 'core/models.py', 'api/permissions.py', 'api/serializers.py']:
    try:
        fix_indentation(file)
    except Exception as e:
        print(f"Error fixing {file}: {e}")
