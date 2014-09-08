from whoosh.index import create_in 
from whoosh.fields import *
from whoosh.qparser import QueryParser
import settings
import os

class indexer():
	def __init__(self, indexFolder='indexDir'):
		self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
		
		if not os.path.isdir(indexFolder):
			os.mkdir(indexFolder)

		self.ix = create_in(indexFolder, self.schema)
		self.writer = self.ix.writer()

	def addDocument(self):
		self.writer.add_document(title=u'First Document', path=u'/a', content=u'This is the first document added!')
		self.writer.commit()

	def searchDocuments(self):
		with self.ix.searcher() as searcher:
			query = QueryParser('content', self.ix.schema).parse('first')
			results = searcher.search(query)
			print results[0]


ind = indexer()
ind.addDocument()
ind.searchDocuments()