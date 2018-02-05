from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Import CRUD operations from lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2><input name="message" type="text" >
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2><input name="message" type="text" >
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<a href='/restaurants/new'>Click here to add a new restaurant</a><br><br>"
                output += "<html><body>"
                output += ""
                output += "<h1>List of Restaurants</h1><ul>"
                ListOfRestaurants = session.query(Restaurant).all()
                for restaurant in ListOfRestaurants:
                    output += "<li>%s</li>" % restaurant.name
                    output += '''<a href="/restaurants/%s/edit">EDIT</a><br>
                        <a href="/restaurants/%s/delete">DELETE</a>''' % (restaurant.id, restaurant.id)
                output += "</ul></body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                    <h3>Please input the new restaurant name below</h3>
                    <input name="newRestaurantName" type="text" placeholder = "type it here mate">
                    <input type="submit" value="Add Restaurant">
                    </form>'''
                output += "</ul></body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDpath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>%s</h1>" % myRestaurantQuery.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>
                        <h3>Change the restaurant name here</h3>
                        <input name="newRestaurantName" type="text" placeholder = "%s">
                        <input type="submit" value="Change Name">
                        </form>''' % (restaurantIDpath, myRestaurantQuery.name)
                    output += "</ul></body></html>"
                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith("/delete"):
                restaurantIDpath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDpath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>%s</h1>" % myRestaurantQuery.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>
                        <h3>Are you sure you want to delete %s ?</h3>
                        <input type="submit" value="delete">
                        </form>''' % (restaurantIDpath, myRestaurantQuery.name)
                    output += "</ul></body></html>"
                    self.wfile.write(output)
                    print output
                    return

            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith("delete"):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                
                # Change Restaurant name
                restaurantIDpath = self.path.split("/")[2]
                RestaurantToDelete = session.query(Restaurant).filter_by(id = restaurantIDpath).one()
                if RestaurantToDelete != []: 
                    session.delete(RestaurantToDelete)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


        if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant Object
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Change Restaurant name
                restaurantIDpath = self.path.split("/")[2]
                RestaurantToRename = session.query(Restaurant).filter_by(id = restaurantIDpath).one()
                if RestaurantToRename != []:
                    RestaurantToRename.name = messagecontent[0]
                    session.add(RestaurantToRename)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
