from mongoengine import *
import hashlib

class User(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField()
    email = EmailField()
    password = StringField() 

    def save(self, *args, **kwargs):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()
        return super(User, self).save(*args, **kwargs)

class Bill(Document):
    id = SequenceField(primary_key=True)
    user_id = ReferenceField(User)
    name = StringField()
    due_date = DateField()
    amount = DecimalField()
    paid = BooleanField(default=False)

