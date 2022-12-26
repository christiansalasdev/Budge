from mongoengine import *

class User(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField()
    email = EmailField()
    password = StringField() 
