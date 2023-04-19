import requests as r
import os

stillInMenu = True;

def clearScreen():
    os.system('cls')

def startUp():
    clearScreen()

    print("Was möchtest du tun?")
    print()
    print("1. Eine neue Liste erstellen")
    print("2. Eine Liste löschen")
    print("3. Einen Eintrag erstellen")
    print("4. Den Namen eines Eintrags aktualisieren")
    print("5. Die Beschreibung eines Eintrags aktualisieren")
    print("6. Einen Eintrag einer anderen Listen zuordnen")
    print("7. Einen Eintrag löschen")
    print("8. Alle Einträge einer Liste anzeigen")
    print("9. Gar nichts")
    print()

    choice = 0

    while True:
        if (choice == "" or not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) >= 10):
            choice = input("Bitte gib eine Zahl ein (1-9): ")
        else:
            if(int(choice) == 9):
                global stillInMenu
                stillInMenu = False
            break

    return int(choice)

def listSelector(prompt):
    clearScreen()
    listLister = r.get("http://127.0.0.1:5000/todo-list")

    i = 0

    if len(listLister.json()) == 0:
        print("Es existiert noch keine Liste")
        print()
        input("Bitte Enter drücken...")
        return False
    else:
        print("Folgende Listen existieren:")
        print()
        while i < len(listLister.json()):
                print("Liste " + str(i+1) + ": " + listLister.json()[i]['name'])
                i += 1
        print()
        
        choice = 0

        while True:
            if (choice == "" or not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) >= 4) or (int(choice) > len(listLister.json())):
                
                match prompt:
                    
                    case 'delete': choice = input("Welche Liste möchtest du löschen? (1-"+str(i)+"): ")

                    case 'create_entry': choice = input("Zu welcher Liste möchtest du einen Eintrag hinzufügen? (1-"+str(i)+"): ")

                    case 'update_entry': choice = input("In welcher Liste möchtest du einen Eintrag aktualisieren? (1-"+str(i)+"): ")

                    case 'update_entry_list': choice = input("Welcher Liste möchtest du den Eintrag zuordnen? (1-"+str(i)+"): ")

                    case 'delete_entry': choice = input("Aus welcher Liste möchtest du einen Eintrag löschen? (1-"+str(i)+"): ")

                    case 'display_entries': choice = input("Aus welcher Liste möchtest du die Einträge einsehen? (1-"+str(i)+"): ")
                
            else:
                clearScreen()
                return str(listLister.json()[int(choice)-1]['id'])
            

def entrySelector(prompt, list_id):
    if list_id is not False:
        clearScreen()
        entryLister = r.get("http://127.0.0.1:5000/todo-list/"+str(list_id)+"/entries")

        i = 0

        if len(entryLister.json()) == 0:
            print("Es existieren noch keine Einträge in dieser Liste")
            print()
            input("Bitte Enter drücken...")
            return False
        else:
            print("Folgende Einträge existieren:")
            print()
            while i < len(entryLister.json()):
                    print("Eintrag " + str(i+1) + ": " + entryLister.json()[i]['name'])
                    i += 1
            print()
            
            choice = 0

            while True:
                if (choice == "" or not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) >= 4) or (int(choice) > len(entryLister.json())):
                    
                    match prompt:
                        
                        case 'delete_entry': choice = input("Welchen Eintrag möchtest du löschen? (1-"+str(i)+"): ")

                        case 'update_entry': choice = input("Welchen Eintrag möchtest du aktualisieren? (1-"+str(i)+"): ")
                    
                else:
                    clearScreen()
                    return str(entryLister.json()[int(choice)-1]['id'])
    else:
        return False
            
