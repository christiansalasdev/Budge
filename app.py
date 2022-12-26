from datetime import datetime
from models import User, Bill, Paycheck
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, current_user

login_manager = LoginManager()


app = Flask(__name__)

app.config['SECRET_KEY'] = "8lJFz9pnU6l0xXT4RqkQmB3XV_lmr1TwSY-WMFEsGec"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id = user_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(user_name = user_name, email = email, password = password)
        user.save()
    return redirect(url_for("index"))

@app.route("/app/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        user = User.objects.get(user_name = user_name)
        verified = user.verify_user(password)
        if verified:
            login_user(user)
        else:
            return "A user with that username does not exist or the password is incorrect."
    return redirect(url_for("index"))

@app.route("/app/add_bill", methods=['GET', 'POST'])
def add_bill():
    if request.method == 'GET':
        return render_template("add_bill.html")
    if request.method == 'POST':
        name = request.form['name']
        due_date = request.form['due_date']
        amount = float(request.form['amount'])
        recurring = request.form['recurring']
        bill = Bill(payer = current_user, name = name, due_date = due_date, amount = amount, recurring = recurring)
        bill.save()
        return "Bill was added."

@app.route("/app/add_paycheck", methods=['GET', 'POST'])
def add_paycheck():
    if request.method == 'GET':
        return render_template("add_paycheck.html")
    if request.method == 'POST':
        amount = float(request.form['amount'])
        pay_date = request.form['pay_date']

        paycheck = Paycheck(payee = current_user, amount = amount, pay_date = pay_date)
        paycheck.save()
    
        return "Paycheck was added."


@app.route("/app/bills")
def bills():
    if request.method == 'GET':
        bills = Bill.objects(payer = current_user)
        return render_template("bills.html", bills = bills)

@app.route("/app/paychecks")
def paychecks():
    if request.method == 'GET':
        paychecks = Paycheck.objects(payee = current_user)
        bills = Bill.objects(payer = current_user)
        return render_template("paychecks.html", paychecks = paychecks, bills = bills)

@app.route("/paycheck/<id>")
def get_paycheck(id):
    paycheck = Paycheck.objects.with_id(id)
    if paycheck:
        if paycheck.payee == current_user:
            future_paychecks = Paycheck.objects.filter(pay_date__gt=paycheck.pay_date)
            total_due = 0
            if future_paychecks:
                future_paychecks = future_paychecks.order_by("pay_date")
                next_paycheck = future_paychecks.first()
                bills = Bill.objects(payer = current_user, due_date__gte=paycheck.pay_date, due_date__lte=next_paycheck.pay_date)
                for bill in bills: total_due += bill.amount
                return render_template("get_paycheck.html", paycheck = paycheck, bills = bills, total_due = total_due)
            else:
                bills = Bill.objects(payer = current_user, due_date__gte=paycheck.pay_date)
                for bill in bills: total_due += bill.amount
                return render_template("get_paycheck.html", paycheck = paycheck, bills = bills, total_due = total_due)
    else:
        return "That doesn't exist."


