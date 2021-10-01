import dbcreds
import mariadb
from flask import Flask, request, Response
import json

conn = None
cursor = None

try:
    conn = mariadb.connect(
                        user=dbcreds.user,
                        password=dbcreds.password,
                        host=dbcreds.host, 
                        port=dbcreds.port,
                        database=dbcreds.database,
                        )
    cursor = conn.cursor()

    #instantiate Flask object
    app = Flask(__name__)
    
    @app.route('/')
    def homepage():
        return "<h1>Hello World</h1>"

    animal_list = [
                {'animal': "snake"},
                {'animal': "giraffe"},
                {'animal': "tiger"}
            ]
    @app.route('/animals', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def animals():
        if (request.method == 'GET'):
            args = request.args
            print("This is params", args)
            return Response(json.dumps(animal_list),
                                    mimetype="application/json",
                                    status=200)
        
        elif (request.method == 'POST'):
            data = request.json
            print("This is client data", data)
            client_animal = "owl"

            resp = {
                "animal" : client_animal
            }

            animal_list.append(resp)
            return Response(json.dumps(animal_list),
                                    mimetype="application/json",
                                    status=200) 
        elif (request.method == 'PATCH'):
            data = request.json
            print("This is client data", data)

            animal_list[1] = {"animal" : 'Hippo'}
            return Response(json.dumps(animal_list),
                                    mimetype="application/json",
                                    status=200) 
        elif (request.method == 'DELETE'):
            data = request.json
            print("This is client data", data)
            
            animal_list.pop(2)
            return Response(json.dumps(animal_list),
                                    mimetype="application/json",
                                    status=200)
        else:
            print("Something went wrong")

except mariadb.DataError:
    print("Something wrong with your data")
except mariadb.OperationalError: #Creating already existing table falls under OperationalError
    print("Something wrong with the connection")
except mariadb.ProgrammingError:
    print("Your query was wrong")
except mariadb.IntegrityError:
    print("Your query would have broken the database")
except ValueError:
    print("Please input a username")
except:
    print("Something went wrong")

finally:
    if (cursor != None):
        cursor.close()
    else:
        print("Cursor was never opened, nothing to close here.")
    if (conn != None):
        conn.close()
    else:
        print("Connection was never opened, nothing to close here.")



