import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json


# Create a connection to MySQL
cnx = mysql.connector.connect(
    user='root', password='قخخف123456789', host='localhost', database='DeltaUni')
cursor = cnx.cursor()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Write HTML code to display the form
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
<style>
body {
  background-image: url('https://new.deltauniv.edu.eg/Uploads/1c2077cb-7fee-4ea3-adb9-dde34c0bdb38_55.jpg');
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

    <h1>DeltaUni</h1>
    <form>
      <div class="form-group">
        <label for="StudentID">StudentID:</label>
        <input type="number" class="form-control" id="StudentID" name="StudentID" placeholder="Student ID">
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
        <label for="Address">Address:</label>
        <input type="text" class="form-control" id="Address" name="Address" placeholder="  ">
      </div>
      <div class="form-group">
        <label for="Phone">Phone:</label>
        <input type="text" class="form-control" id="Phone" name="Phone" placeholder="  ">
      </div>
      <div class="form-group">
        <label for="DateOfBirth">DateOfBirth:</label>
        <input type="date" class="form-control" id="DateOfBirth" name="DateOfBirth" placeholder="  ">
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

    def do_POST(self):
        # Get the form data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        form_data = parse_qs(post_data)

        StudentID = form_data['StudentID'][0]
        FirstName = form_data['FirstName'][0]  # Corrected spelling
        LastName = form_data['LastName'][0]
        Email = form_data['Email'][0]
        Address = form_data['Address'][0]
        Phone = form_data['Phone'][0]
        DateOfBirth = form_data['DateOfBirth'][0]
        action = form_data['action'][0]

        if action == 'insert':
            query = "INSERT INTO students (StudentID, FirstName, LastName, Email, Address, Phone, DateOfBirth) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (StudentID, FirstName, LastName, Email, Address, Phone, DateOfBirth))
            message = 'Record inserted successfully!'
        elif action == 'delete':
            query = "DELETE FROM students WHERE StudentID = %s"
            cursor.execute(query, (StudentID,))
            message = 'Record deleted successfully!'
        elif action == 'update':
            query = "UPDATE students SET FirstName = %s, LastName = %s, Email = %s, Address = %s, Phone = %s, DateOfBirth= %s WHERE StudentID = %s"
            cursor.execute(query, ( FirstName, LastName, Email, Address, Phone, DateOfBirth, StudentID))
            message = 'Record updated successfully!'
        else:
            message = 'Invalid action.'

        cnx.commit()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': message}).encode())


def run():
    httpd = HTTPServer(('localhost', 8080), MyHandler)
    print('Server started on http://localhost:8080')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
