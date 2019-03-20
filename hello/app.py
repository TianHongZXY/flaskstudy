from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session, g, current_app
import click
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

@app.route('/')
@app.route('/hello')
def hello():
	name = g.name
	if name is None:
		name = request.cookies.get('name', 'human')
		response = '<h1>Hello Flask!</h1>' + name

		if 'logged_in' in session:
			response += '[Authenticated]'
		else:
			response += '[Not Authenticated]'
	return response

@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='default'):
	return '<h1>Hello, %s!</h1>' % name

@app.cli.command('say-hello')
def hello():
	'''just say hello'''
	click.echo('Hello, human!')

@app.route('/hi')
def hi():
	return redirect(url_for('hello'))

@app.route('/goback/<int:year>')
def go_back(year):
	return '<p>Welcome to %d!</p><a href="%s">goback</a>' % (2019 - year), url_for('hello')

@app.before_request
def do_before_request():
	pass

@app.route('/404')
def not_found():
	abort(404)

@app.route('/mimetype')
def mime_type():
	response = make_response('<h1>Hello, world</h1>')
	response.mimetype = 'text/plain'
	return response

@app.route('/notes')
def notes():
	note = {
		'name':'Jason Zhu',
		'gender':'male'
	}
	response = make_response(json.dumps(note))
	response.mimetype = 'application/json'
	return response

@app.route('/jsonifynotes')
def jsonify_notes():
	return jsonify(name='Jason Zhu', gender='male')

@app.route('/set/<name>')
def set_cookie(name):
	response = make_response(redirect(url_for('hello')))
	response.set_cookie('name', name)
	return response

@app.route('/login')
def login():
	session['logged_in'] = True
	return redirect('/hello')

@app.route('/logout')
def logout():
	response = make_response(redirect('hello'))
	if 'logged_in' in session:
		session.pop('logged_in')
		response.delete_cookie('name')
	return response

@app.before_request
def get_name():
	g.name = request.args.get('name')

@app.route('/foo')
def foo():
	return '<h1>foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
	return '<h1>bar page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/do_something')
def do_something():
	# print(request.referrer)

	return 'after do thing and then you can go back to %s' % request.referrer
	# return redirect(request.referrer or url_for('hello'))