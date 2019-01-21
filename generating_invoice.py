import requests
import json
import csv
class Invoice:
    def __init__(self, url,token, secret, DEBUG=False):
        self.url = url
        self.token = token
        self.secret = secret
        self.DEBUG = DEBUG
    def send_request(self):

        try:
            r = requests.get(
                url=self.url,
                headers = {
                    "Access-Token":self.token,
                    "Client-Secret":self.secret,
                    "Content-Type":"application/json",
                    "Accept":"application/json",
                },
            )

            if r.status_code is 200:
                data = r.content
                json_data =json.loads(data.decode('utf-8'))
                print(('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code)))
                print(('Response HTTP Response Body : {content}'.format(content=r.content)))
                return json_data['Invoices']
            else:
                return "something went wrong"
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

    def retrieveInvoice(self):
        try:
            list_obj = []
            for c in range(1,2156):

                url = self.url + str(c)

                r = requests.get(
                    url=url,
                    headers={
                        "Access-Token": self.token,
                        "Client-Secret": self.secret,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                )

                if r.status_code is 200:
                    data = r.content
                    json_data =json.loads(data.decode('utf-8'))
                    for i ,j in json_data.items(): #Invoice ID, Amount,Name, Date, Country, charge_id (Your reference)
                        print({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country'],'charge_id/unique_id':j['YourReference']})
                        list_obj.append({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country'],'charge_id/unique_id':j['YourReference']})

            print(list_obj)
            file_path = 'C:\\program_test\\Final_invoice\\allinvoices.csv'
            csv_columns = ['invoice_id', 'amount', 'name', 'Date', 'country', 'charge_id/unique_id']
            with open(file_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in list_obj:
                    writer.writerow(data)
            return file_path
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')


    def duplicateInvoice(self):
        try:
            list_obj = []
            duplicates_total_amount = []
            for c in range(1,2156):

                url = self.url + str(c)

                r = requests.get(
                    url=url,
                    headers={
                        "Access-Token": self.token,
                        "Client-Secret": self.secret,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                )

                if r.status_code is 200:
                    data = r.content
                    json_data =json.loads(data.decode('utf-8'))
                    check_list = []
                    for i ,j in json_data.items(): #Invoice ID, Amount,Name, Date, Country, charge_id (Your reference)
                        if j['YourReference']+"/"+j['Comments'] not in check_list:
                            print(j['YourReference']+"/"+j['Comments'])
                            check_list.append(j['YourReference']+"/"+j['Comments'])
                        else:
                            duplicates_total_amount.append(int(j['Total']))
                            print({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country'],'transaction_id':j['YourReference']+"/"+j['Comments']})
                            list_obj.append({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country'],'transaction_id':j['YourReference']+"/"+j['Comments']})

            print(list_obj)
            file_path = 'C:\\program_test\\Final_invoice\\duplicateinvoices.csv'
            csv_columns = ['invoice_id', 'amount', 'name', 'Date', 'country', 'transaction_id']
            with open(file_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in list_obj:
                    writer.writerow(data)
            return file_path,sum(duplicates_total_amount)
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

class CreditInvoice:
    def __init__(self, url,token, secret,Start_InvoiceID,End_InvoiceID):
        self.url = url
        self.token = token
        self.secret = secret
        self.Start_InvoiceID= Start_InvoiceID
        self.End_InvoiceID = End_InvoiceID
    def CreditInvoicefn(self):
        for c in range(self.Start_InvoiceID, self.End_InvoiceID):
            print(c)
            url = self.url+ '/' + str(c) + '/credit'
            headers = {
                "Access-Token":  self.token,
                "Client-Secret": self.secret,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            try:
                r = requests.put(
                    url=url,
                    headers=headers,
                )
                if r.status_code is 200:
                        list_obj = []
                        data = r.content
                        json_data =json.loads(data.decode('utf-8'))
                        print(json_data)
                        for i ,j in json_data.items(): #Invoice ID, Amount,Name, Date, Country, charge_id (Your reference)
                            if  int(j['Total']) < 0:
                                print(j['Total'])
                                j['Total'] = 0
                                print({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country']})
                                list_obj.append({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country']})
                            else:
                                print({"invoice_id": j['DocumentNumber'], 'amount': j['Total'], 'name': j['CustomerName'],
                                       'Date': j['InvoiceDate'], 'country': j['Country']})
                                list_obj.append(
                                    {"invoice_id": j['DocumentNumber'], 'amount': j['Total'], 'name': j['CustomerName'],
                                     'Date': j['InvoiceDate'], 'country': j['Country']})

                        print(list_obj)
                        return list_obj
                else:
                    print(r.status_code)
            except requests.exceptions.RequestException as e:
                print('HTTP Request failed')

        # try:
        #
        #     duplicates_total_amount = []
        #     for c in range(self.Start_InvoiceID,self.End_InvoiceID):
        #         url = self.url+'/'+str(c)+'/credit'
        #         r = requests.put(
        #             url=url,
        #             headers={
        #                 "Access-Token": self.token,#bec4464e-b2f9-4615-b4a7-2835f8abff69
        #                 "Client-Secret": self.secret, #Q9br54ai9V
        #                 "Content-Type": "application/json",
        #                 "Accept": "application/json",
        #             },
        #         )
        #         print(r.content)
        #
        #         if r.status_code is 200:
        #             list_obj = []
        #             data = r.content
        #             json_data =json.loads(data.decode('utf-8'))
        #             print(json_data)
        #             for i ,j in json_data.items(): #Invoice ID, Amount,Name, Date, Country, charge_id (Your reference)
        #                 if  int(j['Total']) < 0:
        #                     print(j['Total'])
        #                     j['Total'] = 0
        #                     print({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country']})
        #                     list_obj.append({"invoice_id":j['DocumentNumber'],'amount':j['Total'],'name':j['CustomerName'],'Date':j['InvoiceDate'],'country':j['Country']})
        #                 else:
        #                     print({"invoice_id": j['DocumentNumber'], 'amount': j['Total'], 'name': j['CustomerName'],
        #                            'Date': j['InvoiceDate'], 'country': j['Country']})
        #                     list_obj.append(
        #                         {"invoice_id": j['DocumentNumber'], 'amount': j['Total'], 'name': j['CustomerName'],
        #                          'Date': j['InvoiceDate'], 'country': j['Country']})
        #
        #             print(list_obj)
        #             return list_obj
        #         else:
        #             return r.status_code
        # except requests.exceptions.RequestException as e:
        #     print('HTTP Request failed')




