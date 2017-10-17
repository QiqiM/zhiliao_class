# encoding:utf-8

from flask import Flask, render_template, request, redirect, url_for, session,g
import config  # 导入配置文件
from models import User, Question, Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 绑定配置文件

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-creat_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 如果在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'手机号码已注册，请换号码！'
        else:
            # password1要和password2相等
            if password1 != password2:
                return u'两次密码不相等，请重新输入'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就跳转到登录页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # session.clear()
    del session['user_id']
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required  # 如果未登录，则不能进入发布问答页面
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        # question.author = user
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


# 问答详情
@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    # user_id = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    # answer.author = user
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("detail", question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    #title,content 用或操作引入_or模块，与操作直接写入过滤函数就行
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-creat_time')
    return render_template('index.html',questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user': user}
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}
#before_request -> 视图函数 -> context_processor

if __name__ == '__main__':
    app.run()
