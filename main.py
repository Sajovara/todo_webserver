from flask import *
import uuid

allLists = []
allEntries = []

# initialisiere Flask-Server
app = Flask(__name__)

def findList(list_uuid):
    for dictionary in allLists:
        if(dictionary['uuid'] == list_uuid):
            return dictionary
        
def findCorrespondingEntries(list_uuid):
    

# Route fürs Zurückgeben von Entries in einer Liste
@app.route('/todo-list/<list_id>/entries', methods = ['GET'])
def return_entries_of_list(list_id):

    foundEntries = []

    for dictionary in allEntries:
        if(dictionary['list_reference'] == list_id):
            foundEntries.append(dictionary)
            
    return foundEntries

# Route fürs Löschen von Todo-Listen
@app.route('/todo-list/<list_id>', methods = ['DELETE'])
def delete_list(list_id):
    return

# Route fürs Erstellen von Todo-Listen
@app.route('/todo-list', methods = ['PUT'])
def create_list():
    list_name = request.form.get('name')#
    #if not name:
        
    list_uuid = str(uuid.uuid4())
    dictionary = {
        'id' : list_uuid,
        'name' : list_name

    }

    allLists.append(dictionary)

    return jsonify(dictionary)

# Route um einen Eintrag zu einer Todo-Liste hinzuzufügen
@app.route('/entries', methods = ['POST'])
def add_entry_to_list():
    return 

# Route um einen bestehenden Eintrag zu aktualisieren
@app.route('/entries/<list_id>/<entries_id>', methods = ['POST'])
def update_entry_in_list(list_id, entries_id):
    return 

# Route um einen bestehenden Eintrag einer Todo-Liste zu löschen
@app.route('/entries/<list_id>/<entries_id>', methods = ['DELETE'])
def delete_enty_from_list(list_id, entries_id):
    return 

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)