from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin # UserMixin - help manage user sessions


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# represent SQLAlchemy database structure as classes called models
# each class is a table in the database
class Users(db.Model, UserMixin):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20),  unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    transactions = db.relationship('Transaction', backref='phone', lazy=True)
    budgets = db.relationship('Budget', backref='phone', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}', '{self.role}', '{self.date}')"

    # def __init__(self, name, email, phone, role, password, date):
    #     self.name = name
    #     self.email = email
    #     self.phone = phone
    #     self.role = role
    #     self.password = password
    #     self.date = date

class Transaction(db.Model):
    __tablename__ = 'transactions_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.String(30), unique=True, nullable=False)
    # phone_no = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(20), nullable=False)
    merchant_req_id = db.Column(db.String(40),nullable=True)
    mpesa_ref = db.Column(db.String(20),nullable=True)

    def __repr__(self):
        return f"Transaction('{self.transaction_id}', '{self.amount}', '{self.created_at}', '{self.status}', '{self.merchant_req_id}', '{self.mpesa_ref}')"

    # def __init__(self, transaction_id, phone_no, amount, created_at, status, merchant_req_id, mpesa_ref):
    #     self.transaction_id = transaction_id
    #     self.phone_no = phone_no
    #     self.amount = amount
    #     self.created_at = created_at
    #     self.status = status
    #     self.merchant_req_id = merchant_req_id
    #     self.mpesa_ref = mpesa_ref

class Budget(db.Model):
    __tablename__ = 'budgets_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    approved_by = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    
    def __repr__(self):
        return f"Budget('{self.amount}', '{self.purpose}', '{self.status}', '{self.budget_id}', '{self.approved_by}')"

    # def __init__(self, transaction_id, phone_no, amount, created_at, status, merchant_req_id, mpesa_ref):
    #     self.transaction_id = transaction_id
    #     self.phone_no = phone_no
    #     self.amount = amount
    #     self.created_at = created_at
    #     self.status = status
    #     self.merchant_req_id = merchant_req_id
    #     self.mpesa_ref = mpesa_ref


class Payment(db.Model):
    __tablename__ = 'payments_table'
    id = db.Column(db.Integer, primary_key=True)
    result_code = db.Column(db.Integer)
    phone_no = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    mpesa_ref = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True))
    merchant_req_id = db.Column(db.String(40),nullable=True)
    
    def __repr__(self):
        return f"Transaction('{self.result_code}', '{self.phone_no}', '{self.amount}', '{self.mpesa_ref}', '{self.created_at}', '{self.merchant_req_id}')"

    # def __init__(self, result_code, phone_no, amount, mpesa_ref, created_at, merchant_req_id):
    #     self.result_code = result_code
    #     self.phone_no = phone_no
    #     self.amount = amount
    #     self.mpesa_ref = mpesa_ref
    #     self.created_at = created_at
    #     self.merchant_req_id = merchant_req_id
