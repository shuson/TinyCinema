__auther__ = 'shuson'
__version__ = 1.0

import os, glob,sqlite3

cwdir = os.getcwd()
def init_db():
	conn = sqlite3.connect(r'files.db')
	c = conn.cursor()
		
	c.execute("drop table if exists movies")
	conn.commit()
	
	#initialize table
	createSql = """create table movies (
		id integer primary key,
		name text not null,
		path text not null
		)"""

	c.execute(createSql)
	conn.commit()


def QueryFile(fileName):
  	roots = []
	dirs = []
	subdirs=[]
	files = []
	
	os.chdir(os.getcwd()[:3])

	for f in glob.glob('*.%s' %fileName):
		files.append('%s%s' %(os.getcwd(),f))

	for r in os.listdir(os.getcwd()):
		if os.path.isdir(r):
				roots.append(r)
	try:
		roots.remove('$RECYCLE.BIN')
		roots.remove('System Volume Information')
	except:
		pass

	for root in roots:
		for root,dir,file in os.walk(root):	
			dirs.append(root)

	for d in dirs:
		p = r'%s%s' %(os.getcwd()[:3],d)
		os.chdir(p)
		for f in glob.glob('*.%s' %fileName):
			files.append('%s%s\%s' %(os.getcwd()[:3],d,f))

	os.chdir(cwdir)

	#open and write to db
	conn = sqlite3.connect(r'files.db')
	conn.text_factory = str
	c = conn.cursor()
	
	#insert data
	i = 0
	for f in files:
		fName = f[f.rfind('\\')+1:]
		c.execute("insert into movies values (?,?,?)",(i,fName,f))
		i+=1

	conn.commit()
	
	#c.execute("select name from movies")
	#for row in c.fetchall():
	#	print row

	conn.close()

def run():
	init_db()
	fileTypes = ['zip']

	for ft in fileTypes:
			QueryFile(ft)

