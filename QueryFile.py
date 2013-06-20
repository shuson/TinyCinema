__auther__ = 'shuson'
__version__ = 1.0

import os, glob,sqlite3

def QueryFile(fileName):
  	roots = []
	dirs = []
	subdirs=[]
	files = []

	for f in glob.glob('*.%s' %fileName):
		files.append('%s%s' %(os.getcwd(),f))

	for r in os.listdir(os.getcwd()):
		if os.path.isdir(r):
				roots.append(r)

	roots.remove('$RECYCLE.BIN')
	roots.remove('System Volume Information')

	for root in roots:
		for root,dir,file in os.walk(root):	
			dirs.append(root)

	for d in dirs:
		p = r'%s%s' %(os.getcwd()[:3],d)
		os.chdir(p)
		for f in glob.glob('*.%s' %fileName):
			files.append('%s%s\%s' %(os.getcwd()[:3],d,f))

	os.chdir(os.getcwd()[:3])

	#open and write to db
	conn = sqlite3.connect(r'files.db')
	conn.text_factory = str
	c = conn.cursor()
	
	#initialize table
	createSql = """create table movies (
		id integer primary key,
		name text not null,
		path text not null
		)"""
	
	c.execute("drop table if exists movies")
	conn.commit()

	c.execute(createSql)
	conn.commit()

	#insert data
	i = 0
	for f in files:
		fName = f[f.rfind('\\')+1:]
		print fName,f
		c.execute("insert into movies values (?,?,?)",(i,fName,f))
		i+=1

	conn.commit()
	
	#c.execute("select name from movies")
	#for row in c.fetchall():
	#	print row

	conn.close()

QueryFile('mkv')

