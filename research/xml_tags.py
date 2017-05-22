
import re
import json

# ontology_class_file = '/Users/nicholaspiano/code/kuspo_modules_oct_2016/bao.owl'
ontology_class_file = '/Users/nicholaspiano/code/kuspo_modules_oct_2016/efo_2_76.owl'
tag_template = r'<(?P<ns>[^:!/?]+):(?P<sub>[^\s>!?]+)'

tags = {}
with open(ontology_class_file) as open_file:
    for match in re.finditer(tag_template, open_file.read()):
        ns = match.group('ns')
        sub = match.group('sub')

        if ns not in tags:
            tags[ns] = []
        if sub not in tags[ns]:
            tags[ns].append(sub)

print(json.dumps(tags, indent=2))