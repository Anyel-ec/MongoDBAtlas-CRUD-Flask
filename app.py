from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

app = Flask(__name__)

uri = os.getenv("MONGO_URI")  # Acceder a la variable de entorno
# Intenta conectar con MongoDB Atlas
try:
    client = MongoClient(uri)
    db = client.test_database 
    collection = db.personas  
    print("Conexión exitosa a MongoDB Atlas")
except ConnectionFailure:
    print("Error de conexión a MongoDB Atlas")


# Ruta para mostrar todas las personas
@app.route('/')
def show_people():
    people = collection.find()
    return render_template('index.html', people=people)


# Ruta para agregar una nueva persona
@app.route('/add', methods=['GET', 'POST'])
def add_person():
    """
    Add a new person to the collection.

    If the request method is POST, a new person is created using the data from the form.
    The person's name, age, and city are extracted from the form and stored in a dictionary.
    The dictionary is then inserted into the collection using the `insert_one` method.
    Finally, the user is redirected to the 'show_people' route.

    If the request method is GET, the 'add.html' template is rendered.

    Returns:
        If the request method is POST, redirects to the 'show_people' route.
        If the request method is GET, renders the 'add.html' template.
    """
    if request.method == 'POST':
        new_person = {
            'nombre': request.form['nombre'],
            'edad': int(request.form['edad']),
            'ciudad': request.form['ciudad']
        }
        collection.insert_one(new_person)
        return redirect(url_for('show_people'))
    return render_template('add.html')


# Ruta para editar una persona
@app.route('/edit/<person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    """
    Edit a person's information.

    Args:
        person_id (str): The ID of the person to edit.

    Returns:
        Response: A redirect response to the 'show_people' route or a rendered template for the 'edit.html' page.
    """
    person = collection.find_one({'_id': ObjectId(person_id)})
    if request.method == 'POST':
        updated_person = {
            'nombre': request.form['nombre'],
            'edad': int(request.form['edad']),
            'ciudad': request.form['ciudad']
        }
        collection.update_one({'_id': ObjectId(person_id)}, {'$set': updated_person})
        return redirect(url_for('show_people'))
    return render_template('edit.html', person=person)



"""
    Delete a person from the collection based on their ID.

    Args:
        person_id (str): The ID of the person to be deleted.

    Returns:
        redirect: A redirect to the 'show_people' route.
    """
@app.route('/delete/<person_id>')
def delete_person(person_id):
    collection.delete_one({'_id': ObjectId(person_id)})
    return redirect(url_for('show_people'))


if __name__ == '__main__':
    app.run(debug=True)
