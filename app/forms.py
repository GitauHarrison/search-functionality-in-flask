from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import request


class PostForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')


class SearchForm(FlaskForm):
    q = StringField(
        'Search',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Search ...'})

    def __init__(self, *args, **kwargs):
        # formdata is where Flask gets form submissions
        if 'formdata' not in kwargs:
            # GET request: request.args, POST: request.form
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            # Disable CSRF for clickable link
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)
