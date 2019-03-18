from flask import Flask
import click
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello Flask!</h1>' + app.name

@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='default'):
	return '<h1>Hello, %s!</h1>' % name

@app.cli.command('say-hello')
def hello():
	'''just say hello'''
	click.echo('Hello, human!')