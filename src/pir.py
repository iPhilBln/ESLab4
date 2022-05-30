import RPi.GPIO as GPIO
from src.camera import *
from src.telegram import *

def init_pir(pinNumberPIR : int) -> None:
    """Initilisiert den PIR Sensor."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinNumberPIR, GPIO.IN)
    GPIO.add_event_detect(pinNumberPIR , GPIO.RISING, callback=callback_pir)

def exit_pir() -> None:
    """Setzt die GPIO Ports zurück."""
    GPIO.cleanup()

def callback_pir(channel) -> None:
    """Wird bei Bewegungserkennung am PIR Sensor aufgerufen und macht die Bilder."""
    print('Bewegung erkannt. Prozess beginnt...')

    try:
        bot = get_botListValue('pirBot')
    except Exception as err:
        print("Fehlermeldung : " + str(err))
    bot.send_message('PIR: Bewegung erkannt!')

    camList = get_camList()
    for obj in camList:
        if 'telegram' in obj.name:
            obj.get_picture()
            picture = obj.path + obj.name + '.jpg'
            bot.send_photo(picture)
    print('Prozess abgeschlossen.')
