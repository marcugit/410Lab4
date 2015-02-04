import sqlite3
from flask import Flask, request, redirect, url_for

app=Flask(__name__)
dbFile = 'db1.db'
conn = None


def get_conn():
	global conn
	if conn is None:
		conn = sqlite3.connect(dbFile)
		conn.row_factory = sqlite3.Row
		
	return conn

@app.teardown_appcontext
def close_conn(exception):
	global conn
	if conn is not None:
		conn.close()
		conn = None


def query_db(query,args=(), one=False):
	
	cur = get_conn().cursor()
	cur.execute(query, args)
	r = cur.fetchall()
	cur.close()
	return (r[0] if r else None) if one else r


def add_task(category, priority, description):
	
	if priority.isdigit():
		query_db('insert into tasks(category, priority, description) values(?,?,?)', [category, priority, description], one=True)
	
		get_conn().commit()

def delete_task(category, priority, description):
	query_db('delete from tasks where category==? and priority==? and description==?',[category, priority, description], one=True)
	
	get_conn().commit()



@app.route('/')
def welcome():
	return '<h1>Welcome to the Flask Lab!</h1>'


@app.route('/delete', methods = ['GET'])
def delete():
	category = request.args.get('category')
	priority = request.args.get('priority')
	description = request.args.get('description')
	delete_task(category, priority, description)
	return redirect(url_for('task'))

@app.route('/task', methods = ['GET', 'POST'])
def task():
	#POST:
	if request.method == 'POST':
		category = request.form['category']
		priority = request.form['priority']
		description = request.form['description']
		add_task(category, priority, description)
		return redirect(url_for('task'))


	#GET:
	resp = ''
	resp = resp+'''
	<form action="" method=post>
		<p>Category<input type=text name=category></p>
		<p>Priority<input type=text name=priority></p>
		<p>Description<input type=text name=description></p>
		<p><input type=submit value=Add></p>
	</form>
'''	
	
	#show table
	resp = resp+'''
	<table border = "1" cellpadding="3">
		<tbody>
			<tr>
				<th>Category</th>
				<th>Priority</th>
				<th>Description</th>
				<th></th>
			</tr>
'''	


	for task in query_db('select * from tasks'):
		
		resp = resp+"<tr><td>%s</td>"%(task['category'])

		resp = resp+"<td>%s</td>"%(task['priority'])
	
		resp = resp+"<td>%s</td>"%(task['description'])

		resp = resp+"<td><a href=\"/delete?category=%s&priority=%s&description=%s\""%(task['category'],task['priority'],task['description'])+" method=\"get\">Delete</button></td></tr>"

	resp = resp+'</tbody></table>'

	return resp





if __name__ == '__main__':
	app.debug = True
	app.run()
