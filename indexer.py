import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
from win32com.client import Dispatch

SHORTCUT_PATH = \
os.environ['appdata'] + "\\Microsoft\\Windows\\Start Menu\\Programs\\;" + \
os.environ['programdata'] + "\\Microsoft\\Windows\\Start Menu\\Programs\\"

FILES_PATH = \
"C:\\Users\\" + os.environ['username'] + "\\Documents\\;" + \
"C:\\Users\\" + os.environ['username'] + "\\Downloads\\;" + \
"C:\\Users\\" + os.environ['username'] + "\\Music\\;" + \
"C:\\Users\\" + os.environ['username'] + "\\Pictures\\;"

class indexer():
	def __init__(self, indexFolder='indexDir'):
		paths = [SHORTCUT_PATH, FILES_PATH]

		if not os.path.isdir(indexFolder):
			os.mkdir(indexFolder)

		if index.exists_in(indexFolder):
			self.openOldIndex(indexFolder)
			print 'laoded old index'
		else:
			self.openNewIndex(indexFolder, paths)
			print 'loaded new index'

			print "more stuff"
	def getSchema(self):
		return Schema(name=TEXT(stored=True), path=ID(unique=True, stored=True), time=STORED)

	def openOldIndex(self, indexFolder):
		self.ix = index.open_dir(indexFolder)
		self.writer = self.ix.writer()

		#todo: check for updates in background (new thread)

	def openNewIndex(self, indexFolder, paths):
		self.ix = index.create_in(indexFolder, self.getSchema())
		self.writer = self.ix.writer()

		self.addShortcuts(paths[0])
		self.writer.commit()

	def addShortcuts(self, paths):
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

	def searchDocuments(self, search):
		print 'searching with: ' + search
		with self.ix.searcher() as searcher:
			query = QueryParser('name', self.ix.schema).parse(search)
			results = searcher.search(query)
			if len(results) > 0:
				for result in results:
					print result
			else:
				print "no results"
