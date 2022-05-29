import os
import sys
import time
import socket
import picamera
import picamera.array
import multiprocessing
import numpy as np

class Camerasettings(picamera.PiCamera):
    """
        Objekte zum Erstellen verschiedener Kameraoptionen
        Klassenattribute:   cameraInUse : bool
        Objektattribute:    name : str
                            path : str
                            width : int
                            height : int
                            rotation : int
                            effect : str
    """

    #Klassenattribute
    cameraInUse : bool = False

    #Standardkonstruktor: Intialisiert die Attribute des Objekts
    def __init__(self,  name: str = None,
                        path: str = None,
                        width: int = None,
                        height: int = None,
                        rotation: int = None,
                        effect: str = None):

        if type(name) is str: self.set_name(name)
        else: self.set_name('unkown')

        if type(path) is str: self.set_path(path)
        else: self.set_path(os.getcwd())

        if type(width) is int: self.set_width(width)
        else: self.set_width(2592)

        if type(height) is int: self.set_height(height)
        else: self.set_height(1944)

        if type(rotation) is int: self.set_rotation(rotation)
        else: self.set_rotation(180)

        if type(effect) is str: self.set_effect(effect)
        else: self.set_effect("none")

    #GETTER, SETTER, DELETER Methoden
    #Attribut: name
    def get_name(self):
        return self._name
    def set_name(self, name: str):
        self._name = name
    def del_name(self):
        del self._name
    name = property(get_name, set_name, del_name)

    #Attribut: path
    def get_path(self):
        return self._path
    def set_path(self, path: str):
        if path[-1] != "/":
            self._path = path + "/"
        else:
            self._path = path[:-1] + "/"
        if not os.path.exists(self._path):
            os.makedirs(self._path)
    def del_path(self):
        del self._path
    path = property(get_path, set_path, del_path)

    #Attribut: width
    def get_width(self):
        return self._width
    def set_width(self, width: int):
        self._width = width
    def del_width(seld):
        del self._width
    width = property(get_width, set_width, del_width)

    #Attribut: height
    def get_height(self):
        return self._height
    def set_height(self, height: int):
        self._height = height
    def del_height(self):
        del self._height
    height = property(get_height, set_height, del_height)

    #Attribut: rotation
    def get_rotation(self):
        return self._rotation
    def set_rotation(self, rotation: int):
        self._rotation = rotation
    def del_rotation(self):
        del self._rotation
    rotation = property(get_rotation, set_rotation, del_rotation)

    #Attribut: effect
    def get_effect(self):
        return self._effect
    def set_effect(self, effect: str):
        self._effect = effect
    def del_effect(self):
        del self._effect
    effect = property(get_effect, set_effect, del_effect)

#Override Methoden
    #Ausgabemethode für das Objekt überschreiben
    def __str__(self) -> str:
        return  "Name: " + str(self._name) + "\n" +\
                "Path: " + str(self._path) + "\n" +\
                "Width: " + str(self._width) + "\n" +\
                "Hight: " + str(self._height) + "\n" +\
                "Rotation: " + str(self._rotation) + "\n" +\
                "Effect: " + str(self._effect)

#Klassenmethoden
    #alle möglichen Kameraeffekte ausgeben
    @staticmethod
    def print_effects() -> "str : Listet alle Effekte auf":
        with picamera.PiCamera() as camera:
            strEffekte : str = "Diese Effekte stehen zur Auswahl:"
            for effectName in camera.IMAGE_EFFECTS:
                strEffekte += "\n\t" + effectName
            camera.close()
            return strEffekte

#Kamerafunktionen
    def get_picture(self) -> "Fotoaufnahme":
        if not Camerasettings.cameraInUse:
            Camerasettings.cameraInUse = True
            with picamera.PiCamera(resolution = (self._width, self._height)) as camera:
                camera.rotation = self._rotation
                camera.image_effect = self._effect
                try:
                    camera.start_preview()
                    time.sleep(0.75)
                    camera.capture(self._path + self._name + ".jpg")
                except PiCameraError as err:
                    print("unerwarteter Fehler: " + str(err))
                    camera.stop_preview()
                    camera.close()
                except KeyboardInterrupt:
                    camera.stop_preview()
                    camera.close()
                finally:
                    camera.stop_preview()
                    camera.close()
                    Camerasettings.cameraInUse = False
                    print("Foto wurde unter " + self._path + self._name + ".jpg" + " gespeichert.")
        else:
            print("Die Kamera wird aktuell verwendet.")

class MyMotionDetector(picamera.array.PiMotionAnalysis):

    motionDetectionEnable : bool = True

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10 and MyMotionDetector.motionDetectionEnable:
            print('Motion detected!')

def enable_motionDetector(timeInSeconds : int):
    with picamera.PiCamera( resolution = (640, 480),
                            framerate = 30) as camera:
        try:
            camera.start_recording(
            '/dev/null', format = 'h264',
            motion_output = MyMotionDetector(camera)
            )
            camera.wait_recording(timeInSeconds)
        except KeyboardInterrupt:
            camera.stop_recording()

"""
    alle angelegten Kameraeinstellungen werden in einer Liste gespeichert,
    Funktionen um die Liste zu bearbeiten:
        init_camList : Initialisierung der Liste
        get_camList : Holen der Liste
        get_camListValue : such ein Objekt in der Liste
        set_camListValue : Objekt zur Liste hinzufügen
        del_camListValue : Objekt aus der Liste löschen
"""

camList : list = []

def init_camList():
    """Initilisiert die Liste mit den Kameraeinstellungen."""
    print("\nDie Objekliste wird Intialisiert...")
    camList.clear()
    print("Die Kameraliste wurde erfolgreich zurückgesetzt.\n")

def get_camList() -> list:
    """Gibt alle angelegten Kameraeinstellungen zurück."""
    return camList

def get_camListValue(name : str ) -> list:
    """Such ein bestimmtes Objekt in der Liste mit den Kameraeinstellungen."""
    for obj in camList:
        if obj.name == name:
            return obj
    print('Das gesuchte Objekt war nicht in der Liste vorhanden.')
    return -1

def set_camListValue(obj : Camerasettings):
    """Fügt ein Objekt zur Liste mit den Kemaraeinstellungen hinzu."""
    camList.append(obj)
    print(obj.name + " wurde erfolgreich zur Kameraliste hinzugefügt.")


def del_camListValue(obj : Camerasettings):
    """Löscht ein Objekt aus der Liste mit den Kameraeinstellungen."""
    camList.remove(obj)
    print(obj.name + " wurde erfolgreich von der Kameraliste gelöscht.")