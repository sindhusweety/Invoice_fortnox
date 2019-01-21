from flask import Flask,request
from flask import jsonify
from generating_invoice import Invoice
from generating_invoice import CreditInvoice


app = Flask(__name__)
print(app)

@app.route('/allInvoices',methods=['POST'])
def AllInvoice():
    url = request.json['url']
    access_token =request.json['access_token']
    client_secret = request.json['client_secret']
    obj_invoice = Invoice(url,access_token,client_secret)
    # json_data = obj_invoice.send_request()
    # print(len(json_data))
    file_path = obj_invoice.retrieveInvoice()
    return jsonify({"status":"success","filepath":file_path})

#GET ALL DUPLICATES WHERE YOUR REFERENCE/COMMENTS ARE SAME AND SUM OF AMOUNT
@app.route('/getDuplicates',methods=['POST'])
def getDuplicateInvoices():
    url = request.json['url']
    access_token = request.json['access_token']
    client_secret = request.json['client_secret']
    obj_invoice = Invoice(url, access_token, client_secret)
    file_path,total_duplicate_amount = obj_invoice.duplicateInvoice()
    return jsonify({"status": "success",'filepath':file_path,'sum_amount':total_duplicate_amount})
#CREATE NULLIFIES (CREDIT INVOICES)
@app.route('/creditNullifies/<int:start>/<int:end>',methods=['POST'])
def NulCreditInvoices(start,end):
    url = request.json['url']
    access_token = request.json['access_token']
    client_secret = request.json['client_secret']
    obj_invoice = CreditInvoice(url, access_token, client_secret,start,end)
    obj_data = obj_invoice.CreditInvoicefn()
    return jsonify({"status": "success"})





if __name__ == '__main__':
    app.run()