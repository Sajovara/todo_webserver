from flask import *
import uuid

allLists = []
allEntries = []

# initialisiere Flask-Server
app = Flask(__name__)
        
# Route fürs Zurückgeben von Entries in einer Liste
@app.route('/todo-list/<list_id>/entries', methods = ['GET'])
def return_entries_of_list(list_id):

    foundEntries = []

    for dictionary in allEntries:
        if dictionary['list_reference'] == list_id:
            foundEntries.append(dictionary)
            
    return foundEntries

# Route fürs Löschen von Todo-Listen
@app.route('/todo-list/<list_id>', methods = ['DELETE'])
def delete_list(list_id):

    for dictionary in allLists:
        if(dictionary['uuid'] == list_id):
            list.pop(dictionary)

    return jsonify({'deleted' : 'true'})

# Route fürs Erstellen von Todo-Listen
@app.route('/todo-list', methods = ['PUT'])
def create_list():

    dictionary = {
        'id' : str(uuid.uuid4()),
        'name' : request.form.get('name')
    }

    allLists.append(dictionary)

    return jsonify(dictionary)

# Route um einen Eintrag zu einer Todo-Liste hinzuzufügen
@app.route('/entries', methods = ['POST'])
def add_entry_to_list():

    if request.form.get('desc'):
        description = request.form.get('desc')
    else:
        description = ""
    
    dictionary = {
        'list_reference' : request.form.get('list_id'),
        'id' : str(uuid.uuid4()),
        'name' : request.form.get('name'),
        'desc' : description
    }

    allEntries.append(dictionary)

    return jsonify(dictionary)

# Route um einen bestehenden Eintrag zu aktualisieren oder zu löschen
@app.route('/entries/<list_id>/<entries_id>', methods = ['POST', 'DELETE'])
def update_or_delete_entry_in_list(list_id, entries_id):

    counter = 0

    if request.method == 'POST':
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id and dictionary['id'] == entries_id:
                for element in request.form.keys:
                    dictionary[element] = request.form.get(element) 

        return jsonify({'updated' : counter})
    else:
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id and dictionary['id'] == entries_id:
                counter += 1
                allEntries.pop(dictionary)
        
        return jsonify({'deleted' : counter})

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)