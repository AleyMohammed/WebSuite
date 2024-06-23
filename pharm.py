import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

cnx = mysql.connector.connect(
    user='root', password='قخخف123456789', host='localhost', database='pharm')
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
  background-image: url('https://c4.wallpaperflare.com/wallpaper/335/936/967/antibiotic-capsules-close-up-cure-wallpaper-preview.jpg');
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

    <h1>Pharmacy</h1>
    <form>
      <div class="form-group">
        <label for="Productname">Product Name:</label>
        <input type="text" class="form-control" id="Productname" name="Productname" placeholder="Enter your Product name">
      </div>
      <div class="form-group">
        <label for="Productcode">Product code:</label>
        <input type="text" class="form-control" id="Productcode" name="Productcode" placeholder="Enter Product code">
      </div>
      <div class="form-group">
        <label for="Producttype">Product type:</label>
        <input type="text" class="form-control" id="Producttype" name="Producttype" placeholder="Enter Product type">
      </div>
      <div class="form-group">
        <label for="Medain">Meda in:</label>
        <input type="text" class="form-control" id="Medain" name="Medain" placeholder="Meda in">
      </div>
      <div class="form-group">
        <label for="alert">Alert:</label>
        <input type="text" class="form-control" id="alert" name="alert" placeholder="  ">
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
        Productname = form_data['Productname'][0]
        Productcode = form_data['Productcode'][0]  # Corrected spelling
        Producttype = form_data['Producttype'][0]
        Medain = form_data['Medain'][0]
        alert = form_data['alert'][0]
        action = form_data['action'][0]

        # Insert the data into the database
        if action == 'insert':
            query = "INSERT INTO pharmasy (Productname, Productcode, Producttype, Medain, alert) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (Productname, Productcode, Producttype, Medain, alert))
            message = 'Record inserted successfully!'
        elif action == 'delete':
            query = "DELETE FROM pharmasy WHERE Productcode = %s"
            cursor.execute(query, (Productcode,))
            message = 'Record deleted successfully!'
        elif action == 'update':
            query = "UPDATE pharmasy SET Productname = %s, Producttype = %s, Medain = %s, alert = %s WHERE Productcode = %s"
            cursor.execute(query, (Productname, Producttype, Medain, alert, Productcode))
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