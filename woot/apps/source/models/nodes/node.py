
### Django
from django.db import models


class NodeModel(models.Model):

	### Connections
	source = models.ForeignKey('source.OntologyInstance', related_name='models')
	base_iri = models.ForeignKey('source.BaseIRI', related_name='models')

	### Properties
	iri = models.CharField(max_length=255)
	label = models.TextField()
	obselete = models.BooleanField(default=False)
	pending = models.BooleanField(default=True)


class Node(models.Model):

	### Connections
	model = models.ForeignKey('source.NodeModel', related_name='nodes')

	### Properties
	date_created = models.DateTimeField(auto_now_add=True)


class NodeInstance(models.Model):

	### Connections
	node = models.ForeignKey('source.Node', related_name='instances')
	parent = models.ForeignKey('self', related_name='children')
	_subject_of = models.OneToOneField('self', related_name='_subject', null=True)
	_predicate_of = models.OneToOneField('self', related_name='_predicate', null=True)
	_object_of = models.OneToOneField('self', related_name='_object', null=True)

	### Properties
	value = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	### Methods


	### Python properties
	def get_subject_of(self):
		# account for nonexistent model on the other end
		if hasattr(self, '_subject_of'):
			return self._subject_of
		else:
			return None

	def set_subject_of(self, value):
		self._subject_of = value
		self.save()

	subject_of = property(get_subject_of, set_subject_of)

	def get_predicate_of(self):
		# account for nonexistent model on the other end
		if hasattr(self, '_predicate_of'):
			return self._predicate_of
		else:
			return None

	def set_predicate_of(self, value):
		self._predicate_of = value
		self.save()

	predicate_of = property(get_predicate_of, set_predicate_of)

	def get_object_of(self):
		# account for nonexistent model on the other end
		if hasattr(self, '_object_of'):
			return self._object_of
		else:
			return None

	def set_object_of(self, value):
		self._object_of = value
		self.save()

	object_of = property(get_object_of, set_object_of)