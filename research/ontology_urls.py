
import re
import json

# ontology_class_file = '/Users/nicholaspiano/code/kuspo_modules_oct_2016/bao.owl'
ontology_class_file = '/Users/nicholaspiano/code/kuspo_modules_oct_2016/efo_2_76.owl'
iri_template = r'(?P<key>[^\s]+)="(?P<value>[^"]+)"'

iris = []
with open(ontology_class_file) as open_file:
    for match in re.finditer(iri_template, open_file.read()):
        iris.append(match)

structure = {}

for iri_match in iris:
    key = iri_match.group('key')
    value = iri_match.group('value')

    # split on non-word
    sd_iri = re.sub('[/#]', ' ', value[7:])

    if sd_iri:
        if key not in structure:
            structure[key] = {}
        substructure = structure[key]
        for token in sd_iri.split(' '):
            if token not in substructure and token != '':
                substructure[token] = {}

            if token != '':
                substructure = substructure[token]

print(json.dumps(structure, indent=2))
