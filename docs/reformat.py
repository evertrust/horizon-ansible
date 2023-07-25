import os
import re

# Adding captions in index file
with open('rst/index.rst', 'r') as file:
    content = file.read()
content = re.sub(r':hidden:\n.*\n( +)horizon_', r':hidden:\n\g<1>:caption: Module:\n\n\g<1>horizon_', content, 1)
content = re.sub(r':hidden:\n.*\n( +)horizon_', r':hidden:\n\g<1>:caption: Inventory:\n\n\g<1>horizon_', content, 1)
content = re.sub(r':hidden:\n.*\n( +)horizon_', r':hidden:\n\g<1>:caption: Lookup:\n\n\g<1>horizon_', content, 1)
with open('rst/index.rst', 'w') as file:
    file.write(content)

# Removing signature from titles
for file_name in os.listdir("rst"):
    if file_name.startswith("horizon_") :
        # Must remove signature title
        with open('rst/' + file_name, 'r') as file:
            content = file.read()
        content = re.sub(r'(\.\. Title)\n.*\n.*?-- (.*?)', r'\g<1>\n\n\g<2>', content, 1)
        with open('rst/' + file_name, 'w') as file:
            file.write(content)