def printResult(result, prompt):
    clearScreen()
    
    match prompt:
        
        case 'create_list': 
            print("Folgende neue Liste wurde angelegt:")
            print()
            print("ID: " + result.json()['id'])
            print("Name: " + result.json()['name'])
        
        case 'delete_list':
            if result.json()['deleted']:
                print("Die Liste wurde erfolgreich gelöscht")
            else:
                print("Löschen nicht erfolgreich")

        case 'create_entry':
            print("Der folgende Eintrag wurde hinzugefügt:")
            print()
            print("ID: " + result.json()['id'])
            print("Listenreferenz: " + result.json()['list_reference'])
            print("Name: " + result.json()['name'])
            print("Beschreibung: " + result.json()['desc'])

        case 'update_entry':
            print("Der Eintrag sieht nun wie folgt aus: ")
            print()
            print("ID: " + result.json()['id'])
            print("Listenreferenz: " + result.json()['list_reference'])
            print("Name: " + result.json()['name'])
            print("Beschreibung: " + result.json()['desc'])

        case 'delete_entry':
            if result.json()['deleted']:
                print("Der Eintrag wurde gelöscht")
            else: 
                print("Der Eintrag konnte nicht gelöscht werden")

        case 'display_entries':
            if len(result.json()) >= 1:
                i = 0
                while i < len(result.json()):
                    print("Eintrag " + str(i+1) + ":")
                    print()
                    print("ID: " + result.json()[i]['id'])
                    print("Listenreferenz: " + result.json()[i]['list_reference'])
                    print("Name: " + result.json()[i]['name'])
                    print("Beschreibung: " + result.json()[i]['desc'])
                    print()
                    i += 1
            else:
                print("Die Liste hat noch keine Einträge")
    
    print()
    input("Bitte Enter drücken...")

while stillInMenu:
    
    match startUp():

        case 1:
            clearScreen()  
            name = input("Wie soll die neue To-Do Liste heißen? ")
            while len(name) <= 0:
                name = input("Wie soll die neue To-Do Liste heißen? ")
            result = r.put("http://127.0.0.1:5000/todo-list", data={'name' : name})
            printResult(result, 'create_list')
        
        case 2:
            list_selected =  listSelector('delete')

            if list_selected is not False:
                result = r.delete("http://127.0.0.1:5000/todo-list/" + list_selected)
                printResult(result, 'delete_list')

        case 3:
            list_selected = listSelector('create_entry')
            if list_selected is not False:
                name = input("Wie soll der neue Eintrag heißen? ")
                description = input("Wie soll die Beschreibung lauten? (darf leer sein): ")
                result = r.post("http://127.0.0.1:5000/entries", data={'name' : name, 'list_reference' : list_selected, 'desc' : description})
                printResult(result, 'create_entry')

        case 4:
            list_selected = listSelector('update_entry')
            entry_selected = entrySelector('update_entry', list_selected)

            if entry_selected is not False:
                name = input("Bitte gib den neuen Namen des Eintrags ein: ")
                result = r.post("http://127.0.0.1:5000/entries/" + list_selected + "/" + entry_selected, data={'name' : name, 'type' : 'name'})
                printResult(result, 'update_entry')

        case 5:
            list_selected = listSelector('update_entry')
            entry_selected = entrySelector('update_entry', list_selected)

            if entry_selected is not False:
                description = input("Bitte gib die neue Beschreibung des Eintrags ein: ")
                result = r.post("http://127.0.0.1:5000/entries/" + list_selected + "/" + entry_selected, data={'desc' : description, 'type' : 'desc'})
                printResult(result, 'update_entry')

        case 6:
            list_selected = listSelector('update_entry')
            entry_selected = entrySelector('update_entry', list_selected)

            if entry_selected is not False:
                list_reference = listSelector('update_entry_list')
                result = r.post("http://127.0.0.1:5000/entries/" + list_selected + "/" + entry_selected, data={'list_reference' : list_reference, 'type' : 'list_reference'})
                printResult(result, 'update_entry')

        case 7:
            list_selected = listSelector('delete_entry')
            entry_selected = entrySelector('delete_entry', list_selected)
            
            if list_selected is not False and entry_selected is not False:
                result = r.delete("http://127.0.0.1:5000/entries/" + list_selected + "/" + entry_selected)
                printResult(result, 'delete_entry')

        case 8:
            list_selected = listSelector('display_entries')

            if list_selected is not False:
                result = r.get("http://127.0.0.1:5000/todo-list/" + list_selected)
                printResult(result, 'display_entries')