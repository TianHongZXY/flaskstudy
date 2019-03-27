from flask import Flask, request, render_template, redirect, \
    url_for, abort, make_response, json, jsonify, session, g, current_app,\
    Markup 
import click
import os
from urllib.parse import urlparse, urljoin
from jinja2 import escape
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
bootstrap = Bootstrap()
bootstrap.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    name = g.name
    if name is not None:
        # name = request.cookies.get('name', 'human')
        # name = request.args.get('name', 'human')
        response = '<h1>Hello %s!</h1>' % escape(name)

        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    else:
        response = '<h1>Hello!</h1>'
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
    return '<p>Welcome to %d!</p><a href="%s">goback</a>' % ((2019 - year), url_for('hello'))


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
        'name': 'Jason Zhu',
        'gender': 'male'
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
    return '<h1>foo page</h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>bar page</h1><a href="%s">Do something</a>' % url_for('do_something')


@app.route('/do_something')
def do_something():
    # print(request.referrer)

    # return 'after do thing and then you can go back to %s' % request.referrer
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for('hello', **kwargs))

def is_safe_url(target):
    # 获取程序内主机的url
    ref_url = urlparse(request.host_url)
    # 用urljoin将目标url转换为绝对url, urlparse解析url
    test_url = urlparse(urljoin(request.host_url, target))
    print(ref_url.netloc)
    print(test_url.netloc)
    return test_url.scheme in ('http', 'https') and \
		ref_url.netloc == test_url.netloc

from jinja2.utils import generate_lorem_ipsum
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2) # 生成 两 段 随机 文本
    # return ''' <h1> A very long post</h1> 
    # <div class="body">%s</div> 
    # <button id="load"> Load More</ button> 
    # <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    # <script type="text/javascript"> 
    # $(function() { 
    #     $('#load').click(function(){ 
    #     $.ajax({
    #     url:'/more', // 目标URL 
    #     type:'get', // 请求方法 
    #     success:function(data){ // 返回2XX 响应后触发的回调函数 
    #         $('.body').append(data); // 将返回的响应插入到页面中 
    #         }
    #         })
    #         })
    #         })
    #         </script>''' % post_body
    return render_template('post.html', post_body=post_body)

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

@app.route('/watchlist')
def watchlist():
    zxy = {'username':'zhuxinyu'}
    return render_template('watchlist.html',user=zxy, movies=movies)

# 自定义上下文
# 模板上下文处理函数，渲染任意模板时，上下文处理函数都会被执行
# 它们的返回值在任意一个模板中都可用
@app.context_processor
def inject_foo():
    foo = 'You are a foo.'
    return {'foo':foo}

# 自定义全局函数
# 在模板中可以直接使用
# name默认为函数名，也可自定义
@app.template_global(name='bar')
def bar():
    return 'I am your baba.'

@app.template_filter(name='musical')
def musical(s):
    # Markup类可以标记安全字符，即不转义
    return s + Markup(' &#9835;')

# 3.2.5模板环境对象 jinja_env

# 添加自定义全局对象
def barrrr():
    return 'I am your father!'

fooooo = 'You are so silly.'
app.jinja_env.globals['barrrr'] = barrrr
app.jinja_env.globals['fooooo'] = fooooo

# 添加自定义过滤器
def smiling(s):
    return s + ' :) '

app.jinja_env.filters['smiling'] = smiling

# 添加自定义测试器
def zxybirth(n):
    if n == '199933':
        return True
    return False
app.jinja_env.tests['zxybirth'] = zxybirth
