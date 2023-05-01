from app import app, db
from flask import render_template, url_for, session, request, flash, redirect, g
from app.forms import PostForm
from app.models import User, Post
from app.forms import SearchForm

# Executed before the a function
@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(
        g.search_form.q.data,
        page,
        app.config['POSTS_PER_PAGE'])
    next_url = url_for(
        'search',
        q=g.search_form.q.data,
        page=page + 1) if total > page * app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for(
        'search',
        q=g.search_form.a.data,
        page=page - 1) if total > 1 else None
    return render_template(
        'search.html',
        title='Search',
        posts=posts,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        post = Post(body=form.body.data, author=user)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()
        flash('Saved.')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'index.html',
        title='Home',
        form=form,
        posts=posts,
        next_url=next_url,
        prev_url=prev_url)
