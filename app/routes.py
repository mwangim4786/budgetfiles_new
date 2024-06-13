from flask import render_template, request, url_for, flash, redirect, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BudgetForm, UpdateUserForm
from app.models import Users, Budget, Payment, Transaction
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import uuid


transactions_table_content = {
    "1": {
        "trans_No": "QSILKA3L7DX",
        "budget_Id": "bgt-001",
        "user": "Martin Kihungi",
        "date": "20-05-2024",
        "status": "Paid",
        "amount": "150",
        "description": "Shipping"
        },
    "2": {
        "trans_No": "QSI4XGH86FH",
        "budget_Id": "bgt-001",
        "user": "Martin Kihungi",
        "date": "20-05-2024",
        "status": "Paid",
        "amount": "200",
        "description": "Stationery"
        }
    }

approvals_table_content = {
    "1": {
        "request_id": "bgt-003",
        "user": "Martin Kihungi",
        "date": "25-05-2024",
        "status": "Pending",
        "amount": "150"
        },
    "2": {
        "request_id": "bgt-003",
        "user": "Martin Kihungi",
        "date": "25-05-2024",
        "status": "Pending",
        "amount": "150"
        }
    }



# def create_db():
#     with app.app_context():
#         db.create_all()


@app.route('/home')
@login_required
def home():
    return render_template('home.html', page='home',)
# ------------------------------------------------------------------------------- #
@app.route('/register', methods=['POST', 'GET'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date_val = form.date.data
        date_value = datetime.strptime(date_val, "%Y-%m-%d")
        user = Users(name=form.name.data, email=form.email.data, phone=form.phone.data, role=form.role.data, password=hashed_pw, date=date_value)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('users'))
    return render_template('register.html', page='register', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(phone=form.phone.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # if form.phone.data == '0712345678' and form.password.data == 'password':
            #     flash(f'You have been logged in!', 'success')
            #     return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccesseful. Check your details!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account/<user_id>')
@login_required
def account(user_id):
    user = Users.query.get_or_404(user_id)
    # if user.phone != current_user:
    #     abort(403)
    return render_template('account.html', page='account', title='Account', user=user)


@app.route('/budgets')
@login_required
def budgets():
    budgets = Budget.query.all()
    return render_template('budgets.html', page='budgets', title='Budgets', budgets=budgets)


@app.route('/approvals')
@login_required
def approvals():
    budgets = Budget.query.all()
    return render_template('approvals.html', page='approvals', title='Approvals', budgets=budgets)


@app.route('/new_budget/new', methods=['POST', 'GET'])
@login_required
def create_budget():
    form = BudgetForm()
    bdgt_id = str(uuid.uuid4())
    if form.validate_on_submit():
        budget = Budget(budget_id=bdgt_id, amount=form.amount.data, purpose=form.purpose.data, phone=current_user)
        db.session.add(budget)
        db.session.commit()
        flash('Your budget has been created. Await Approval!', 'success')
        return redirect(url_for('budgets'))
    return render_template('create_budget.html', page='budgets', title='Create New Budget',
                           form=form, legend='New Budget')
    



@app.route("/budget/<int:budget_id>/update", methods=['POST', 'GET'])
def budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.phone != current_user:
        abort(403)
    form = BudgetForm()
    if form.validate_on_submit():
        budget.amount = form.amount.data
        budget.purpose = form.purpose.data
        db.session.commit()
        flash('Your budget has been Updated!', 'success')
        return redirect(url_for('budgets'))
    elif request.method == 'GET':
        form.amount.data = budget.amount
        form.purpose.data = budget.purpose
    return render_template('create_budget.html', page='budgets', title='Update Budget',  ad_class = 'disabled', form=form, del_id=budget.id, phone=budget.phone, legend='Update Budget',
                           delete_bdgt='<a role="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal">Delete Budget</a>')



@app.route("/user/<int:user_id>/update", methods=['POST', 'GET'])
def user(user_id):
    user = Users.query.get_or_404(user_id)
    
    form = UpdateUserForm()
    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date_val = form.date.data
        date_value = datetime.strptime(date_val, "%Y-%m-%d")

        user.name = form.name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.role = form.role.data
        if user == current_user:
            user.password = hashed_pw

        user.date = date_value

        db.session.commit()
        flash('User has been Updated!', 'success')
        return redirect(url_for('account', user_id=user.id))
    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.role.data = user.role
        form.id.data = user.id
        form.date.data = user.date.strftime('%Y-%m-%d')
    return render_template('register.html', page='users', title='Update user', form=form, del_id=user.id, user=user, legend='Update user')


@app.route("/budget/<int:budget_id>/delete", methods=['POST'])
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.phone != current_user:
        abort(403)
    db.session.delete(budget)
    db.session.commit()
    flash('Your budget has been Deleted!', 'success')
    return redirect(url_for('budgets'))


@app.route("/user/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    if current_user.role != 'Admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User has been Deleted!', 'success')
    return redirect(url_for('users'))


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
# ------------------------------------------------------------------------------- #

# @app.route('/create')
# def create_all():
#     # return 'Hello World!'
#     create_db()

#     return 'ok'


@app.route('/transactions')
@login_required
def transactions():
    # return 'Hello World!'

    return render_template('transactions.html', page='transactions', data=transactions_table_content)


# @app.route('/approvals', methods=['POST', 'GET'])
# @login_required
# def approvals():
#     return render_template('approvals.html', page='approvals', data=approvals_table_content)


# @app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def users():
#     if request.method == 'GET':
#         users = Users.query.all()
#         return render_template('users.html', users=users)
#     elif request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = "254"+request.form['phone']
#         role = request.form['role']
#         password = request.form['password']
#         date = datetime.today().strftime('%d-%m-%Y')

#         if name == '' or email == '' or phone == '' or role == '' or password == '':
#             return render_template('users.html', message='Please enter required fields.') 
        
#         data = Users(name, email, phone, role, password, date)
#         db.session.add(data)
#         db.session.commit()
#         return render_template('users.html', message='User added successfully.')
        # return redirect("/users")



@app.route("/users")
def users():
    users = Users.query.all()
    return render_template('users.html', page='users', users=users)


# @app.route('/users/<user_id>', methods=['PUT'])
# def edit_user(user_id):
#     user_id = request.form['edit_user_id']
#     data = Users.query.filter_by(id==id).first()
#     data = Users(name, email, phone, role, password, date)
#     db.session.add(data)
#     db.session.commit()

# @app.route('/submit', methods=['POST', 'GET'])
# def submit_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         role = request.form['role']
#         password = request.form['password']
#         date = datetime.today().strftime('%d-%m-%Y')

#         if name == '' or email == '' or phone == '' or role == '' or password == '':
#             return render_template('users.html', message='Please enter required fields.') 
        
#         data = Users(name, email, phone, role, password, date)
#         db.session.add(data)
#         db.session.commit()
#         # return render_template('success.html')
#         return render_template('users.html', message='User added successfully.')
#         # return redirect("/users")
#     elif request.method == 'GET':
#         users = Users.query.all()
#         return render_template('users.html', users=users)



# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         customer = request.form['customer']
#         dealer = request.form['dealer']
#         rating = request.form['rating']
#         comments = request.form['comments']
#         # print(customer, dealer, rating, comments)
#         if customer == '' or dealer == '':
#             return render_template('index.html', message='Please enter required fields.') 
#         if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
#             data = Feedback(customer, dealer, rating, comments)
#             db.session.add(data)
#             db.session.commit()
#             return render_template('success.html')
#         return render_template('index.html', message='Hello '+customer+', you have already submitted feedback.')
    
