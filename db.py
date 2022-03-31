
        
import sqlite3 as sq
import sys
_database = 'trend.sqlite'

def init_db():
    db = sq.connect('trend.sqlite')
    with open('schema.sql') as f:
        db.executescript(f.read())
def helper(statement,values):
	connect = sq.connect(_database)
	cursor = connect.cursor()
	cursor.execute(statement,values)
	connect.commit()
	p = cursor.fetchall()
	connect.close()
	return p

def insert(user_id,location='worldwide'):
    try:
        helper("INSERT INTO User (chat_id,location) VALUES(?,?)",(user_id,location))
    except Exception as ex:
	    pass

def update_location(user_id,location):
    helper("UPDATE User SET location = ? WHERE chat_id = ?",(location,user_id))

def user_info(user_id):
    	return helper("SELECT location FROM User WHERE chat_id = ?",(int(user_id),))
 
def get_woeid(location):
	connect = sq.connect(_database)
	cursor = connect.cursor()
	try:
		cursor.execute('SELECT woeid FROM Location WHERE LOWER(name) = ?',(location.lower(),))
	except:
		sys.stderr.write('The Location is not included!')
		connect.close()
		return
	p = cursor.fetchone()
	connect.close()
	return p