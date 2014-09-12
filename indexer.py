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
		if not os.path.isdir(indexFolder):
			os.mkdir(indexFolder)

		self.cleanIndex(indexFolder, INDEX_PATH)

	def getSchema(self):
		return Schema(name=TEXT(stored=True), path=ID(unique=True, stored=True), time=STORED)

	def cleanIndex(self, indexFolder, paths):
		self.ix = create_in(indexFolder, schema=self.getSchema())
		self.writer = self.ix.writer()

		self.addDocuments(paths)
		self.writer.commit()

	def searchDocuments(self):
		with self.ix.searcher() as searcher:
			query = QueryParser('name', self.ix.schema).parse(u'*notepad*')
			results = searcher.search(query)
			if len(results) > 0:
				for result in results:
					print result
			else:
				print "no results"

	def addDocuments(self, paths):
		paths = paths.split(';')
		for path in paths:
			for dirPath, dirNames, fileNames in os.walk(path):
				for fileName in fileNames:
					if fileName.split('.')[-1] == 'lnk':
						fullPath = os.path.join(dirPath, fileName)
						targetPath = Dispatch('WScript.Shell').CreateShortCut(fullPath).Targetpath
						
						if targetPath.split('.')[-1] == 'exe':
							#add document to index
							fileName = fileName.split('.')[0]
							modTime = os.path.getmtime(fullPath)

							self.writer.add_document(name=unicode(fileName), path=unicode(targetPath), time=modTime)

dex = indexer()
dex.searchDocuments()