
### Django
from django.core.management.base import BaseCommand, CommandError

### Local
from apps.source.models import Ontology, NodeModel, Node, NodeInstance

### Util
from rdflib import ConjunctiveGraph, OWL, RDF, RDFS
from os.path import basename, splitext

class Command(BaseCommand):

	def add_arguments(self, parser):
		# Path
		parser.add_argument('--path',
			action='store',
			dest='path',
			default='',
			help='Import path',
		)

	def handle(self, *args, **options):

		# http://www.ebi.ac.uk/ols/api/ontologies

		# args
		path = options['path']
		default_namespace = options['namespace']

		# vars
		path_label = splitext(basename(path))[0]

		# create conjunctive graph
		graph = ConjunctiveGraph()
		graph.parse(path, format="xml")

		# get ontology_iri
		ontology_iri = str([x for x, y, z in graph.triples((None, RDF.type, OWL.Ontology))][0])

		# get namespaces and create an ontology class for each one
		namespaces = {}
		for prefix, namespace in graph.namespaces():
			namespaces[namespace] = prefix
			if prefix:
				ontology, ontology_created = Ontology.objects.get_or_create(iri=namespace, label=prefix)

				# can I really rely on this?
				# Maybe there needs to be a better way of extracting the name of the ontology

		# iterate through all triples and make a new node_model for each one

		for s, p, o in graph.triples((None, None, None)):
			potential_subject_namespaces = [namespaces[n] for n in namespaces.keys() if n in str(s)]
			if potential_subject_namespaces:
				subject_namespace = potential_subject_namespaces[0]
			else:
				subject_namespace = default_namespace

			# subject_node_model, subject_node_model_created = NodeModel.objects.create()

			print('predicate', str(p), type(p), [namespaces[n] for n in namespaces.keys() if n in str(s)])
			print('object', str(o), type(o), [namespaces[n] for n in namespaces.keys() if n in str(s)])

		# need list of things I am going to ignore (i.e. not create nodes)