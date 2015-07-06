from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from moengage.models import Users,Comment,Posts,Friends,Tags
from moengage import app,db
import datetime
from bson.objectid import ObjectId
import uuid
moe = Blueprint('moengage', __name__, template_folder='templates')

class Login(MethodView):

    def get(self):
        return render_template('moengage/index.html')

class Logout(MethodView):

    def get(self):
        posts = Posts.objects.all()
        return render_template('moengage/list.html', posts=posts)

class Home(MethodView):

    def get(self):
        posts = Posts.objects.all()
        return render_template('moengage/home.html', posts=posts)

class MakePosts(MethodView):

    def get(self):
        posts = Posts.objects.all()
        return render_template('moengage/posts.html', posts=posts)

class FindTags(MethodView):

    def get(self):
        posts = Posts.objects.all()
        return render_template('moengage/list.html', posts=posts)


class InsertUser(MethodView):
    #decorators = [cors.crossdomain(origin='*')]
    #form = model_form(Users,exclude=['created_at'])

    def post(self):
        data = request.get_json()
        print data
        user_id = data['id']
        try:    
            user  = Users.objects.get(user_id=user_id)

            if not user.image_url == data['link']:
                user.image_url = data['link']
            user.last_login = datetime.datetime.now()
            user.save()

            #update friend_list

            friends = Friends.objects.get(user_id=user_id)
            if not friends.friend_list == data['friends']:
                friends.friend_list = data['friends']
            friends.save()

            # send to feed page, also send you the list of posts

            #get all the tags and post_ids

            posts = []
            all_tags = Tags.objects.filter(tag_id=user_id)
            for i in all_tags:
                post_id = i.post_id
                posts.append(Posts.objects.get(post_id=post_id))
            print posts
            #posts = Posts.objects.filter(author_id=user_id)
            return jsonify({'status':'success','posts':posts})
        
        except Exception:
            # register the guy in the mongo db
            #raise
            return self.register(data)
    
    def register(self,data):
        print "in register"

        try:
            #get user details
            user_id = data['id']
            first_name = data['first_name']
            last_name = data['last_name']
            image_url = data['link']
            gender = data['gender']
            email = data['email']
            timezone = str(data['timezone'])
            friend_list = data['friends']
            locale = data['locale']

            #create a user object
            user = Users(user_id=user_id,first_name=first_name,last_name=last_name,image_url=image_url,gender=gender,email=email,timezone=timezone,locale=locale)

            #add friend list
            friends = Friends(user_id=user_id,friend_list=friend_list)

            #save objects
            user.save()
            friends.save()
            return jsonify({'status':'success'})
        except Exception, e:
            raise
            return jsonify({'status':'error'})

class InsertPost(MethodView):

    def post(self):
        data = request.get_json()
        user_id = data['author_id']
        user_name = data['author_name']
        user  = Users.objects.get(user_id=user_id)
        friends_list = []
        dic = data['tag_list']
        for k,v in dic.items():
            if dic[k]:
                friends_list.append(k)
        if not user == None:
            # valid post
            try:
                post = Posts(post_id=str(uuid.uuid4()),author_name=user_name,author_id=user_id,tagged_friend_ids=friends_list,post=data['post_data'])
                post.save()
                post_id = post.post_id
                # also save in tag model for faster retrieval of posts
                for i in friends_list:
                    tag = Tags(post_id=post_id,tag_id=i)
                    tag.save()
                return jsonify({'status':'success'})
            except Exception:
                raise
                return jsonify({'status':'error'})    
        else:
            # cannot make a post , since user should not exist !
            return jsonify({'status':'error'})

class InsertComment(MethodView):

    def post(self):
        data = request.get_json()
        print data
        author_id = data['author_id']
        user_id = data['user_id']
        user  = Users.objects.get(user_id=user_id)
        post_id = data['oid']
        user_name = data['user_name']
        if not user == None:
            # valid post
            try:
                print "in try"
                post = Posts.objects.get(post_id=post_id)
                comment = Comment(author_id=user_id,text=data['comment'],author_name=user_name)
                post.comments.append(comment)
                post.save()
                posts = []
                all_tags = Tags.objects.filter(tag_id=user_id)
                for i in all_tags:
                    post_id = i.post_id
                    posts.append(Posts.objects.get(post_id=post_id))
                return jsonify({'status':'success','posts':posts})
            except Exception,e:
                raise
                return jsonify({'status':'error'})
        else:
            # cannot make a post , since user should not exist !
            return jsonify({'status':'error'})

moe.add_url_rule('/', view_func=Login.as_view('login'))
moe.add_url_rule('/logout/', view_func=Logout.as_view('logout'))
moe.add_url_rule('/home/', view_func=Home.as_view('home'))
moe.add_url_rule('/insert_user/', view_func=InsertUser.as_view('insert_user'))
moe.add_url_rule('/insert_post/', view_func=InsertPost.as_view('insert_post'))
moe.add_url_rule('/insert_comment/', view_func=InsertComment.as_view('insert_comment'))
moe.add_url_rule('/find_tags/', view_func=FindTags.as_view('find_tags'))
