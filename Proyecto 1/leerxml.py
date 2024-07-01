from listadoble import *
from tkinter import filedialog 
import xml.etree.ElementTree as ET
from Libreria import *
from Cancion import *


class XML:
    def __init__(self):
        self.ruta = self.loadXML()
        self.contenido = ""
    def loadXML(self):
        try:
            ruta  = filedialog.askopenfilename(title = "Seleccione su XML", filetypes=[("XML File", "*.xml *.XML")])
            return ruta
        except: FileNotFoundError
    def analyze(self):
        if self.ruta == "":
            print("Sin ruta XML")
            return None
        else:
            self.contenido = open(self.ruta, "r").read()
            self.biblioteca = Library()
            library = ET.fromstring(self.contenido)
            for biblioteca in library.iter("biblioteca"):
                for cancion in biblioteca.iter("cancion"):
                    nombre = cancion.attrib["nombre"]
                    album = ""
                    artista = ""
                    imagen = ""
                    ruta = ""
                    for artist, album_, image, path in zip(
                        cancion.iter("artista"), cancion.iter("album"), cancion.iter("imagen"), cancion.iter("ruta")):
                        album += album_.text
                        artista += artist.text
                        imagen += image.text
                        ruta += path.text
                    if nombre == "":
                        nombre += "single"
                    if album == "":
                        album += "single"
                    if artista == "":
                        artista += "single"
                    self.biblioteca.addSong(Cancion(nombre, album, artista, ruta, imagen))
            return self.biblioteca 