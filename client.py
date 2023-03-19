import requests as r
import os

stillInMenu = True;

def clearScreen():
    os.system('cls')

def startUp():
    clearScreen()
    print("Was möchtest du tun?")
    print("1. Eine neue Liste erstellen")
    print("2. Eine Liste löschen")
    print("3. Einen Eintrag erstellen")
    print("4. Den Namen eines Eintrags aktualisieren")
    print("5. Die Beschreibung eines Eintrags aktualisieren")
    print("6. Einen Eintrag einer anderen Listen zuordnen")
    print("7. Einen Eintrag löschen")
    print("8. Alle Einträge einer Liste anzeigen")
    print("9. Gar nichts")

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

while stillInMenu:
    
    match startUp():

        case 1:
            clearScreen()  
            name = input("Wie soll die neue To-Do Liste heißen? ")
            while len(name) <= 0:
                name = input("Wie soll die neue To-Do Liste heißen? ")
            result = r.put("http://127.0.0.1:5000/todo-list", data={'name' : name})
            clearScreen()
            print("Folgende neue Liste wurde angelegt:")
            print("ID: " + result.json()['id'])
            print("Name: " + result.json()['name'])
            input("Bitte Enter drücken...")
        
        case 2:
            clearScreen()  
            list_id = input("Welche Liste möchtest du löschen? (ID): ")
            result = r.delete("http://127.0.0.1:5000/todo-list/" + str(list_id))
            clearScreen()
            if result.json()['deleted']:
                print("Die Liste wurde erfolgreich gelöscht")
            else:
                print("Löschen nicht erfolgreich (gibt es die Liste?)")
            input("Bitte Enter drücken...")

        case 3:
            clearScreen()
            list_reference = input("Zu welcher Liste soll der Eintrag gehören? (ID): ")
            name = input("Wie soll der neue Eintrag heißen? ")
            description = input("Wie soll die Beschreibung lauten? (darf leer sein): ")
            result = r.post("http://127.0.0.1:5000/entries", data={'name' : name, 'list_reference' : list_reference, 'desc' : description})
            clearScreen()
            if result.json()['list_reference'] == "":
                print("Die Liste existiert nicht")
            else: 
                print("Der folgende Eintrag wurde hinzugefügt:")
                print("ID: " + result.json()['id'])
                print("Listenreferenz: " + result.json()['list_reference'])
                print("Name: " + result.json()['name'])
                print("Beschreibung: " + result.json()['desc'])
            input("Bitte Enter drücken...")

        case 4:
            clearScreen()
            list_id = input("In welcher Liste möchtest du einen Eintrag aktualisieren? (ID): ")
            entry_id = input("Um welchen Eintrag handelt es sich? (ID): ")

            name = input("Bitte gib den neuen Namen des Eintrags ein: ")
            
            clearScreen()
            result = r.post("http://127.0.0.1:5000/entries/" + str(list_id) + "/" + entry_id, data={'name' : name, 'type' : 'name'})

            if not result.json():
                print("Die Liste oder der Eintrag existiert nicht")
            else:
                print("Der Eintrag sieht nun wie folgt aus: ")
                print("ID: " + result.json()['id'])
                print("Listenreferenz: " + result.json()['list_reference'])
                print("Name: " + result.json()['name'])
                print("Beschreibung: " + result.json()['desc'])
            input("Bitte Enter drücken...")

        case 5:
            clearScreen()
            list_id = input("In welcher Liste möchtest du einen Eintrag aktualisieren? (ID): ")
            entry_id = input("Um welchen Eintrag handelt es sich? (ID): ")

            description = input("Bitte gib die neue Beschreibung des Eintrags ein: ")
            
            clearScreen()
            result = r.post("http://127.0.0.1:5000/entries/" + str(list_id) + "/" + str(entry_id), data={'desc' : description, 'type' : 'desc'})

            if not result.json():
                print("Die Liste oder der Eintrag existiert nicht")
            else:
                print("Der Eintrag sieht nun wie folgt aus: ")
                print("ID: " + result.json()['id'])
                print("Listenreferenz: " + result.json()['list_reference'])
                print("Name: " + result.json()['name'])
                print("Beschreibung: " + result.json()['desc'])
            input("Bitte Enter drücken...")

        case 6:
            clearScreen()
            list_id = input("In welcher Liste möchtest du einen Eintrag aktualisieren? (ID): ")
            entry_id = input("Um welchen Eintrag handelt es sich? (ID): ")

            list_reference = input("Bitte gib die neue Listenzuordnung des Eintrags ein (ID): ")
            
            clearScreen()
            result = r.post("http://127.0.0.1:5000/entries/" + str(list_id) + "/" + str(entry_id), data={'list_reference' : list_reference, 'type' : 'list_reference'})

            if not result.json():
                print("Die Liste oder der Eintrag existiert nicht")
            else:
                print("Der Eintrag sieht nun wie folgt aus: ")
                print("ID: " + result.json()['id'])
                print("Listenreferenz: " + result.json()['list_reference'])
                print("Name: " + result.json()['name'])
                print("Beschreibung: " + result.json()['desc'])
            input("Bitte Enter drücken...")

        case 7:
            clearScreen()
            list_id = input("In welcher Liste möchtest du einen Eintrag löschen? (ID): ")
            entry_id = input("Um welchen Eintrag handelt es sich? (ID): ")
            
            clearScreen()
            result = r.delete("http://127.0.0.1:5000/entries/" + str(list_id) + "/" + str(entry_id))
            if result:
                print("Der Eintrag wurde gelöscht")
            else: 
                print("Der Eintrag konnte nicht gelöscht werden")
            input("Bitte Enter drücken...")

        case 8:
            clearScreen()
            list_id = input("Von welcher Liste möchstest du alle Einträge anzeigen? (ID): ")

            clearScreen()
            result = r.get("http://127.0.0.1:5000/todo-list/" + str(list_id) + "/entries")

            if result.json() is not False:
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
                print("Die Liste existiert nicht")

            input("Bitte Enter drücken...")