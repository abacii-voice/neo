
### Local
from apps.source.models.nodes.ontology import Ontology
from apps.source.models.nodes.node import NodeModel, Node, NodeInstance

### Methods
def one_to_one_field_property(attr):
	def get_field(self):
		if hasattr(self, attr):
			return getattr(self, attr)
		else:
			return None

	def set_field(self, value):
		setattr(self, attr, value)
		self.save()

	return property(get_field, set_field)