from flask import jsonify, render_template, flash, redirect, url_for, request, g
from app import app,db
from app.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app.translate import translate

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language =detect(form.post.data)
        except LangDetectException():
            language=''
        post = Post( content=form.post.data, author=current_user, language=language )
        db.session.add(post)
        db.session.commit()
        flash(_('Posted'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1,type=int)
    posts=current_user.followed_posts().paginate(page=page,
        per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url= url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='Home',form=form,posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
    page=request.args.get('page', 1, type=int)
    posts= Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url= url_for('explore',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html',title='Explore', posts=posts.items,next_url=next_url, prev_url=prev_url)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Your account has been created!'))
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
@app.route('/about')
@login_required
def about():
    return render_template('about.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if  user is None or not user.check_password(form.password.data):
            flash(_('Check your credentials and try again!'))
            return redirect(url_for('login'))
        login_user(user, remember= form.remember.data)
        next_page = request.args.get('next')

        return redirect(next_page )if next_page else  redirect(url_for('index'))
         
    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username ).first_or_404()
    page=request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page,
                    per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user' ,username=user.username,page=posts.next_num ) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', title='Profile Page', user = user, posts = posts, next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('updated ✔'))
        return redirect(url_for('user', username=current_user.username))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email= form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.txt', form=form)

@app.route('/translate',methods=['GET','POST'])
@login_required
def translate_text():
    data = request.get_json()
    text = data['text']
    source_lang=data['sourceLang']
    dest_lang=data['destLang']
    translated_text= translate(text, source_lang, dest_lang)
    return jsonify({'text':translated_text})                    