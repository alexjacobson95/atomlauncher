from whoosh.index import create_in 
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
from win32com.client import Dispatch

INDEX_PATH = \
os.environ['appdata'] + "\\Microsoft\\Windows\\Start Menu\\Programs\\;" + \
os.environ['programdata'] + "\\Microsoft\\Windows\\Start Menu\\Programs\\"

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

def testExplode():
	paths = INDEX_PATH.split(';')
	for dirPath, dirNames, fileNames in os.walk(paths[0]):
		for fileName in fileNames:
			if fileName.split('.')[-1] == 'lnk':
				targetPath = Dispatch('WScript.Shell').CreateShortCut(fullPath).Targetpath
				
				if targetPath.split('.')[-1] == 'exe':
					fullPath = os.path.join(dirPath, fileName)
					print fullPath + "\n" + targetPath




print INDEX_PATH
testExplode()
