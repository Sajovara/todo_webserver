from flask import *
import uuid

allLists = []
allEntries = []

# initialisiere Flask-Server
app = Flask(__name__)
        
# Route fürs Zurückgeben von Entries in einer Liste
@app.route('/todo-list/<list_id>/entries', methods = ['GET'])
def return_entries_of_list(list_id):

    listExists = False

    for dictionary in allLists:
        if dictionary['id'] == list_id:
            listExists = True

    foundEntries = []
    if listExists:
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id:
                foundEntries.append(dictionary)
                
        return jsonify(foundEntries)
    else:
        return jsonify(False)

# Route fürs Löschen von Todo-Listen
@app.route('/todo-list/<list_id>', methods = ['DELETE'])
def delete_list(list_id):

    deleted = False

    for dictionary in allLists:
        if(dictionary['id'] == list_id):
            allLists.remove(dictionary)
            deleted = True
            
    return jsonify({'deleted' : deleted})

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

    list_reference = request.form.get('list_reference')

    listExists = False

    for dictionary in allLists:
        if(dictionary['id'] == list_reference):
            listExists = True

    if not listExists:
        list_reference = ""
    
    dictionary = {
        'list_reference' : list_reference,
        'id' : str(uuid.uuid4()),
        'name' : request.form.get('name'),
        'desc' : request.form.get('desc')
    }

    allEntries.append(dictionary)

    return jsonify(dictionary)

# Route um einen bestehenden Eintrag zu aktualisieren oder zu löschen
@app.route('/entries/<list_id>/<entries_id>', methods = ['POST', 'DELETE'])
def update_or_delete_entry_in_list(list_id, entries_id):

    if request.method == 'POST':
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id and dictionary['id'] == entries_id:
                if request.form.get('type') == 'name':
                    dictionary['name'] = request.form.get('name')
                elif request.form.get('type') == 'desc':
                    dictionary['desc'] = request.form.get('desc')
                elif request.form.get('type') == 'list_reference':
                    dictionary['list_reference'] = request.form.get('list_reference')
            return jsonify(dictionary)
        return jsonify(False)
    else:
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id and dictionary['id'] == entries_id:
                allEntries.remove(dictionary)
                return jsonify(True)
        return jsonify(False)
        
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)