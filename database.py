import sqlite3 as sq
import sys
_database = 'trend.sqlite'


def helper(statement):
	connect = sq.connect(_database)
	cursor = connect.cursor()
	cursor.execute(statement)
	connect.commit()
	p = cursor.fetchall()
	connect.close()
	return p

def insert(user_id,hupdate=1, mupdate=0, location='worldwide'):
	helper('INSERT INTO User VALUES({},{},{},"{}")'.format(user_id, hupdate, mupdate, location))

def update_info(user_id,**kwargs):
	for k, v in zip(kwargs.keys(),kwargs.values()):
		helper('UPDATE User SET {}="{}" WHERE uid={}'.format(k,v,user_id))

def user_info(user_id):
	return helper('SELECT hupdate, mupdate, location FROM User WHERE uid = %s'%(int(user_id)))

def get_woeid(location):
	connect = sq.connect(_database)
	cursor = connect.cursor()
	try:
		cursor.execute('SELECT woeid FROM Location WHERE LOWER(name) = "{}"'.format(location.lower()))
	except:
		sys.stderr.write('The Location is not included!')
		connect.close()
		return
	p = cursor.fetchone()
	connect.close()
	return p
