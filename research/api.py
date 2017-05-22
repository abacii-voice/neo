import exceptions
import json

from ontospy.core.utils import isBlankNode
from rdflib import ConjunctiveGraph
from rdflib import OWL
from rdflib import RDF
from rdflib import RDFS


class OntologyAPI(object):
	"""Class that includes methods for querying an RDFS/OWL ontology"""

	def __init__(self, uri, language=""):
		super(OntologyAPI, self).__init__()

		self.rdfGraph = ConjunctiveGraph()
		try:
			self.rdfGraph.parse(uri, format="xml")
		except Exception as e:
			print 'xml failed'
			print e.args
			print e.message
			try:
				self.rdfGraph.parse(uri, format="n3")
			except Exception as e:
				print 'n3 failed'
				print e.args
				print e.message
				raise exceptions.Error("Could not parse the file! Is it a valid RDF/OWL ontology?")

		finally:
			#get list of all classes and the base of the ontology
			self.baseURI = self.getOntologyURI() or uri
			self.allclasses = self.getAllNamedClasses()
			self.topClasses = self.getTopClasses()

	def getOntologyURI(self, return_as_string=True):
		ontology_uri = [x for x, y, z in self.rdfGraph.triples((None, RDF.type, OWL.Ontology))]

		if ontology_uri:
			if return_as_string:
				return str(ontology_uri[0])
			else:
				return ontology_uri[0]
		else:
			return None

	def getAllNamedClasses(self, classPredicate="", removeBlankNodes=True):
		"""
		Extracts all the classes from a model
		We use the RDFS and OWL predicate by default; also, we extract non explicitly declared classes
		"""

		rdfGraph = self.rdfGraph
		entities = set()

		# estimate lengths
		print 'owl classes'
		print len(list(rdfGraph.triples((None, RDF.type, OWL.Class))))

		print 'rdfs classes'
		print len(list(rdfGraph.triples((None, RDF.type, RDFS.Class))))

		print 'subclass of anything'
		print len(list(rdfGraph.triples((None, RDFS.subClassOf, None))))

		print 'rdfs domain'
		print len(list(rdfGraph.triples((None, RDFS.domain, None))))

		print 'rdfs range'
		print len(list(rdfGraph.triples((None, RDFS.range, None))))


		if not classPredicate:
			for s, v, o in rdfGraph.triples((None, RDFS.comment, None)):
				print(s, v, o, self.getRDFSLabel(s))

			print 'getting owl classes'
			for s, v, o in rdfGraph.triples((None, RDF.type, OWL.Class)):
				entities.add(s)
			print 'getting rdf classes'
			for s, v, o in rdfGraph.triples((None, RDF.type, RDFS.Class)):
				entities.add(s)

			# this extra routine makes sure we include classes not declared explicitly
			# eg when importing another onto and subclassing one of its classes...
			print 'getting unnamed axioms'
			for s, v, o in rdfGraph.triples((None, RDFS.subClassOf, None)):
				entities.add(s)
				entities.add(o)

			# this extra routine includes classes found only in rdfs:domain and rdfs:range definitions
			for s, v, o in rdfGraph.triples((None, RDFS.domain, None)):
				entities.add(o)
			for s, v, o in rdfGraph.triples((None, RDFS.range, None)):
				entities.add(o)

		else:
			if classPredicate == "rdfs" or classPredicate == "rdf":
				for s, v, o in rdfGraph.triples((None, RDF.type, RDFS.Class)):
					entities.add(s)
			elif classPredicate == "owl":
				for s, v, o in rdfGraph.triples((None, RDF.type, OWL.Class)):
					entities.add(s)
			else:
				raise exceptions.Error("ClassPredicate must be either rdf, rdfs or owl")

		#return sort_uri_list_by_name(entities)
		return list(entities)

	# methods for getting ancestores and descendants of classes: by default, we do not include blank nodes

	def getDirectSuperclasses(self, uri, excludeBnodes=True):
		returnlist = set()
		for s, v, o in self.rdfGraph.triples((uri, RDFS.subClassOf, None)):
			if excludeBnodes:
				if not isBlankNode(o):
					returnlist.add(o)
			else:
				returnlist.add(o)

		return list(returnlist)

	def getDirectSubclasses(self, uri, excludeBnodes=True):
		returnlist = set()
		for s, v, o in self.rdfGraph.triples((None, RDFS.subClassOf, uri)):
			if excludeBnodes:
				if not isBlankNode(s):
					returnlist.add(s)

			else:
				returnlist.add(s)

		return list(returnlist)

	def getDescendants(self, uri, excludeBnodes=True):

		return self.getTransitiveSubjects(RDFS.subClassOf, uri)
		'''
		for sub in self.getDirectSubclasses(uri, excludeBnodes):
			if sub != returnlist:
				returnlist.add(sub)
				self.getDescendants(sub, returnlist, excludeBnodes)
		return list(returnlist)
		'''

	def getAncestors(self, uri, excludeBnodes=True):

		return self.getTransitiveObjects(uri, RDFS.subClassOf)
		'''
		for superc in self.getDirectSuperclasses(uri, excludeBnodes):
			returnlist.add(superc)
			self.getAncestors(superc, returnlist, excludeBnodes)
		return list(returnlist)
		'''

	def getClassSiblings(self, uri, excludeBnodes=True):
		returnlist = set()
		for father in self.getDirectSuperclasses(uri, excludeBnodes):
			for child in self.getDirectSubclasses(father, excludeBnodes):
				if child != uri:
					returnlist.add(child)

		return list(returnlist)


	def getValuesForGivenProperty(self, subject, property):
		results = self.rdfGraph.triples((subject, property, None))
		values = []
		for s, p, o in results:
			values.append(o)
		return values

	def getRDFSLabel(self, subject):
		results = self.rdfGraph.label(subject)
		return results

	def getTransitiveSubjects(self, predicate, object):
		results = self.rdfGraph.transitive_subjects(predicate, object)
		values = set()
		for s in results:
			if not isBlankNode(s):
				values.add(s)
		if object in values:
			values.remove(object)
		return list(values)

	def getTransitiveObjects(self, subject, predicate):
		values = set()
		for o in self.rdfGraph.transitive_objects(subject, predicate):
			if not isBlankNode(o):
				values.add(o)
		if subject in values:
			values.remove(subject)
		return list(values)

	def getTopClasses(self, classPredicate=''):

		""" Finds the topclass in an ontology (works also when we have more than on superclass)
		"""
		returnlist = set()

		# gets all the classes
		for eachclass in self.allclasses:
			x = self.getDirectSuperclasses(eachclass)
			if not x:
				returnlist.add(eachclass)

		return list(returnlist)

	def getClassTree(self, father=None, out=None):

		""" Reconstructs the taxonomical tree of an ontology, from the 'topClasses' (= classes with no supers, see below)
			Returns a dictionary in which each class is a key, and its direct subs are the values.
			The top classes have key = 0

			Eg.
			{'0' : [class1, class2], class1: [class1-2, class1-3], class2: [class2-1, class2-2]}
		"""

		if not father:
			out = {}
			topclasses = self.topClasses
			out[0] = topclasses

			for top in topclasses:
				children = self.getDirectSubclasses(top)
				out[top] = children
				for potentialfather in children:
					self.getClassTree(potentialfather, out)

			return out

		else:
			children = self.getDirectSubclasses(father)
			out[father] = children
			for ch in children:
				self.getClassTree(ch, out)


