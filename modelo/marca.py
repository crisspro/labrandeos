class Data():
    def __init__(self, *ARGS, **KWARGS):
        self.id = 0
        self.titulo = ''
        self.autor = ''
        self.tiempo_inicio = 0
        self.milesimas = 0

        ''' lista de  marcas. '''
        self.lista_marcas = []

    # añade una nueva marca a la lista.
    def agregarMarca(self, marca):
        self.lista_marcas.append(marca)

    def ordenar(self):
        ''' ordena las marcas '''
        self.lista_marcas.sort(key=lambda marca: marca.milesimas)
        id = 0
        for marca in self.lista_marcas:
            marca.id = id + 1
            id = id + 1

    def editarMarca(self, id, marca):
        self.lista_marcas[id] = marca

    def borrar_marca(self, id):
        self.lista_marcas.pop(id)

    # limpia la lista de marcas.
    def limpiar(self):
        self.lista_marcas.clear()
        self.titulo = ''
        self.autor = ''

    def es_vacia(self):
        return self.lista_marcas == []

    def getMarcas(self):
        return self.lista_marcas

    def __eq__(self, otro):
        if isinstance(otro, Data) and len(otro.lista_marcas) == len(self.lista_marcas):
            for i, j in zip(otro.lista_marcas, self.lista_marcas):
                valor = vars(i) == vars(j)
                if valor is False:
                    break
                    return False
                else:
                    return True
        else:
            return False


class Marca():
    def __init__(self, id, titulo, autor, tiempo_inicio, milesimas):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.tiempo_inicio = tiempo_inicio
        self.milesimas = milesimas

    def filtrar_tiempo_inicio_cue(self):
        tiempo = self.tiempo_inicio.split()
        minutos = int(tiempo[0]) * 60 + int(tiempo[2])
        tiempo = f'{minutos}:{tiempo[4].zfill(2)}:{tiempo[6].zfill(2)}'
        return tiempo
