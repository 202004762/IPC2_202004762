class Nodo:
    def __init__(self, value, id):
        self.value = value
        self.id = id
        self.siguiente = None
        self.anterior = None
    
    
    def __str__(self) -> str:
        return str(self.value)


