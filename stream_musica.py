# trabjo 
# primero importamos lo paquetes que quizas vayamos a necesitar 
from abc import ABC, abstractmethod
import random
from functools import reduce
import math
# empezamos creando cancion ya que no forma parte de ninguns intancia de tipo , singleton etc 


class cancion : 
    def __init__ ( self, id , titulo, atributos_sonoros , atributos_sentimentales ): 
        self.id = id 
        self.titulo = titulo 
        self.atributos_sonoros = atributos_sonoros# es un diccionario 
        self.atributos_sentimentales = atributos_sentimentales  #  es un diccionario 

    def get_atributos_sonoros(self): 
        return self.atributos_sonoros
    def get_atributos_sentimentales ( self ): 
        return self.atributos_sentimentales 
        

# ahora hacemos la class playlist 
class playlist: 
    def __init__(self, id , fechacreacion , canciones): 
        self.id = id 
        self.fechacreacion = fechacreacion
        self.canciones = canciones 

    def calcular_media_conora(self): 
        if not self.canciones : 
            return {}
        # obtengo las claves del primer elemento 
        claves = self.canciones[0].get_atributos_sonoros().keys 
        dic_medias = {} #lo guardamos en un diccionario porque puede haber varios tipos , entomces guardamos la media para cada tipo 
        for clave in claves :
            valores = list(map(lambda x : x.get_atributos_sonoros()[clave],self.canciones))
            dic_medias[clave] = sum(valores)/len(self.canciones)
        return dic_medias
    
    def calcular_media_sentimental ( self ): 
         if not self.canciones : 
            return {}
        # obtengo las claves del primer elemento 
         claves = self.canciones[0].get_atributos_sentimentales().keys 
         dic_medias = {}
         for clave in claves :
            valores = list(map(lambda x : x.get_atributos_sentimentales()[clave],self.canciones))
            dic_medias[clave] = sum(valores)/len(self.canciones)
         return dic_medias





class artista: 
    def __init__(self, nombre, fecha_nacimiento , canciones): 
        self.nombre = nombre 
        self.fecha_nacimiento = fecha_nacimiento 
        self.canciones = canciones

    def  get_atributos_sonoros ( self ): 
        return list(map(lambda x : x.get_atributos_sonoros(), self.canciones))
    def get_atributos_sentimentales ( self): 
        return list(map(lambda x : x.get_atributos_sentimentales(), self.canciones))
    
    def calcular_media_sentimental ( self ): 
         if not self.canciones : 
            return {}
        # obtengo las claves del primer elemento 
         claves = self.canciones[0].get_atributos_sentimentales().keys 
         dic_medias = {}
         for clave in claves :
            valores = list(map(lambda x : x.get_atributos_sentimentales()[clave],self.canciones))
            dic_medias[clave] = sum(valores)/len(self.canciones)
         return dic_medias


class catalogo : 
    def __init__(self,canciones , artistas , playlist ): 
        self.canciones = canciones
        self.artistas = artistas 
        self.playlist = playlist 

    def get_canciones ( self): 
        return self.canciones 
    def get_artistas (self ): 
        return self.artistas
    def get_playlist(self): 
        return self.playlist
    def get_cancion_por_id ( self ,id): 
         for x in self.canciones: 
            if x.id == id:
                return x
            return None 



#vamos ahora a por la cadena de responsabilidad 

class SesionEscucha:
    def __init__(self, ventana_max, manejador):
        self.ventana_max = ventana_max
        self.canciones = []
        self.manejador = manejador
        self.stats = {}

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

        if len(self.canciones) > self.ventana_max:
            self.canciones.pop(0)

        # ponemos aqui la cadena de responsabilidad para calcular los stats cada vez que se añade una canción
        self.stats = self.manejador.manejar_stat(self.canciones, {})


class ManejadorStat(ABC):

    def __init__(self, sucesor):
        self.sucesor = sucesor
        self.stat = {}

    def siguiente_stat(self, sucesor, stats):
        self.sucesor = sucesor

    @abstractmethod
    def manejar_stat(self, cancion, stats):

        if self.sucesor:
            return self.sucesor.manejar_stat(cancion, stats)

        return stats


class ManejadorSonor(ManejadorStat):

    def manejar_stat(self, canciones, stats):

        if not canciones:
            stats["sonoros"] = {}
            return stats

        propiedades = canciones[0].get_atributos_sonoros().keys()

        medias = {}
        des_tipica = {}

        for k in propiedades:

            valores = [c.get_atributos_sonoros()[k] for c in canciones]

            media[k]=reduce(lambda acc, x: acc + x, valores, 0) / len(valores)
            m=media[k]

            varianza = reduce(lambda acc, x: acc + (x - m) ** 2, valores, 0) / len(valores)            
            des_tipica[k] = math.sqrt(varianza)

        stats["sonoros"] = {
            "media": medias,
            "desviacion": des_tipica
        }

        if self.sucesor:
            return self.sucesor.manejar_stat(canciones, stats)

        return stats

class ManejadorSentimientos(ManejadorStat): 
    def manejador_stat(self,cancion,stats): 
        if not cancion:
            return stats["sentimientos"]={}
        propiedades=cancion[0].get_atributos_sentimentales().keys()
        medias={}
        des_tipica={}
        for k in propiedades:
            valores=[c.get_atributos_sentimentales[k] for c in canciones]
            media[k]=reduce(lambda acc, x: acc + x, valores, 0) / len(valores)
            m=media[k]
            varianza = reduce(lambda acc, x: acc + (x - m) ** 2, valores, 0) / len(valores)
            des_tipica[k]=math.sqrt(varianza)
        
        stats["sentimientos"] = {
            "media": medias,
            "desviacion": des_tipica
        }

        if self.sucesor:
            return self.sucesor.manejar(canciones, stats)
        return stats
    
#ahora pasamos al decorador:

class GeneradorRecomendador(SistemaRecomendador,EstrategiaBusqueda):
    def __init__(self,catalogo,sesion,estrategia):
        self.catalogo=catalogo #Catalogo
        self.sesion=sesion #SesionEscucha
        self.estrategia=estrategia #EstrategiaBusqueda
    
    def recomendar(self):
        pass

class RecomendarCancion(GeneradorRecomendador):
    def recomendar(self):

        def similitud(dic1, dic2):
            return reduce(lambda acc, k: acc + (1 - abs(dic1[k] - dic2[k])),dic1.keys(),0) / len(dic1)
        
        # 1. estadísticas de sesión
        stats_sonoros = self.sesion.get_sonor_sat()
        stats_sentimentales = self.sesion.get_sentimental_sat()

        mejor = None
        mejor_score = -1

        # 2. aplicar estrategia de orden
        elementos = self.estrategia.ordenar(self.catalogo.get_canciones())

        # 3. recorrer catálogo
        for cancion in elementos:

            s_sono = cancion.get_atributos_sonoros()
            s_sent = cancion.get_atributos_sentimentales()

            score = (
                similitud(stats_sonoros, s_sono) +
                similitud(stats_sentimentales, s_sent)
            ) / 2

            #criterio de match
            if score > mejor_score:
                mejor_score = score
                mejor = cancion

        return mejor


