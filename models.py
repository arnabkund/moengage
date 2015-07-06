import datetime
from flask import url_for
from moengage import db

class Users(db.Document):
    first_name = db.StringField(max_length=255,required=True)
    last_name = db.StringField(max_length=255,required=True)
    user_id = db.StringField(max_length=255,required=True)
    email = db.StringField(max_length=255,required=True)
    locale = db.StringField(max_length=255)
    timezone = db.StringField(max_length=255)
    image_url = db.StringField(max_length=255)
    gender = db.StringField(max_length=255)
    created_at = db.DateTimeField(default=datetime.datetime.now(),required=True)
    last_login = db.DateTimeField(default=datetime.datetime.now(),required=True)

class Friends(db.Document):
    user_id = db.StringField(max_length=255,required=True)
    friend_list = db.ListField()

class Tags(db.Document):
    post_id = db.StringField(max_length=255)
    tag_id = db.StringField(max_length=255)

class Comment(db.EmbeddedDocument):
    author_id = db.StringField(max_length=255,required=True)
    author_name = db.StringField(max_length=255,required=True)
    text = db.StringField(verbose_name="Comment", required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now(),required=True)


class Posts(db.Document):
    post_id = db.StringField(max_length=255)
    author_id = db.StringField(max_length=255,required=True)
    author_name = db.StringField(max_length=255,required=True)
    tagged_friend_ids = db.ListField()
    post = db.StringField(max_length=255,required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    created_at = db.DateTimeField(default=datetime.datetime.now(),required=True)
