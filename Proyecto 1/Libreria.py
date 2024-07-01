import os
from listadoble import *
from Album import *
from Artista import *


class Library:
    def __init__(self):
        self.listaArtistas = ListaDoble()
    def addSong(self, song):
        new = song
        nombre = new.nombre
        album = new.album
        artista = new.artista
        imagen = new.imagen
        contains = self.listaArtistas.contains(artista)
        if contains != None:
            artist = self.listaArtistas.getById(contains)
            contains = artist.listaAlbumes.contains(album)
            if contains != None:
                album_ = artist.listaAlbumes.getById(contains)
                contains = album_.listaCanciones.contains(nombre)
                if contains != None:
                    print("Cancion en biblioteca.. Posición: {}".format(contains))
                else:
                    album_.listaCanciones.append(new)
            else:
                nuevoAlbum = Album(album, imagen)
                nuevoAlbum.listaCanciones.append(new)
                artist.listaAlbumes.append(nuevoAlbum)
        else:
            nuevoArtista = Artista(artista)
            nuevoAlbum = Album(album, imagen)
            nuevoAlbum.listaCanciones.append(new)
            nuevoArtista.listaAlbumes.append(nuevoAlbum)
            self.listaArtistas.append(nuevoArtista)
    def toList(self):#Este método retorna una lista que es necesaria
        lista = ListaDoble()
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    lista.append(cancion)
        return lista
    def report(self):
        string = """digraph G {
layout = dot;
labelloc = "t";
edge [weigth = 1000];
rankdir = LR;\n"""
        string += "\tsubgraph artistas {\n\trankdir = LR;\n"
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            string += '\t\t"{}"[fillcolor = beige style = "filled"];\n'.format(artista.nombre)
            string += '\t\t\tsubgraph "album{}"{}\n\t\t\trankdir = TB;\t\t\trank=same;\n'.format(artista.nombre,"{")
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                if j == 0:
                    string += '\t\t\t\t"{}"->"{}"\n'.format(artista.nombre,album.nombre)
                string += '\t\t\t\t"{}"[fillcolor = aquamarine style = "filled"];\n'.format(album.nombre)
                string += '\t\t\t\t\tsubgraph "album{}"{}\n\t\t\t\t\trankdir = LR;\n'.format(album.nombre,"{")
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    if k == 0:
                        string += '\t\t\t\t\t\t"{}"->"{}"\n'.format(album.nombre, cancion.nombre)
                    string += '\t\t\t\t\t\t\t"{}"[fillcolor = deepskyblue style = "filled"];\n'.format(cancion.nombre)
                string += '\t\t\t\t\t}\n'

            string += '\t\t\t}\n'
        string += "\t}\n"
        #Hacia delante
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            if i+1 == self.listaArtistas.length:
                string += '"{}"->"NoneR{}"[style = dashed];\n'.format(artista.nombre, i+1)
            else:
                siguiente = self.listaArtistas.getById(i+1)
                string += '"{}"->"{}";\n'.format(artista.nombre, siguiente.nombre)
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                if j+1 == artista.listaAlbumes.length:
                    string += '"{}"->"NoneR{}{}"[style = dashed];\n'.format(album.nombre,i,j)
                else:
                    siguiente = artista.listaAlbumes.getById(j+1)
                    string += '"{}"->"{}";\n'.format(album.nombre, siguiente.nombre)
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    if k+1 == album.listaCanciones.length:
                        string += '"{}"->"NoneR{}{}{}"[style = dashed];\n'.format(cancion.nombre,i,j,k)
                    else:
                        siguiente = album.listaCanciones.getById(k+1)
                        string += '"{}"->"{}";\n'.format(cancion.nombre, siguiente.nombre)
        #Hacia atras
        for i in range(self.listaArtistas.length-1,-1,-1):
            artista = self.listaArtistas.getById(i)
            if i-1 == -1:
                string += '"{}"->"NoneL{}"[style = dashed];\n'.format(artista.nombre,i)
            else:
                anterior = self.listaArtistas.getById(i-1)
                string += '"{}"->"{}";\n'.format(artista.nombre, anterior.nombre)
            for j in range(artista.listaAlbumes.length-1,-1,-1):
                album = artista.listaAlbumes.getById(j)
                if j-1 == -1:
                    string += '"{}"->"NoneL{}{}"[style = dashed];\n'.format(album.nombre,j,i)
                else:
                    anterior = artista.listaAlbumes.getById(j-1)
                    string += '"{}"->"{};"\n'.format(album.nombre, anterior.nombre)
                for k in range(album.listaCanciones.length-1,-1,-1):
                    cancion = album.listaCanciones.getById(k)
                    if k-1 == -1:
                        string += '"{}"->"NoneL{}{}{}"[style = dashed];\n'.format(cancion.nombre,k,j,i)
                    else:
                        anterior = album.listaCanciones.getById(k-1)
                        string += '"{}"->"{}";\n'.format(cancion.nombre, anterior.nombre)
        string += "\n}"
        file = open("library.dot", "w")
        file.write(string)
        file.close()
        os.system('dot -Tpng library.dot -o library.png')
    def getArtistas(self):
        lista = []
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            lista.append(artista.nombre)
        return lista    
    def __str__(self):
        string = "Biblioteca\n\tArtistas:\n"
        for i in range(self.listaArtistas.length):
            string += "\n\t{}".format(self.listaArtistas.getById(i))
        return string