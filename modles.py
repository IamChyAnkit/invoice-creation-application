from shop import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(15))
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    logged_in = db.Column(db.TIMESTAMP, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
class Customer(db.Model):
    __table_args__ = {'extend_existing': True}
    
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    userid = db.Column(db.String(15),primary_key=True)
    phone_no = db.Column(db.String(12), nullable=False, unique=True)
    state = db.Column(db.String(25),nullable=False)
    district = db.Column(db.String(30),nullable=False)
    invoices = db.relationship('Invoice',cascade='all,delete',backref ='customer',lazy=True)
    def __repr__(self):
        return f'<Customer {self.firstname}>' 

class Itemlist(db.Model):
    __table_args__ = {'extend_existing': True}
   
    s_id =db.Column(db.Integer,primary_key =True)
    item_name = db.Column(db.String(50),db.ForeignKey('stock.item_name'),nullable=False)
    qty_per_unit = db.Column(db.Float(),nullable = False)       
    price_per_unit = db.Column(db.Float(),nullable = False)
    discount=db.Column(db.Float(),nullable = False)
    net_price = db.Column(db.Float(),nullable = False)    
    tax = db.Column(db.Float(),nullable = False)
    total = db.Column(db.Float(),nullable = False)
    invoice_no = db.Column(db.Integer, db.ForeignKey('invoice.invoice_no'),primary_key = True)

    def __repr__(self):
        return f'<Itemlist {self.item_name}>'


class Stock(db.Model):
    __table_args__ = {'extend_existing': True}
   
    s_id =db.Column(db.Integer,primary_key =True)
    item_name = db.Column(db.String(50),nullable = False)
    qty_per_unit = db.Column(db.Float(),nullable = False)
    cp_per_unit = db.Column(db.Float(),nullable = False)
    sp_per_unit = db.Column(db.Float(),nullable = False)
    discount_per_unit = db.Column(db.Float(),default=0)
    tax_rate = db.Column(db.Float(),nullable = False)
    itemlists = db.relationship('Itemlist',cascade='all,delete',backref ='stock',lazy=True)
    def __repr__(self):
        return f'<Stock {self.item_name}>'

class Invoice(db.Model):
    __table_args__ = {'extend_existing': True}
    invoice_no = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.TIMESTAMP, default=datetime.now().date())
    userid = db.Column(db.String(15),db.ForeignKey('customer.userid'))
    itemlists = db.relationship('Itemlist',cascade='all,delete',backref ='invoice',lazy=True)
    invoice_summeries = db.relationship('InvoiceSummery',cascade='all,delete',backref ='invoice',lazy=True)
    def __repr__(self):
        return f'<Invoice {self.userid}>'

class InvoiceSummery(db.Model):
    __table_args__ = {'extend_existing': True}
    invoice_no =db.Column(db.Integer,primary_key =True)
    subtotal = db.Column(db.Float(), nullable=False)
    total_gst = db.Column(db.Float(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    igst = db.Column(db.Boolean)

    invoice_no = db.Column(db.Integer, db.ForeignKey('invoice.invoice_no'),primary_key = True)


    def __repr__(self):
        return f'<InvoiceSummery {self.invoice_no}>'


db.create_all()
db.session.commit()