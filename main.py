#!/usr/bin/env python3

#copy all code files from host to client:
#scp -r "/Users/philippmielke/Documents/Hochschule/Modulunterlagen/6. Semester/ES/Embedded Systems 1/UE/Labor 4/Quellcode/"* uniprojekt:/home/phil/Uniprojekte/Lab4/
#!/usr/bin/env python3
import sys
import time
import subprocess
import multiprocessing
from src.pir import *
from src.camera import *
from src.telegram import *
from src.static_webserver import *

def main():
    """
        1. Initialisierung des PIR Sensors
        2. Initialisierung der Objektliste
        3. Initialisierung des Telegram Bots
        4. Initialisierung der Objekte mit den jeweiligen
           Kameraeinstellungen
    """

    pinNumberPIR : int  = 4
    init_pir(pinNumberPIR)

    init_camList()
    init_botList()

    init_pirTelebot()

    name : str = "telegram"
    path : str = "/home/phil/Uniprojekte/Lab4/Applications"
    telegram: Camerasettings = Camerasettings(name, path)
    set_camListValue(telegram)

    name : str = "browser"
    path : str = "/home/phil/Uniprojekte/Lab4/Applications"
    width : int = 640
    height : int = 480
    browser : Camerasettings = Camerasettings(name, path, width, height)
    set_camListValue(browser)

    list = get_camList()
    for obj in list:
        print()
        print(obj)

    start_static_webserver()
    while True:
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            exit_pir()
            break
    print("\nAuf Wiedersehen...")
    sys.exit()

if __name__ == "__main__":
    main()
