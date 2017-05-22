
### Django
from django.db import models

class Ontology(models.Model):

	### Properties
	date_created = models.DateTimeField(auto_now_add=False)
	iri = models.CharField(max_length=255)
	label = models.CharField(max_length=255)
	namespace = models.CharField(max_length=255)
	preferred_prefix = models.CharField(max_length=255)
	homepage_url = models.TextField()
	description = models.TextField()
	file_location = models.TextField()
	is_core = models.BooleanField(default=False)

class OntologyInstance(models.Model):

	### Connections
	ontology = models.ForeignKey('source.Ontology')

	### Properties
	name = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=False)

class BaseIRI(models.Model):

	### Connections
	ontology = models.ForeignKey('source.OntologyInstance', related_name='base_iris')

	### Properties
	value = models.CharField(max_length=255)

