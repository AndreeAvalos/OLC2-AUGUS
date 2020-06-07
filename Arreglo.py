class Arreglo:
    def __init__(self):
        self.diccionario = {}
    #Direcciones es un arreglo de indices
    #valor es el valor que se desea guardar
    def add(self,direcciones, valor):
        temporal = self.diccionario
        for x in range(len(direcciones)):
            new_dic={}
            if(x+1) == len(direcciones):
                temporal[direcciones[x]] = valor
            else:
                temporal[direcciones[x]] = new_dic
            temporal = new_dic
