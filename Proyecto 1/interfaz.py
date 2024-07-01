import random
import os 
from tkinter.constants import END, CENTER, VERTICAL
from tkinter import Image, Tk , Button,Frame,Label, ttk, messagebox
import tkinter.font as Tfont
from PIL import Image, ImageTk
from hilos import *
from listadoble import*
from leerxml import XML
import webbrowser
from ListaCircular import *
from posicionEntrada import *



class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        x_ =self.winfo_screenwidth()//2-1025//2
        y_ = self.winfo_screenheight() //2-625//2
        self.resizable(0,0)
        self.geometry('1025x625+{}+{}'.format(x_,y_))
        self.title('IPCmusic')
        self.library = None
        self.songslist = ListaDoble()
        self.playlist = ListaCircular()
        self.actualPlaylist = None
        self.threadPlay = None
        self.listaPlayList = ListaCircular()
        self.initComponent()
    
    def initComponent(self):
        self.fondo = Frame(self, background= '#082032')
        self.fondo.place(x=0, y=0 , width = 1025, height = 625)
        
        
        
        #botones
        self.btnCargarXML = Button(self.fondo, text = "Cargar Archivo", command = self.cargarXML)
        self.btnReportes = Button(self.fondo, text = "Reportes", command = self.reportes)
        self.btnPlay = Button(self.fondo, text = "Play", command = self.playLista)
        self.btnAleatorio = Button(self.fondo, text = "Aleatorio", command = self.playRandom)
        self.btnpause = Button(self.fondo, text = "Pausa", command = self.pause)
        self.btnStop = Button(self.fondo, text = "Stop", command = self.stop)
        self.btnSiguiente = Button(self.fondo,  text = "Next", command = self.aNext)
        self.btnAnterior = Button(self.fondo, text = "Back", command = self.aBack)
        self.btnAddToList = Button(self.fondo, text = "Agregar a Lista ↓", command = self.addToList)
        self.btnSaveList = Button(self.fondo, text = "Guardar Lista", command = self.saveList)
        self.btnDelete = Button(self.fondo, text = "Eliminar Lista", command = self.addPlayList)
        self.btnExportList = Button(self.fondo, text = "Exportar Listas", command = self.exportarListas)
        self.btnhtml = Button(self.fondo, text = "html", command=self.exportar_listas_html)
        
        
        
        
        #labels
        fontStyle = Tfont.Font(family= 'lucida grande' ,size = 13 )
        self.labelCancion = Label(self.fondo, text = "Canción: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.labelAlbum = Label(self.fondo, text = "Album: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.labelArtista = Label(self.fondo, text = "Artista: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")

        self.lblartista = Label(self.fondo, text = "Artista", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.lblalbum = Label(self.fondo, text = "Album", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.lblplaylist = Label(self.fondo, text = "Playlist", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        
        
        
        #foto
        self.foto = Frame(self.fondo)
        
        # Arbol 
        self.addArbol()
        
        #playlist
        self.addPlayList()
        
        #COMBOBOX
        self.cbbArtistas = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbAlbumbes = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbListas = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbArtistas.bind("<<ComboboxSelected>>", self.change_artist)
        self.cbbAlbumbes.bind("<<ComboboxSelected>>", self.change_album)
        self.cbbArtistas.place(x = 890, y = 40, width = 120)
        self.cbbAlbumbes.place(x = 890, y = 100, width = 120)
        self.cbbListas.place(x = 890, y = 160, width = 120)
        
        
        
        
        # se ubican los objetos
        self.btnCargarXML.place(x = 20, y = 20, width = 135, height = 25)
        self.btnReportes.place(x = 200, y = 20, width = 85, height = 25)
        self.btnhtml.place(x = 300, y = 20, width = 85, height = 25)

        self.foto.place(x = 20, y = 70, width = 360, height = 350)
        self.btnPlay.place(x = 20, y = 440, width = 40, height = 25)
        self.btnAleatorio.place(x = 68, y = 440, width = 68, height = 25)
        self.btnpause.place(x = 144, y = 440, width = 50, height = 25)
        self.btnStop.place(x = 202, y = 440, width = 40, height = 25)
        self.btnAnterior.place(x = 250, y = 440, width = 40, height = 25)
        self.btnSiguiente.place(x = 300, y = 440, width = 40, height = 25)

        self.labelCancion.place(x = 20, y = 480, height = 35, width = 360)
        self.labelAlbum.place(x = 20, y = 525, height = 35, width = 360)
        self.labelArtista.place(x = 20, y = 570, height = 35, width = 360)

        self.btnAddToList.place(x = 500, y = 300, width = 100)
        self.btnSaveList.place(x = 700, y = 300, width = 100)

        self.btnDelete.place(x = 900, y = 400, width = 100)
        self.btnExportList.place(x = 900, y = 450, width = 100) 

        self.lblartista.place(x = 925, y = 20, width = 100, height = 20)
        self.lblalbum.place(x = 925, y = 80, width = 100, height = 20)
        self.lblplaylist.place(x = 922, y = 140, width = 100, height = 20)
        
    def playLista(self):
        selected_lista = self.cbbListas.get()
        if selected_lista:
            lista = self.listaPlayList.findByName(selected_lista)
            if lista:
                self.playList = lista
                self.play()
            else:
                messagebox.showwarning(title="Alerta", message="Lista de reproducción no encontrada.")
        else:
            messagebox.showwarning(title="Alerta", message="Selecciona una lista de reproducción.")

    
    def addArbol(self):
        columns = ("cancion", "album", "artista")
        self.tabla = ttk.Treeview(self.fondo, columns = columns, show = "headings")
        self.tabla.heading('cancion',text = "Canción")
        self.tabla.heading('album', text = "Album")
        self.tabla.heading('artista', text = "Artista")
        self.tabla.column('cancion', width = 150)
        self.tabla.column('album', width = 150)
        self.tabla.column('artista', width = 150)
        scrollbar = ttk.Scrollbar(self.fondo, orient = VERTICAL, command = self.tabla.yview)
        self.tabla.configure(yscrollcommand = scrollbar.set)
        scrollbar.place(x= 860, y = 20, width = 20, height = 200)
        self.tabla.place(x = 410, y = 20, width = 450, height = 200)
    
    def addPlayList(self):
        self.entryPlaylist = EntryPlaceholder("Nombre de Playlist", self.fondo, color = "#000000")
        self.entryPlaylist.config(justify = CENTER)
        columns2 = ("lista")
        self.tablePlaylist = ttk.Treeview(self.fondo, columns =  columns2, show = "headings")
        texto = self.entryPlaylist.get()
        self.tablePlaylist.heading("lista", text = texto)
        scrollbar2 = ttk.Scrollbar(self.fondo, orient = VERTICAL, command = self.tablePlaylist.yview)
        self.tablePlaylist.configure(yscrollcommand = scrollbar2.set)
        scrollbar2.place(x = 860, y = 400, width = 20, height = 200)
        self.entryPlaylist.place(x = 410, y = 400, width = 450, height = 30)
        self.tablePlaylist.place(x = 410, y = 430, width = 450, height = 170)
        self.playList = ListaCircular()
        
    def cargarXML(self):
        lector = XML()
        self.library = lector.analyze()
        self.songslist = self.library.toList()
        self.setArtistas()
        
    def setArtistas(self):
        Artistas = self.library.getArtistas()
        self.cbbArtistas["values"] = Artistas
        self.cbbArtistas.current(0)
        self.change_artist(None)
    
    def change_artist(self, event):
        self.setAlbumes()
    
    def setAlbumes(self):
        artista = self.cbbArtistas.current()
        artista = self.library.listaArtistas.getById(artista)
        self.cbbAlbumbes["values"] = artista.getAlbumes()
        self.cbbAlbumbes.current(0)
    
    def change_album(self, event):
        self.setCanciones()
    
    def setCanciones(self):
        self.addArbol()
        self.songslist = self.library.listaArtistas.getById(
            self.cbbArtistas.current()).listaAlbumes.getById(
                self.cbbAlbumbes.current()).getCanciones()
        for i in range(self.songslist.length):
            song = self.songslist.getById(i)
            row = ("{}".format(song.nombre),"{}".format(song.album),"{}".format(song.artista))
            self.tabla.insert('', END, values = row, iid = i)
        child_id = self.tabla.get_children()[0]
        self.tabla.focus(child_id)
        self.tabla.selection_set(child_id)  
    
    def addToList(self):
        self.tablePlaylist.heading("lista", text = self.entryPlaylist.get())
        if self.songslist.length > 0:
            song = self.songslist.getById(int(self.tabla.focus()))
            self.playList.append(song)
            row = ("{}".format(song.nombre), "{}".format(song.album), "{}".format(song.artista))
            self.tablePlaylist.insert('', END, values = row, iid = self.playList.length-1)
    
    def play(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.playList.head
            self.setInfo(self.actualPlaylist.value.nombre, self.actualPlaylist.value.album, self.actualPlaylist.value.artista)
            self.setPhoto(self.actualPlaylist)
            self.reproducir(self.actualPlaylist.value)
        elif self.songslist.length > 0 and self.playList.length == 0:
            for i in range(self.songslist.length):
                song = self.songslist.getById(i)
                self.playList.append(song)
                row = ("{}".format(song.nombre), "{}".format(song.album), "{}".format(song.artista))
                self.tablePlaylist.insert('', END, values=row, iid=i)
    
            # Reproduce la primera canción en la playlist recién creada
            self.actualPlaylist = self.playList.head
            self.setInfo(self.actualPlaylist.value.nombre, self.actualPlaylist.value.album, self.actualPlaylist.value.artista)
            self.setPhoto(self.actualPlaylist)
            self.reproducir(self.actualPlaylist.value)
    
    def aNext(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.next(self.actualPlaylist)
            self.tablePlaylist.focus(self.actualPlaylist.id)
            self.tablePlaylist.selection_set(self.actualPlaylist.id)
            self.reproducir(self.actualPlaylist.value)
    
    def aBack(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.back(self.actualPlaylist)
            self.tablePlaylist.focus(self.actualPlaylist.id)
            self.tablePlaylist.selection_set(self.actualPlaylist.id)
            self.reproducir(self.actualPlaylist.value)
    
    def next(self, nodo):
        aux = nodo.siguiente
        self.setInfo(aux.value.nombre, aux.value.album, aux.value.artista)
        self.setPhoto(aux)
        return aux
    
    def back(self, nodo):
        aux = nodo.anterior
        self.setInfo(aux.value.nombre, aux.value.album, aux.value.artista)
        self.setPhoto(aux)
        return aux
    
    def setPhoto(self, nodo):
        try:
            self.img1 = Image.open(nodo.value.imagen)
            self.img1 = self.img1.resize((360, 350), Image.LANCZOS)
            self.photoImg1 = ImageTk.PhotoImage(self.img1)
            self.lbl = Label(self.foto, image = self.photoImg1)
            self.lbl.place(x = 0,y = 0, width = 360, height = 350)
        except FileNotFoundError:
            print(FileNotFoundError)
    
    def setInfo(self, nombre, album, artista):
        self.labelCancion.config(text = "Canción {}".format(nombre))
        self.labelAlbum.config(text = "Album: {}".format(album))
        self.labelArtista.config(text = "Artista: {}".format(artista))
    
    def reproducir(self, cancion):
        if self.threadPlay is not None:
            self.threadPlay.raise_exception()
            self.threadPlay.join()

    # Crear un nuevo hilo para reproducir la canción actual
        self.threadPlay = TPlay(cancion.ruta)
        self.threadPlay.start()

    def playRandom(self):
        if self.playList.length > 0:
            # Convertir la lista circular a una lista
            lista_reproduccion_lista = self.playList.toList()

            # Barajar la lista
            random.shuffle(lista_reproduccion_lista)

            # Reconstruir la lista circular a partir de la lista barajada
            self.playList = ListaCircular()
            for cancion in lista_reproduccion_lista:
                self.playList.append(cancion)

            # Reproducir la primera canción en la lista barajada
            self.actualPlaylist = self.playList.head
            self.setInfo(self.actualPlaylist.value.nombre, self.actualPlaylist.value.album, self.actualPlaylist.value.artista)
            self.setPhoto(self.actualPlaylist)
            self.reproducir(self.actualPlaylist.value)
        else:
            messagebox.showwarning(title="¡Alerta!", message="No hay canciones en la lista de reproducción")
            

    def pause(self):
        if self.threadPlay != None:
            if self.threadPlay.estado != "p":
                self.threadPlay.estado = "p"
            else:
                self.threadPlay.estado = "r"
    
    def stop(self):
        if self.threadPlay != None:
            self.threadPlay.estado = "e"
    
    
    def reportes(self):
        if self.library != None:
            self.library.report()
            if self.listaPlayList.length > 0:
                string = """
digraph G{
    edge [weigth = 1000];
    subgraph listas{
        rankdir = LR;\n"""
                string2 = ""
                for i in range(self.listaPlayList.length):
                    lista = self.listaPlayList.getById(i)
                    string += '\t\t"{}"[color = beige style = "filled"];\n'.format(lista.nombre)
                    string2 +="\tsubgraph lista{}{}\n".format(i,"{")
                    string2 += "\t\trank = same;\n"
                    for j in range(lista.length):
                        cancion = lista.getById(j)
                        string2 += '\t\t"{}"[color = coral style = "filled"]\n'.format(cancion.nombre)
                    string2 += "\t}\n"
                string += '\t}\n'
                string += string2
                for i in range(self.listaPlayList.length):
                    lista = self.listaPlayList.getById(i)
                    if i+1 == self.listaPlayList.length:
                        string += '"{}"->"NoneL->"\n'.format(lista.nombre)
                    else:
                        siguiente = self.listaPlayList.getById(i+1)
                        string += '"{}"->"{}"\n'.format(lista.nombre, siguiente.nombre)
                    for j in range(lista.length):
                        cancion = lista.getById(j)
                        if j == 0:
                            string += '"{}"->"{}"'.format(lista.nombre, cancion.nombre)
                        if j+1 == lista.length:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(0).nombre)
                        else:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(j+1).nombre)
                for i in range(self.listaPlayList.length-1,-1,-1):
                    lista = self.listaPlayList.getById(i)
                    if i-1 == -1:
                        string += '"{}"->"<-NoneL"\n'.format(lista.nombre)
                    else:
                        siguiente = self.listaPlayList.getById(i-1)
                        string += '"{}"->"{}"\n'.format(lista.nombre, siguiente.nombre)
                    for j in range(lista.length-1,-1,-1):
                        cancion = lista.getById(j)
                        if j-1 == -1:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(lista.length-1).nombre)
                        else:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(j-1).nombre)
                string += '}'
                file = open("grafo_circular.dot", "w")
                file.write(string)
                file.close()
                os.system('dot -Tpng grafo_circular.dot -o grafo_circular.png')
            else:
                messagebox.showerror(message = "No se han creado listas de reproducción", title = "Error")
        else:
            messagebox.showerror(message = "No se ha cargado ninguna biblioteca", title = "Error")
    
    def saveList(self):
        self.playList.nombre = self.entryPlaylist.get()
        aux = self.playList
        self.playList = None
        contenedor = self.listaPlayList.contains(aux.nombre)
        print("Contenedor: {}".format(contenedor))
        if contenedor == None:
            self.listaPlayList.append(aux)
            valores = []
            for i in range(self.listaPlayList.length):
                valores.append(self.listaPlayList.getById(i).nombre)
                self.cbbListas["values"] = valores
        else:
            messagebox.showwarning(title = "Alerta!!!", message = "Ya existe una lista de reproducción con este nombre")
        self.addPlayList()
    
    
    def exportarListas(self):
        if self.listaPlayList.length > 0:
            xml = '<?xml version = "1.0" encoding="UTF-8"?>\n'
            xml += '<ListasReproduccion>\n'
            for i in range(self.listaPlayList.length):
                lista = self.listaPlayList.getById(i)
                xml += '\t<Lista nombre = "{}">\n'.format(lista.nombre)
                for j in range(lista.length):
                    cancion = lista.getById(j)
                    xml += '\t\t<cancion nombre = "{}"\n'.format(cancion.nombre)
                    xml += '\t\t\t<artista>{}</artista>\n'.format(cancion.artista)
                    xml += '\t\t\t<album>{}</album>\n'.format(cancion.album)
                    xml += '\t\t\t<vecesReproducida>{}</vecesReproducida>\n'.format(0)
                    xml += '\t\t\t<imagen>{}</imagen>\n'.format(cancion.imagen)
                    xml += '\t\t\t<ruta>{}</ruta>\n'.format(cancion.ruta)
                    xml += '\t\t</cancion>\n'
                xml += '\t</Lista>\n'
            xml += '</ListasReproduccion>\n'
            file = open("Listas_de_reproducción.xml", "w")
            file.write(xml)
            file.close()
    
    def exportar_listas_html(self):
        if self.listaPlayList.length > 0:
            html = '<!DOCTYPE html>\n'
            html += '<html>\n<head>\n<title>Informe de Listas de Reproducción</title>\n'
            # Ajustes en tamaño y color de las letras
            html += '<style>ul { list-style-type: none; } .bar-container { margin-top: 20px; } .bar { display: inline-block; margin-bottom: 10px; position: relative; height: 30px; } .bar-label { position: absolute; top: 5px; left: 100%; transform: translateX(-100%); font-weight: bold; font-size: 14px; color: white; } .song-name { margin-bottom: 5px; font-size: 12px; color: #333; } </style>\n'
            html += '</head>\n<body>\n'
            html += '<h1>Listas de Reproducción</h1>\n'

            for i in range(self.listaPlayList.length):
                lista = self.listaPlayList.getById(i)
                html += '<h2>{}</h2>\n'.format(lista.nombre)
                html += '<ul>\n'

                for j in range(lista.length):
                    cancion = lista.getById(j)
                    html += '<li>\n'
                    html += '<p>Nombre: {}</p>\n'.format(cancion.nombre)
                    html += '<p>Artista: {}</p>\n'.format(cancion.artista)
                    html += '<p>Veces Reproducida: 1</p>\n'
                    html += '<p>Portada: <img src="{}" alt="{}" style="width: 90px; height: 90px;"></p>\n'.format(cancion.imagen, cancion.nombre)
                    html += '</li>\n'

                html += '</ul>\n'

            # Agregar un gráfico de barras simple con solo HTML y CSS
            html += '<h2>Gráfico de Reproducciones</h2>\n'
            html += '<div class="bar-container" style="font-size: 16px;">\n'

            colores = ['blue', 'green', 'red', 'orange', 'purple']  # Lista de colores

            for j in range(lista.length):
                cancion = lista.getById(j)
                color = colores[j % len(colores)]  # Ciclo a través de los colores
                reproducciones = 1  # Reemplaza esto con la cantidad real de reproducciones
                ancho_barra = 100  # Ajusta el ancho de la barra
                alto_barra = 150  # Ajusta el alto de la barra
                html += '<div class="bar" style="width: {}px; height: {}px; background-color: {};">\n'.format(ancho_barra, alto_barra, color)
                # Ajustes en tamaño y color del nombre de la canción
                html += '<div class="song-name" style="font-size: 11px; color: #ffffff;">{}</div>\n'.format(cancion.nombre)
                html += '<div class="bar-label">{}</div>\n'.format(reproducciones)
                html += '</div>\n'

            html += '</div>\n'

            html += '</body>\n</html>'

            with open("Informe_Listas_de_Reproduccion.html", "w") as file:
                file.write(html)

            webbrowser.open("Informe_Listas_de_Reproduccion.html")


