from flask import *

allLists = []

# initialisiere Flask-Server
app = Flask(__name__)

# Route fürs Zurückgeben von Entries in einer Liste
@app.route('/todo-list/<list_id>/entries ', methods = ['GET'])
def return_entries_of_list(list_id):
    return 

# Route fürs Löschen von Todo-Listen
@app.route('/todo-list/<list_id> ', methods = ['DELETE'])
def delete_list(list_id):
    return 

# Route fürs Erstellen von Todo-Listen
@app.route('/todo-list', methods = ['PUT'])
def create_list():
    return 

# Route um einen Eintrag zu einer Todo-Liste hinzuzufügen
@app.route('/entries', methods = ['POST'])
def index():
    return 

# Route um einen bestehenden Eintrag zu aktualisieren
@app.route('/entries/<list_id>/<entries_id>', methods = ['POST'])
def index(list_id, entries_id):
    return 

# Route um einen bestehenden Eintrag einer Todo-Liste zu löschen
@app.route('/entries/<list_id>/<entries_id>', methods = ['DELETE'])
def index(list_id, entries_id):
    return 

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)