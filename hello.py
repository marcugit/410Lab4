from flask import Flask
app = Flask(__name__)

#decorator (to call the method)
@app.route('/hello')
def hello():
	return '<h1>hello Flask!</h1>'

@app.route('/bye')
def bye():
	return '<h1>bye Flask!</h1>'

if __name__ == '__main__':
	app.run()
