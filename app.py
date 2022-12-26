from models import User
from flask import Flask, render_template, redirect, url_for

User1 = User(user_name = "toby", email = "toby@aol.com", password = "ilovepablo")

User1.save()