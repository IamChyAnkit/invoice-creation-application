from shop import app
from flask import render_template, request, url_for, redirect
from shop.modles import Customer,Invoice,Itemlist, Stock, InvoiceSummery
from shop import db
from datetime import datetime



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


        


@app.route('/', methods=('GET', 'POST'))
def customer_details():
   
    if request.method=="POST":
    
        firstname=request.form.get("firstname")
        lastname = request.form.get('lastname')
        userid = request.form.get('userid')
        userid = request.form.get('userid')
        phone_no = int(request.form.get('phone_no'))
        state = request.form.get('state')
        district= request.form.get('district')
        
        customer = Customer(
                        firstname=firstname,
                        lastname=lastname,
                        userid=userid,
                        phone_no=phone_no,
                        state=state,
                        district=district,
                       
                        )
        db.session.add(customer)
        db.session.commit()        
        return redirect(url_for('invoice'))
    else:
        return render_template('customer.html')
    
@app.route('/invoice',methods=('GET', 'POST'))
def invoice():
    if request.method=="POST":
        date = request.form.get('date')
        userid = request.form.get('userid')
        invoice= Invoice(
                
                            date=datetime.now().date(),
                            userid=userid
            )   
        db.session.add(invoice)
        db.session.commit()
        invoice = Invoice.query.order_by(Invoice.invoice_no.desc()).first()
        print(invoice.invoice_no)
        return redirect(url_for('sale'))
    else:
        return render_template('invoice.html')


@app.route('/sale', methods=('GET', 'POST'))
def sale():

  
    
    if request.method=="POST":
        
        item_name = request.form.get('item_name')
        qty_per_unit = float(request.form.get('qty_per_unit'))
        item_name = item_name.strip()
        item_name = item_name.capitalize()
        item_details = Stock.query.filter_by(item_name=item_name).first()
        updated = item_details.qty_per_unit-qty_per_unit

        price_per_unit = item_details.sp_per_unit
        discount = item_details.discount_per_unit
        tax_rate = item_details.tax_rate
        net_price = price_per_unit-discount
        ammount=net_price*qty_per_unit
        tax = (ammount*tax_rate)/100
        total = ammount+tax


        invoice = Invoice.query.order_by(Invoice.invoice_no.desc()).first()
        
        itemlist = Itemlist(
                           
                            invoice_no=invoice.invoice_no,
                            item_name=item_name,
                            qty_per_unit=qty_per_unit,
                            price_per_unit=price_per_unit,
                            tax=tax,
                            discount=discount,
                            net_price=net_price,
                            total=total
        )
        db.session.add(itemlist)
        db.session.commit()
        item_details = Stock.query.filter_by(item_name=item_name).first()
        if updated==0.0:
            db.session.delete(item_details)
            db.session.commit()
        else:
            item_details.qty_per_unit = updated
            db.session.add(item_details)
            db.session.commit()
        invoice = Invoice.query.order_by(Invoice.invoice_no.desc()).first()
        if request.form['button'] == 'product':
            
            return redirect(url_for('sale'))
            

        elif request.form['button'] == 'summery':
            return redirect(url_for('summery',invoice_no=invoice.invoice_no))
    else:
        return render_template('itemlist.html')


@app.route('/summery/<invoice_no>/')
def summery(invoice_no):
    items = Itemlist.query.filter_by(invoice_no=int(invoice_no))
    total_price =0
    total_qty = 0
    total_discount =0
    total_net_price =0
    total=0
    total_tax =0
    for item in items:
        total_qty += item.qty_per_unit
        total_price += item.price_per_unit
        total_discount += item.discount
        total_net_price += item.net_price
        total += item.total 
        total_tax += item.tax
    invoice = Invoice.query.filter_by(invoice_no=int(invoice_no)).first()
    customer = Customer.query.filter_by(userid=invoice.userid).first()
    
    if customer.state=='Bihar':
        Igst = True
    else:
        Igst = False

    # summery  =InvoiceSummery(
    #             subtotal = total,
    #             total_gst = total_tax,
    #             amount = total,
    #             igst = Igst,
    #             invoice_no = invoice.invoice_no
                
                

    # )
    # db.session.add(summery)
    # db.session.commit()

    return render_template('summery.html',total_discount=total_discount,total_net_price=total_net_price,total_tax=total_tax,total=total )

@app.route('/editproductdetails/<item_name>/', methods=('GET', 'POST'))
def editproductdetails(item_name):
    if request.method=="POST":
        item_name = item_name.strip()
        item_name = item_name.capitalize()
        item = Stock.query.filter_by(item_name=item_name).first()
        print(item)
        item_name = request.form.get('item_name')
        qty_per_unit = float(request.form.get('qty_per_unit'))
        cp_per_unit = float(request.form.get('cp_per_unit'))
        sp_per_unit = float(request.form.get('sp_per_unit'))
        discount_per_unit = float(request.form.get('discount_per_unit'))
        tax_rate = float(request.form.get('tax_rate'))
        item_name = item_name.strip()
        item_name = item_name.capitalize()
        item.item_name = item_name
        item.qty_per_unit=qty_per_unit
        item.cp_per_unit=cp_per_unit
        item.sp_per_unit=sp_per_unit
        item.discount_per_unit=discount_per_unit
        item.tax_rate=tax_rate
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('purchase'))
    else:
        return render_template('stockitemlist.html')

@app.route('/admin')
def layout():
    return render_template('admin/itemstock')
@app.route('/itemstock', methods=('GET', 'POST'))
def purchase():
    if request.method=="POST":
    
        item_name = request.form.get('item_name')
        qty_per_unit = float(request.form.get('qty_per_unit'))
        cp_per_unit = float(request.form.get('cp_per_unit'))
        sp_per_unit = float(request.form.get('sp_per_unit'))
        discount_per_unit = float(request.form.get('discount_per_unit'))
        tax_rate = float(request.form.get('tax_rate'))
        item_name = item_name.strip()
        item_name = item_name.capitalize()
        

        saleitemlist =Stock(
                            item_name=item_name,
                            qty_per_unit=qty_per_unit,
                            cp_per_unit=cp_per_unit,
                            sp_per_unit=sp_per_unit,
                            discount_per_unit=discount_per_unit,
                            tax_rate=tax_rate,
                            
                           
        )
        
        db.session.add(saleitemlist)
        db.session.commit()
        
   
        return redirect(url_for('purchase'))
    else:
        return render_template('stockitemlist.html')


if __name__ == "__main__":
    app.run(debug=True)
