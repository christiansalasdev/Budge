from mongoengine import *
import hashlib

DEV_DB_URI = "mongodb://localhost:27017/budge"

connect(host=DEV_DB_URI)


class User(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField()
    email = EmailField()
    password = StringField() 
    is_active = BooleanField(default=True)

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def verify_user(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == self.password:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.password = self.hash_password(self.password)
        return super(User, self).save(*args, **kwargs)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Bill(Document):
    id = SequenceField(primary_key=True)
    payer = ReferenceField(User)
    name = StringField()
    due_date = DateTimeField()
    amount = DecimalField()
    recurring = BooleanField()
    paid = BooleanField(default=False)

    def mark_as_paid(self):
        self.paid = True
        self.save()

class Paycheck(Document):
    id = SequenceField(primary_key=True)
    payee = ReferenceField(User)
    amount = DecimalField()
    pay_date = DateTimeField()


