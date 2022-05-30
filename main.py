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
        2. Initialisierung der Objektlisten
        3. Initialisierung der Telegram Bots
        4. Initialisierung der Objekte mit den jeweiligen
           Kameraeinstellungen
    """

    #1.
    pinNumberPIR : int  = 4
    init_pir(pinNumberPIR)

    #2.
    init_camList()
    init_botList()

    #3.
    init_pirTelebot()

    #4.
    init_camSettings()

    list = get_camList()
    for obj in list:
        print()
        print(obj)

    print(Camerasettings.print_effects())

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
