 # الجزء الأول: الاتصال بقاعدة البيانات MySQL

import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json  #  لتشفير وفك تشفير البيانات إلى ومن صيغة JSON.

cnx = mysql.connector.connect(
    user='root', password='قخخف123456789', host='localhost', database='bank')  # Changed host to 'localhost'
cursor = cnx.cursor()
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):   #  هدف منها اجيب حاجه من سيرفر لل broeser
        self.send_response(200)        # سيرفر بيرد بحاله اوكى
        self.send_header('Content-type', 'text/html')   # نوع المحتوى فى رساله جيت هو
        self.end_headers()

        # Write HTML code to display the form
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
<style>
body {
  background-image: url('https://cdn-res.keymedia.com/cms/images/ca/155/0379_638158050789922982.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed; 
  background-size: cover;
}
</style>
  <meta charset="UTF-8">
  <title>Pharmacy</title>
  <!-- Bootstrap CSS -->

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"
   integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">

</head>
<body>
  <div class="container">
      <form action="/" method="post">

    <h1>Bank</h1>
    <form>
      <div class="form-group">
        <label for="CustomerID">Customer ID:</label>
        <input type="number" class="form-control" id="CustomerID" name="CustomerID" placeholder="Customer ID">
      </div>
      <div class="form-group">
        <label for="FirstName">First Name:</label>
        <input type="text" class="form-control" id="FirstName" name="FirstName" placeholder="Enter FirstName">
      </div>
      <div class="form-group">
        <label for="LastName">Last Name:</label>
        <input type="text" class="form-control" id="LastName" name="LastName" placeholder="Enter LastName">
      </div>
      <div class="form-group">
        <label for="Email"> Email:</label>
        <input type="text" class="form-control" id="Email" name="Email" placeholder=" ">
      </div>
      <div class="form-group">
        <label for="Phone">Phone:</label>
        <input type="text" class="form-control" id="Phone" name="Phone" placeholder="  ">
      </div>
      <div class="form-group">
        <label for="Address">Address:</label>
        <input type="text" class="form-control" id="Address" name="Address" placeholder="  ">
      </div>
          Action: 
                <select name="action">
                    <option value="insert">Insert</option>
                    <option value="delete">Delete</option>
                    <option value="update">Update</option>
                </select>
                <input type="hidden" name="action" value="insert">
               <button type="submit" class="btn btn-primary">Submit</button>
               
    </form>
  </div>

  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
   integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>

<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" 
integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" 
integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>

</body>
</html>'''

        # Send the HTML code to the client
        self.wfile.write(bytes(html, 'utf-8'))
        return

    def do_POST(self): # بيرسل معلومه من browser للسيرفر
        # Get the form data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # سيرفر read
        post_data = post_data.decode('utf-8') # هيفك تشفير بيانات اللى جايه
        form_data = parse_qs(post_data) # ب تحليل البيانات إلى قاموس (ديكشنري).

        CustomerID = form_data['CustomerID'][0]
        FirstName = form_data['FirstName'][0]  # Corrected spelling
        LastName = form_data['LastName'][0]
        Email = form_data['Email'][0]
        Phone = form_data['Phone'][0]
        Address = form_data['Address'][0]
        action = form_data['action'][0]

        if action == 'insert':
            query = "INSERT INTO customers (CustomerID, FirstName, LastName, Email, Phone, Address) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (CustomerID, FirstName, LastName, Email, Phone, Address))
            message = 'Record inserted successfully!'
        elif action == 'delete':
            query = "DELETE FROM customers WHERE CustomerID = %s"
            cursor.execute(query, (CustomerID,))
            message = 'Record deleted successfully!'
        elif action == 'update':
            query = "UPDATE customers SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, Address = %s  WHERE CustomerID = %s"
            cursor.execute(query, (FirstName, LastName, Email, Phone, Address, CustomerID))
            message = 'Record updated successfully!'
        else:
            message = 'Invalid action.'
      #  إرسال الرد :
        cnx.commit()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': message}).encode())  # إرسال الرسالة إلى العميل بصيغة JSON.


def run():
    httpd = HTTPServer(('localhost', 8080), MyHandler)
    print('Server started on http://localhost:8080')
    httpd.serve_forever()


if __name__ == '__main__':
    run()


