from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['first']) < 2 or len(postData['last']) < 2 and not NAME_REGEX.match(postData['first']) or not NAME_REGEX.match(postData['last']):
            errors.append("First/last name should be more than 2 characters and must only contain alphabetic characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in correct format.")
        if len(postData['password']) < 8:
            errors.append("Password must be 8 or more characters!")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords must match!")
        if len(User.objects.filter(email = postData['email'])):
            errors.append("Email is already in use.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first'], last_name = postData['last'], email = postData['email'], password = hashed_pw, user_level = 1)
            if len(User.objects.all()) == 1:
                user.user_level = 9000
                user.save()
            res['data'] = user
        return res

    def login_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        try:
            the_user = User.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            res['data'] = the_user
            return res
        else:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res

    def edit_info_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['first']) < 2 or len(postData['last']) < 2 and not NAME_REGEX.match(postData['first']) or not NAME_REGEX.match(postData['last']):
            errors.append("First/last name should be more than 2 characters and must only contain alphabetic characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in correct format.")
        if len(User.objects.filter(email = postData['email'])) and User.objects.get(id = postData['user_id']).email != postData['email']:
            errors.append("Email is already in use.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            info_user = User.objects.get(id = postData['user_id'])
            if postData['user_type'] == "9000":
                info_user.user_level = 9000
            else:
                info_user.user_level = 1
            info_user.first_name = postData['first']
            info_user.last_name = postData['last']
            info_user.email = postData['email']
            info_user.save()
            res['data'] = info_user
        return res

    def edit_password_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['password']) < 8:
            errors.append("Password must be 8 or more characters!")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords must match!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            updated_hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            password_user = User.objects.get(id = postData['user_id'])
            password_user.password = updated_hashed_pw
            password_user.save()
            res['data'] = password_user
        return res

    def edit_description_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        if len(postData['description']) < 10:
            res['status'] = "bad"
            res['data'] = "Description must be 10 or more characters!"
        else:
            description_user = User.objects.get(id = postData['user_id'])
            description_user.description = postData['description']
            description_user.save()
            res['data'] = description_user
        return res

class MessageManager(models.Manager):
    def message_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        if len(postData['message']) < 5:
            res['status'] = "bad"
            res['data'] = "Message must be more than 5 characters long"
        else:
            message = Message.objects.create(content = postData['message'], user_id = postData['user_id'], poster_id = postData['poster_id'])
            res['data'] = message
        return res

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        if len(postData['comment']) < 5:
            res['status'] = "bad"
            res['data'] = "Comment must be more than 5 characters long"
        else:
            comment = Comment.objects.create(content = postData['comment'], message_id = postData['message_id'], poster_id = postData['poster_id'])
            res['data'] = comment
        return res
        
        

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    description = models.TextField(default = '')
    user_level = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Message(models.Model):
    content = models.TextField(default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "messages")
    poster = models.ForeignKey(User, related_name = "posted_messages")

    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField(default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    message = models.ForeignKey(Message, related_name = "comments")
    poster = models.ForeignKey(User, related_name = "posted_comments")

    objects = CommentManager()

