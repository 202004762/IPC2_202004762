from Nodo import *

class ListaDoble:
    def __init__(self):
        self.length = 0
        self.cabeza = None
        self.cola = None


    def append(self, value):
        nuevo = Nodo(value, self.length)
        if self.cabeza == None:
            self.cabeza = nuevo
            self.cola = self.cabeza
        else:
            actual = self.cola
            nuevo.anterior = actual
            self.cola = nuevo
            actual.siguiente = self.cola
        self.length += 1



    def getById(self, id):
        if self.cabeza == None:
            return "No hay cabeza"
        else:
            if id < 0 or id >= self.length:
                return "Fuera de rango"
            else:
                actual = self.cabeza
                while actual.id != id:
                    actual = actual.siguiente
                return actual.value



    def contains(self, nombre):
        if self.cabeza == None:
            return None
        else:
            actual = self.cabeza
            while actual != None:
                if actual.value.nombre == nombre:
                    break
                else:
                    actual = actual.siguiente
            if actual != None:
                return actual.id
            else:
                return None


    def __str__(self):
        if self.cabeza == None:
            return "[]"
        else:
            string = "["
            actual = self.cabeza
            while actual != None:
                if actual.siguiente == None:
                    string += "{}]".format(actual)
                else:
                    string += "{},".format(actual)
                actual = actual.siguiente
            return string















