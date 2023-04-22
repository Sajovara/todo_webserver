from flask import *
import uuid

allLists = []
allEntries = []

# initialisiere Flask-Server
app = Flask(__name__)
        
# Route fürs Zurückgeben aller Entries in einer Liste oder fürs Löschen einer kompletten Liste oder für das Aktualisieren des Namens einer Liste
@app.route('/todo-list/<list_id>', methods = ['GET', 'DELETE', 'PATCH'])
def return_entries_of_list_or_rename_list_or_delete_list(list_id):

    list_exists = False
    for dictionary in allLists:
        if dictionary['id'] == list_id:
            list_exists = True
    
    if not list_exists:
        return Response("{\"message\": \"Error: UUID not found\"}", status=404, mimetype="application/json")

    else:

        if request.method == 'GET':

            foundEntries = []
            for dictionary in allEntries:
                if dictionary['list_reference'] == list_id:
                    foundEntries.append(dictionary)

            return jsonify(foundEntries)
        
        elif request.method == 'DELETE':

            for dictionary in allLists:
                if(dictionary['id'] == list_id):
                    allLists.remove(dictionary)

            return Response("{\"message\": \"Operation successful\"}", status=200, mimetype="application/json")
            
        elif request.method == 'PATCH':

            for dictionary in allLists:
                if(dictionary['id'] == list_id):
                    dictionary['name'] = request.form.get('name')
                    return jsonify(dictionary)
                
        return Response("{\"message\": \"Critical error while writing\"}", status=500, mimetype="application/json") 

# Route fürs Erstellen von Todo-Listen oder zum Zurückgeben aller Todo-Listen
@app.route('/todo-list', methods = ['GET', 'POST'])
def create_list():

    if request.method == 'GET':
        return jsonify(allLists)
    
    elif request.method == 'POST':

        if not request.form.get('name'):
            
            return Response("{\"message\": \"No name was specified\"}", status=403, mimetype="application/json")

        else:

            dictionary = {
                'id' : str(uuid.uuid4()),
                'name' : request.form.get('name')
            }

            allLists.append(dictionary)

            return jsonify(dictionary)

# Route um einen Eintrag zu einer Todo-Liste hinzuzufügen
@app.route('/todo-list/<list_id>/entry', methods = ['POST'])
def add_entry_to_list(list_id):

    list_exists = False
    for dictionary in allLists:
        if dictionary['id'] == list_id:
            list_exists = True

    if not list_exists:
        return Response("{\"message\": \"Error: UUID not found\"}", status=404, mimetype="application/json")
    
    else:
    
        dictionary = {
            'list_reference' : list_id,
            'id' : str(uuid.uuid4()),
            'name' : request.form.get('name'),
            'desc' : request.form.get('desc')
        }

        allEntries.append(dictionary)

        return jsonify(dictionary)

# Route um einen bestehenden Eintrag zu aktualisieren oder zu löschen
@app.route('/entry/<entry_id>', methods = ['PATCH', 'DELETE'])
def update_or_delete_entry_in_list(entry_id):

    entry_exists = False
    for dictionary in allEntries:
        if dictionary['id'] == entry_id:
            entry_exists = True

    if not entry_exists:
        return Response("{\"message\": \"Error: UUID not found\"}", status=404, mimetype="application/json")
    
    else:

        if request.method == 'PATCH':
            for dictionary in allEntries:
                if dictionary['id'] == entry_id:
                    if request.form.get('name'):
                        dictionary['name'] = request.form.get('name')
                    if request.form.get('desc'):
                        dictionary['desc'] = request.form.get('desc')

                    return jsonify(dictionary)
            
        elif request.method == 'DELETE':
            deleted = False
            for dictionary in allEntries:
                if dictionary['id'] == entry_id:
                    allEntries.remove(dictionary)
                    deleted = True
            
            return jsonify({'deleted' : deleted})
        
        return Response("{\"message\": \"Critical error while writing\"}", status=500, mimetype="application/json")

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)