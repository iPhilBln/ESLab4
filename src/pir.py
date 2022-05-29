import RPi.GPIO as GPIO
from src.camera import *
from src.telegram import *

def init_pir(pinNumberPIR : int) -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinNumberPIR, GPIO.IN)
    GPIO.add_event_detect(pinNumberPIR , GPIO.RISING, callback=callback_pir)

def exit_pir() -> None:
    GPIO.cleanup()

def callback_pir(channel) -> None:
    print('Bewegung erkannt. Prozess beginnt...')
    objects = get_camList()
    for obj in objects:
        obj.get_picture()
        if obj.name == 'telegram':
            picture = obj.path + obj.name + '.jpg'
            try:
                bot = get_botListValue('pirBot')
            except Exception as err:
                print("Fehlermeldung : " + str(err))
            bot.send_message('PIR: Bewegung erkannt!')
            bot.send_photo(picture)
    print('Prozess abgeschlossen.')
