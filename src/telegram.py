import os
import time
import json
import telepot
import urllib.request

class MyBots(object):
    """Klasse mit angelegten Telegrambots"""
    def __init__(self,  name : str,
                        token : str,
                        id : int):
        self.set_name(name)
        self.set_token(token)
        self.set_id(id)
        self.bot = telepot.Bot(self.token)

    #GETTER, SETTER, DELETER Methoden
    #Attribut: name
    def get_name(self):
        return self._name
    def set_name(self, name: str):
        self._name = name
    def del_name(self):
        del self._name
    name = property(get_name, set_name, del_name)

    #Attribut: token
    def get_token(self):
        return self._token
    def set_token(self, token: str):
        self._token = token
    def del_token(self):
        del self._token
    token = property(get_token, set_token, del_token)

    #Attribut: id
    def get_id(self):
        return self._id
    def set_id(self, id: int):
        self._id = id
    def del_id(self):
        del self._id
    id = property(get_id, set_id, del_id)

#Override Methoden
    #Ausgabemethode für das Objekt überschreiben
    def __str__(self) -> str:
        return  "Name: " + str(self._name) + "\n" +\
                "Token: " + str(self._token) + "\n" +\
                "ID: " + str(self._id) + "\n"

#Botfunktionen
    def send_message(self, message : str) -> None:
        """Sendet die angegebene Textnachricht."""
        self.bot.sendMessage(self._id, message)

    def send_photo(self, photopath : str) -> None:
        """Sendet ein Foto vom angegebenen Pfad."""
        self.bot.sendPhoto(self._id, photo=open(f'{photopath}', 'rb'))

def init_pirTelebot() -> None:
    """legt einen Telegrambot für den PIR Sensor an."""
    token : str = ''
    id : int = None

    print()
    try:
        path : str = os.getcwd() + '/src/token.txt'
        with open(path, 'r') as f:
            token = f.readline().rstrip("\n")
            print('Token: ' + str(token))
    except Exception as err:
        print(err)

    url =   'https://api.telegram.org/bot'\
            + token +\
            '/getUpdates'
    while type(id) != int:
        try:
            with urllib.request.urlopen(url) as update:
                data = json.loads(update.read().decode())
                id = data['result'][0]['message']['from']['id']
                time.sleep(1)
        except Exception as err:
            print('Fehler: ' + str(err))

    print('ID: ' + str(id))
    print()
    pirBot = MyBots('pirBot', token, id)
    set_botListValue(pirBot)
    pirBot.send_message('PIR: System online!')


"""
    alle angelegten Telegrambots werden in einer Liste gespeichert,
    Funktionen um die Liste zu bearbeiten:
        init_botList : Initialisierung der Liste
        get_botList : Holen der Liste
        get_botListValue : such ein Objekt in der Liste
        set_botListValue : Objekt zur Liste hinzufügen
        del_botListValue : Objekt aus der Liste löschen
"""

botList : list = []

def init_botList() -> None:
    """
        Initilisiert die Liste mit den Telegrambots
    """
    print("\nDie Botliste wird Intialisiert...")
    botList.clear()
    print("Die Botliste wurde erfolgreich zurückgesetzt.\n")

def get_botList() -> list:
    """
        Gibt alle angelegten Telegrambots zurück.
    """
    return botList

def get_botListValue(name : str ) -> object:
    """
        Such ein bestimmtes Objekt in der Liste mit den Telegrambots.
    """
    for obj in botList:
        if obj.name == name:
            return obj
    print('Das gesuchte Objekt war nicht in der Liste vorhanden.')
    return -1

def set_botListValue(obj : MyBots) -> None:
    """
        Fügt ein Objekt zur Liste mit den Telegrambots hinzu.
    """
    botList.append(obj)
    print(obj.name + " wurde erfolgreich zur Botliste hinzugefügt.")

def del_objListValue(obj : MyBots) -> None:
    """
        Löscht ein Objekt aus der Liste mit den Telegrambots.
    """
    botList.remove(obj)
    print(obj.name + " wurde erfolgreich von der Botliste gelöscht.")
