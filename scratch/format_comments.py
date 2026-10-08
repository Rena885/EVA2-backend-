import os
import re
import textwrap

def reformat_comments(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    
    for line in lines:
        if '# RR -' in line:
            # Split code and comment
            parts = line.split('# RR -')
            code_part = parts[0].rstrip()
            comment_part = 'RR -' + parts[1].strip()
            
            # Indentation of the code
            indent = len(code_part) - len(code_part.lstrip())
            space = ' ' * indent
            
            # Format comment
            wrapped = textwrap.fill(comment_part, width=60)
            docstring = f"{space}\"\"\"\n"
            for wline in wrapped.split('\n'):
                docstring += f"{space}{wline}\n"
            docstring += f"{space}\"\"\"\n"
            
            # Insert docstring before the code!
            # Special case for dict keys: it's better to put them as # comments above the key 
            # to avoid syntax errors inside dictionaries or classes where a raw string isn't allowed without assignment.
            # But the user asked for """ """. Python allows standalone strings inside classes/functions, 
            # but NOT inside dict definitions (like in settings.py SIMPLE_JWT).
            
            # Let's check if it's inside a dict or list (ends with comma)
            if code_part.endswith(','):
                # Use # for safety to avoid breaking dictionaries
                docstring = ""
                for wline in wrapped.split('\n'):
                    docstring += f"{space}# {wline}\n"
            
            new_lines.append(docstring)
            new_lines.append(code_part + '\n')
        else:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for file in [
    'ticketRB/settings.py',
    'core/models.py',
    'api/serializers.py',
    'api/permissions.py',
    'api/views.py',
    'api/urls.py'
]:
    reformat_comments(file)
