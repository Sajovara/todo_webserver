from flask import *
import uuid

allLists = []
allEntries = []

# initialisiere Flask-Server
app = Flask(__name__)
        
# Route fürs Zurückgeben aller Entries in einer Liste oder fürs Löschen einer kompletten Liste
@app.route('/todo-list/<list_id>', methods = ['GET', 'DELETE'])
def return_entries_of_list(list_id):

    list_exists = False
    for dictionary in allLists:
        if dictionary['id'] == list_id:
            list_exists = True
    
    if not list_exists:
        return Response("{\"message\": \"Error: List doesn't exist\"}", status=404, mimetype="application/json")

    else:

        if request.method == 'GET':

            foundEntries = []
            for dictionary in allEntries:
                if dictionary['list_reference'] == list_id:
                    foundEntries.append(dictionary)

            return jsonify(foundEntries)
        
        elif request.method == 'DELETE':

            deleted = False

            for dictionary in allLists:
                if(dictionary['id'] == list_id):
                    allLists.remove(dictionary)
                    deleted = True
            
            if deleted:
                return jsonify({'deleted' : deleted})
            
            else:
               return Response("{\"message\": \"Critical error while writing\"}", status=500, mimetype="application/json") 

# Route fürs Erstellen von Todo-Listen
@app.route('/todo-list', methods = ['GET', 'PUT'])
def create_list():

    if request.method == 'GET':
        return jsonify(allLists)
    
    else:

        dictionary = {
            'id' : str(uuid.uuid4()),
            'name' : request.form.get('name')
        }

        allLists.append(dictionary)

        return jsonify(dictionary)

# Route um einen Eintrag zu einer Todo-Liste hinzuzufügen
@app.route('/entries', methods = ['POST'])
def add_entry_to_list():
    
    dictionary = {
        'list_reference' : request.form.get('list_reference'),
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
    else:
        deleted = False
        for dictionary in allEntries:
            if dictionary['list_reference'] == list_id and dictionary['id'] == entries_id:
                allEntries.remove(dictionary)
                deleted = True
        return jsonify({'deleted' : deleted})

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)