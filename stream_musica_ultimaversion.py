# primero importamos los paquetes que quizas vayamos a necesitar
from abc import ABC, abstractmethod
import random
from functools import reduce
import math
from datetime import datetime

class cancion:
    def __init__(self, id, fecha_creacion, titulo, atributos_sonoros, atributos_sentimentales):
        try:
            self.id = id
            self.fecha_creacion = fecha_creacion
            self.titulo = titulo
            self.atributos_sonoros = atributos_sonoros          # diccionario
            self.atributos_sentimentales = atributos_sentimentales  # diccionario
        except Exception as e: # ponemos un except para captar cualquier error 
            raise ValueError(f"[cancion.__init__] Error al crear canción: {e}") from e

    def get_atributos_sonoros(self):
        try:
            return self.atributos_sonoros
        except Exception as e:
            raise RuntimeError(f"[cancion.get_atributos_sonoros] {e}") from e

    def get_atributos_sentimentales(self):
        try:
            return self.atributos_sentimentales
        except Exception as e:
            raise RuntimeError(f"[cancion.get_atributos_sentimentales] {e}") from e


class playlist:
    def __init__(self, id, titulo, fecha_creacion, canciones):
        try:
            self.id = id
            self.fecha_creacion = fecha_creacion
            self.canciones = canciones
            self.titulo = titulo
        except Exception as e:
            raise ValueError(f"[playlist.__init__] Error al crear playlist: {e}") from e

    def calcular_media_sonora(self):
        try:
            if not self.canciones:
                return {}
            claves = self.canciones[0].get_atributos_sonoros().keys()
            dic_medias = {}
            for clave in claves:
                valores = list(map(lambda x: x.get_atributos_sonoros()[clave], self.canciones)) # usamos map para extraer todos lo valores 
                dic_medias[clave] = sum(valores) / len(self.canciones)
            return dic_medias
        except Exception as e:
            raise RuntimeError(f"[playlist.calcular_media_sonora] {e}") from e

    def calcular_media_sentimental(self):
        try:
            if not self.canciones:
                return {}
            claves = self.canciones[0].get_atributos_sentimentales().keys()
            dic_medias = {}
            for clave in claves:
                valores = list(map(lambda x: x.get_atributos_sentimentales()[clave], self.canciones))
                dic_medias[clave] = sum(valores) / len(self.canciones)
            return dic_medias
        except Exception as e:
            raise RuntimeError(f"[playlist.calcular_media_sentimental] {e}") from e


class artista:
    def __init__(self, nombre, fecha_nacimiento, canciones):
        try:
            self.nombre = nombre
            self.fecha_nacimiento = fecha_nacimiento
            self.canciones = canciones
        except Exception as e:
            raise ValueError(f"[artista.__init__] Error al crear artista: {e}") from e

    def get_atributos_sonoros(self):
        try:
            return list(map(lambda x: x.get_atributos_sonoros(), self.canciones))
        except Exception as e:
            raise RuntimeError(f"[artista.get_atributos_sonoros] {e}") from e

    def get_atributos_sentimentales(self):
        try:
            return list(map(lambda x: x.get_atributos_sentimentales(), self.canciones))
        except Exception as e:
            raise RuntimeError(f"[artista.get_atributos_sentimentales] {e}") from e

    def calcular_media_sentimental(self):
        try:
            if not self.canciones:
                return {}
            claves = self.canciones[0].get_atributos_sentimentales().keys()
            dic_medias = {}
            for clave in claves:
                valores = list(map(lambda x: x.get_atributos_sentimentales()[clave], self.canciones))
                dic_medias[clave] = sum(valores) / len(self.canciones)
            return dic_medias
        except Exception as e:
            raise RuntimeError(f"[artista.calcular_media_sentimental] {e}") from e

    def calcular_media_sonora(self):
        try:
            if not self.canciones:
                return {}
            claves = self.canciones[0].get_atributos_sonoros().keys()
            dic_medias = {}
            for clave in claves:
                valores = list(map(lambda x: x.get_atributos_sonoros()[clave], self.canciones))
                dic_medias[clave] = sum(valores) / len(self.canciones)
            return dic_medias
        except Exception as e:
            raise RuntimeError(f"[artista.calcular_media_sonora] {e}") from e


class catalogo:
    def __init__(self, canciones, artistas, playlist):
        try:
            self.canciones = canciones
            self.artistas = artistas
            self.playlist = playlist
        except Exception as e:
            raise ValueError(f"[catalogo.__init__] Error al crear catálogo: {e}") from e

    def get_canciones(self):
        return self.canciones

    def get_artistas(self):
        return self.artistas

    def get_playlist(self):
        return self.playlist

    def get_cancion_por_id(self, id):
        try:
            for x in self.canciones:
                if x.id == id:
                    return x
            return None
        except Exception as e:
            raise RuntimeError(f"[catalogo.get_cancion_por_id] {e}") from e

class SesionEscucha:
    def __init__(self, ventana_max, manejador):
        try:
            self.ventana_max = ventana_max
            self.canciones = []
            self.manejador = manejador
            self.stats = {}
        except Exception as e:
            raise ValueError(f"[SesionEscucha.__init__] {e}") from e

    def agregar_cancion(self, cancion):
        try:
            self.canciones.append(cancion)
            if len(self.canciones) > self.ventana_max:
                self.canciones.pop(0)
            # cadena de responsabilidad: recalcula stats tras cada adición
            self.stats = self.manejador.manejar_stat(self.canciones, {})
        except Exception as e:
            raise RuntimeError(f"[SesionEscucha.agregar_cancion] {e}") from e

    def get_sonor_stat(self):
        return self.stats.get("sonoros", {})

    def get_sentimental_stat(self):
        return self.stats.get("sentimientos", {})

# creamoa manejador que es una clase abstracta que se encarga de las stadisticas 
class ManejadorStat(ABC):
    def __init__(self, sucesor=None):
        try:
            self.sucesor = sucesor
            self.stat = {}
        except Exception as e:
            raise ValueError(f"[ManejadorStat.__init__] {e}") from e

    def siguiente_stat(self, sucesor):
        
        self.sucesor = sucesor

    @abstractmethod
    def manejar_stat(self, canciones, stats):
        if self.sucesor:
            return self.sucesor.manejar_stat(canciones, stats)
        return stats


class ManejadorSonor(ManejadorStat):
    def manejar_stat(self, canciones, stats):
        try:
            if not canciones:
                stats["sonoros"] = {}
                return stats if not self.sucesor else self.sucesor.manejar_stat(canciones, stats)

            propiedades = canciones[0].get_atributos_sonoros().keys()
            medias = {}
            des_tipica = {}

            for k in propiedades:
                valores = [c.get_atributos_sonoros()[k] for c in canciones]
                medias[k] = reduce(lambda acc, x: acc + x, valores, 0) / len(valores)
                m = medias[k]
                varianza = reduce(lambda acc, x: acc + (x - m) ** 2, valores, 0) / len(valores)
                des_tipica[k] = math.sqrt(varianza)

            stats["sonoros"] = {"media": medias, "desviacion": des_tipica}

            if self.sucesor:
                return self.sucesor.manejar_stat(canciones, stats)
            return stats
        except Exception as e:
            raise RuntimeError(f"[ManejadorSonor.manejar_stat] {e}") from e


class ManejadorSentimientos(ManejadorStat):
    
    def manejar_stat(self, canciones, stats):
        try:
            if not canciones:
                stats["sentimientos"] = {}
                return stats if not self.sucesor else self.sucesor.manejar_stat(canciones, stats)

            propiedades = canciones[0].get_atributos_sentimentales().keys()
            medias = {}
            des_tipica = {}

            for k in propiedades:
                valores = [c.get_atributos_sentimentales()[k] for c in canciones]
                medias[k] = reduce(lambda acc, x: acc + x, valores, 0) / len(valores)
                m = medias[k]
                varianza = reduce(lambda acc, x: acc + (x - m) ** 2, valores, 0) / len(valores)
                des_tipica[k] = math.sqrt(varianza)

            stats["sentimientos"] = {"media": medias, "desviacion": des_tipica}

            if self.sucesor:
               
                return self.sucesor.manejar_stat(canciones, stats)
            return stats
        except Exception as e:
            raise RuntimeError(f"[ManejadorSentimientos.manejar_stat] {e}") from e



class EstrategiaBusqueda(ABC):
    @abstractmethod
    def buscar(self, catalogo, sesion, modo):
        pass

    def match(self, item, sesion):
        try:
            if not sesion.stats:
                return True  # sin stats todo hace match

            media_sonora = sesion.stats.get("sonoros", {}).get("media", {})
            media_sentimental = sesion.stats.get("sentimientos", {}).get("media", {})

            if isinstance(item, cancion):
                atributos_sonoros = item.get_atributos_sonoros()
                atributos_sentimentales = item.get_atributos_sentimentales()
            else:
                atributos_sonoros = item.calcular_media_sonora()
                atributos_sentimentales = item.calcular_media_sentimental()

            def calcular(d1, d2):
                if not d1 or not d2:
                    return 1
                return sum(abs(d1[c] - d2[c]) for c in d1 if c in d2) / len(d1)

            diferencia_total = (calcular(media_sonora, atributos_sonoros) +
                                calcular(media_sentimental, atributos_sentimentales)) / 2
            return diferencia_total < 0.2
        except Exception as e:
            raise RuntimeError(f"[EstrategiaBusqueda.match] {e}") from e


class orden_alfabetico(EstrategiaBusqueda):
    def buscar(self, catalogo, sesion, modo):
        try:
            if modo == "canciones":
                elementos = catalogo.get_canciones()
            elif modo == "artistas":
                elementos = catalogo.get_artistas()
            elif modo == "playlist":
                elementos = catalogo.get_playlist()
            else:
                raise ValueError(f"Modo desconocido: {modo}")

            ordenado = sorted(
                elementos,
                key=lambda x: x.titulo if isinstance(x, (cancion, playlist)) else x.nombre
            )
            for e in ordenado:
                if self.match(e, sesion):
                    return e
            return None
        except Exception as e:
            raise RuntimeError(f"[orden_alfabetico.buscar] {e}") from e


class forma_aleatoria(EstrategiaBusqueda):
    
    def buscar(self, catalogo, sesion, modo):
        try:
            if modo == "canciones":
                elementos = catalogo.get_canciones()
            elif modo == "artistas":
                elementos = catalogo.get_artistas()
            elif modo == "playlist":
                elementos = catalogo.get_playlist()
            else:
                raise ValueError(f"Modo desconocido: {modo}")

            if not elementos:
                return None

            intentos = 0
            max_intentos = len(elementos) * 10  # evitar bucle infinito
            while intentos < max_intentos:
                candidato = random.choice(elementos)
                if self.match(candidato, sesion):
                    return candidato
                intentos += 1
            return None  # ninguno hizo match tras muchos intentos
        except Exception as e:
            raise RuntimeError(f"[forma_aleatoria.buscar] {e}") from e


class orden_temporal(EstrategiaBusqueda):
    def buscar(self, catalogo, sesion, modo):
        try: # vemos que modo se ha elegido con un try e igualando 
            if modo == "canciones":
                elementos = catalogo.get_canciones()
            elif modo == "artistas":
                elementos = catalogo.get_artistas()
            elif modo == "playlist":
                elementos = catalogo.get_playlist()
            else:
                raise ValueError(f"Modo desconocido: {modo}")

            ordenado = sorted(
                elementos,
                key=lambda x: x.fecha_creacion if isinstance(x, (playlist, cancion)) else x.fecha_nacimiento,
                reverse=True
            )
            for e in ordenado:
                
                if self.match(e, sesion):
                    return e
            return None
        except Exception as e:
            raise RuntimeError(f"[orden_temporal.buscar] {e}") from e


class GeneradorRecomendador(ABC):
    def __init__(self, catalogo, sesion, estrategia):
        try:
            self.catalogo = catalogo      # Catalogo
            self.sesion = sesion          # SesionEscucha
            self.estrategia = estrategia  # EstrategiaBusqueda
        except Exception as e:
            raise ValueError(f"[GeneradorRecomendador.__init__] {e}") from e

    @abstractmethod
    # debe ser abstracto según el diagrama; los hijos usan self.x
    def recomendar(self):
        pass


class RecomendarCancion(GeneradorRecomendador):
    def recomendar(self):
        # el original recibía catalogo/sesion/estrategia como params
        # pero ya los tiene en self; además el key tenía un espacio extra
        try:
            recomendado = self.estrategia.buscar(self.catalogo, self.sesion, modo="canciones")
            if isinstance(recomendado, cancion):
                return {"cancion": recomendado}
            return {"item_recomendado": recomendado}
        except Exception as e:
            raise RuntimeError(f"[RecomendarCancion.recomendar] {e}") from e


class RecomendadorArtista(GeneradorRecomendador):
    def recomendar(self):
        try:
            recomendado = self.estrategia.buscar(self.catalogo, self.sesion, modo="artistas")
            if isinstance(recomendado, artista):
                return {"artista": recomendado}
            return {"item_recomendado": recomendado}
        except Exception as e:
            raise RuntimeError(f"[RecomendadorArtista.recomendar] {e}") from e


class RecomendadorPlaylist(GeneradorRecomendador):
    def recomendar(self):
        try:
            recomendado = self.estrategia.buscar(self.catalogo, self.sesion, modo="playlist")
            if isinstance(recomendado, playlist):
                return {"playlist": recomendado}
            return {"item_recomendado": recomendado}
        except Exception as e:
            raise RuntimeError(f"[RecomendadorPlaylist.recomendar] {e}") from e

class Usuario:
    def __init__(self, id, nombre, sesion: SesionEscucha, fecha_registro: datetime):
        try:
            self.id = id
            self.nombre = nombre
            self.sesion = sesion
            self.fecha_registro = fecha_registro
        except Exception as e:
            raise ValueError(f"[Usuario.__init__] {e}") from e

    def escuchar_cancion(self, c: cancion, fecha_hora: datetime):
        try:
            self.sesion.agregar_cancion(c)
        except Exception as e:
            raise RuntimeError(f"[Usuario.escuchar_cancion] {e}") from e

    def get_sesion(self):
        return self.sesion

    def pedir_recomendacion(self, recomendador: GeneradorRecomendador):
        try:
            return recomendador.recomendar()
        except Exception as e:
            raise RuntimeError(f"[Usuario.pedir_recomendacion] {e}") from e


# creamos el singleton j, qie es el que se encarga de gestionar las recomendaciones en todo el sistema 
class Sistema_recomendador:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        try:
            self.canciones: list[cancion] = []
            self.artistas: list[artista] = []
            self.playlists: list[playlist] = []
            self.catalogo_actual: catalogo = None
            self.estrategia_actual: EstrategiaBusqueda = None
            self._inicializado = True
        except Exception as e:
            raise RuntimeError(f"[Sistema_recomendador.__init__] {e}") from e

    def configurar_recomendacion(self, cat: catalogo, estrategia: EstrategiaBusqueda):
        try:
            self.catalogo_actual = cat
            self.estrategia_actual = estrategia
        except Exception as e:
            raise RuntimeError(f"[Sistema_recomendador.configurar_recomendacion] {e}") from e

    def get_recomendacion(self, tipo: str, sesion: SesionEscucha, estrategia: EstrategiaBusqueda = None):
        """tipo: 'canciones' | 'artistas' | 'playlist'"""
        try:
            est = estrategia or self.estrategia_actual
            cat = self.catalogo_actual
            if cat is None:
                raise ValueError("El catálogo no está configurado.")

            if tipo == "canciones":
                rec = RecomendarCancion(cat, sesion, est)
            elif tipo == "artistas":
                rec = RecomendadorArtista(cat, sesion, est)
            elif tipo == "playlist":
                rec = RecomendadorPlaylist(cat, sesion, est)
            else:
                raise ValueError(f"Tipo desconocido: {tipo}")

            return rec.recomendar()
        except Exception as e:
            raise RuntimeError(f"[Sistema_recomendador.get_recomendacion] {e}") from e

    def establecer_estrategia(self, estrategia: EstrategiaBusqueda):
        try:
            self.estrategia_actual = estrategia
        except Exception as e:
            raise RuntimeError(f"[Sistema_recomendador.establecer_estrategia] {e}") from e

    def pedir_recomendacion_di(self, usuario: Usuario, tipo: str, fecha_hora: datetime):
        """Atajo: pide recomendación directamente desde un usuario."""
        try:
            return self.get_recomendacion(tipo, usuario.get_sesion())
        except Exception as e:
            raise RuntimeError(f"[Sistema_recomendador.pedir_recomendacion_di] {e}") from e
        


# atributos_sonoros:            ritmo, tono, escala_melodica,
#                               distorsion, densidad_armonica
# atributos_sentimentales:      felicidad, bailabilidad, energia,
#                               nostalgia, agresividad
# Todos los valores están en la escala 0.0 – 1.0

# empezamos con el programa principal para verificar que nuestro codigo funciona 

if __name__ == "__main__":
    from kafka import KafkaConsumer
    import threading
    import json
 
    # **************************************************************************
    # LEYENDA DE ATRIBUTOS
    #
    # SONOROS
    #   ritmo            → velocidad/pulso percibido  (0=lentísimo, 1=frenético)
    #   tono             → altura dominante           (0=muy grave, 1=muy agudo)
    #   escala_melodica  → carácter de la escala      (0=menor/oscura, 1=mayor/brillante)
    #   distorsion       → cantidad de overdrive/fuzz (0=limpio, 1=saturado al máximo)
    #   densidad_armonica→ riqueza de capas sonoras   (0=minimalista, 1=orquestal/denso)
    #
    # SENTIMENTALES
    #   felicidad   → emoción positiva transmitida    (0=desolador, 1=eufórico)
    #   bailabilidad→ impulso a moverse               (0=nada bailable, 1=irresistible)
    #   energia     → vitalidad/activación            (0=relajante, 1=explosivo)
    #   nostalgia   → evocación del pasado            (0=nada nostálgico, 1=muy nostálgico)
    #   agresividad → carga confrontacional           (0=dulce, 1=rabioso)
    # ***************************************************************************
 
    #NIRVANA 
    c01 = cancion(1, datetime(1991, 9, 10), "Smells Like Teen Spirit",
        {"ritmo": 0.76, "tono": 0.45, "escala_melodica": 0.20,
         "distorsion": 0.92, "densidad_armonica": 0.55},
        {"felicidad": 0.25, "bailabilidad": 0.60, "energia": 0.95,
         "nostalgia": 0.50, "agresividad": 0.88})
 
    c02 = cancion(2, datetime(1993, 9, 13), "Heart-Shaped Box",
        {"ritmo": 0.55, "tono": 0.38, "escala_melodica": 0.15,
         "distorsion": 0.85, "densidad_armonica": 0.45},
        {"felicidad": 0.15, "bailabilidad": 0.35, "energia": 0.78,
         "nostalgia": 0.60, "agresividad": 0.72})
 
    #BLACK SABBATH 
    c03 = cancion(3, datetime(1970, 2, 13), "Black Sabbath",
        {"ritmo": 0.30, "tono": 0.15, "escala_melodica": 0.05,
         "distorsion": 0.95, "densidad_armonica": 0.50},
        {"felicidad": 0.05, "bailabilidad": 0.20, "energia": 0.88,
         "nostalgia": 0.30, "agresividad": 0.95})
 
    c04 = cancion(4, datetime(1971, 9, 18), "War Pigs",
        {"ritmo": 0.40, "tono": 0.20, "escala_melodica": 0.10,
         "distorsion": 0.93, "densidad_armonica": 0.60},
        {"felicidad": 0.08, "bailabilidad": 0.25, "energia": 0.90,
         "nostalgia": 0.35, "agresividad": 0.92})
 
    # AC/DC 
    c05 = cancion(5, datetime(1980, 7, 25), "Back in Black",
        {"ritmo": 0.72, "tono": 0.40, "escala_melodica": 0.30,
         "distorsion": 0.88, "densidad_armonica": 0.45},
        {"felicidad": 0.50, "bailabilidad": 0.65, "energia": 0.92,
         "nostalgia": 0.55, "agresividad": 0.80})
 
    c06 = cancion(6, datetime(1979, 10, 22), "Highway to Hell",
        {"ritmo": 0.75, "tono": 0.42, "escala_melodica": 0.35,
         "distorsion": 0.85, "densidad_armonica": 0.42},
        {"felicidad": 0.55, "bailabilidad": 0.70, "energia": 0.90,
         "nostalgia": 0.50, "agresividad": 0.78})
 
    #GUNS N' ROSES 
    c07 = cancion(7, datetime(1987, 7, 21), "Welcome to the Jungle",
        {"ritmo": 0.74, "tono": 0.50, "escala_melodica": 0.25,
         "distorsion": 0.90, "densidad_armonica": 0.65},
        {"felicidad": 0.30, "bailabilidad": 0.60, "energia": 0.95,
         "nostalgia": 0.40, "agresividad": 0.88})
 
    c08 = cancion(8, datetime(1992, 2, 11), "November Rain",
        {"ritmo": 0.38, "tono": 0.55, "escala_melodica": 0.55,
         "distorsion": 0.35, "densidad_armonica": 0.85},
        {"felicidad": 0.30, "bailabilidad": 0.25, "energia": 0.55,
         "nostalgia": 0.88, "agresividad": 0.25})
 
    #LED ZEPPELIN 
    c09 = cancion(9, datetime(1971, 11, 8), "Stairway to Heaven",
        {"ritmo": 0.35, "tono": 0.50, "escala_melodica": 0.50,
         "distorsion": 0.45, "densidad_armonica": 0.80},
        {"felicidad": 0.40, "bailabilidad": 0.20, "energia": 0.65,
         "nostalgia": 0.85, "agresividad": 0.30})
 
    c10 = cancion(10, datetime(1969, 1, 12), "Whole Lotta Love",
        {"ritmo": 0.80, "tono": 0.45, "escala_melodica": 0.30,
         "distorsion": 0.88, "densidad_armonica": 0.55},
        {"felicidad": 0.50, "bailabilidad": 0.65, "energia": 0.95,
         "nostalgia": 0.45, "agresividad": 0.85})
 
    #MICHAEL JACKSON 
    c11 = cancion(11, datetime(1982, 11, 30), "Billie Jean",
        {"ritmo": 0.78, "tono": 0.60, "escala_melodica": 0.55,
         "distorsion": 0.08, "densidad_armonica": 0.70},
        {"felicidad": 0.50, "bailabilidad": 0.92, "energia": 0.82,
         "nostalgia": 0.60, "agresividad": 0.10})
 
    c12 = cancion(12, datetime(1983, 1, 2), "Beat It",
        {"ritmo": 0.82, "tono": 0.58, "escala_melodica": 0.45,
         "distorsion": 0.55, "densidad_armonica": 0.72},
        {"felicidad": 0.55, "bailabilidad": 0.85, "energia": 0.88,
         "nostalgia": 0.55, "agresividad": 0.48})
 
    #THE BEATLES 
    c13 = cancion(13, datetime(1969, 9, 26), "Come Together",
        {"ritmo": 0.62, "tono": 0.45, "escala_melodica": 0.40,
         "distorsion": 0.30, "densidad_armonica": 0.60},
        {"felicidad": 0.45, "bailabilidad": 0.65, "energia": 0.70,
         "nostalgia": 0.72, "agresividad": 0.20})
 
    c14 = cancion(14, datetime(1967, 6, 1), "Lucy in the Sky with Diamonds",
        {"ritmo": 0.50, "tono": 0.65, "escala_melodica": 0.70,
         "distorsion": 0.12, "densidad_armonica": 0.75},
        {"felicidad": 0.75, "bailabilidad": 0.45, "energia": 0.55,
         "nostalgia": 0.80, "agresividad": 0.05})
 
    #PINK FLOYD 
    c15 = cancion(15, datetime(1973, 3, 1), "Money",
        {"ritmo": 0.60, "tono": 0.42, "escala_melodica": 0.35,
         "distorsion": 0.50, "densidad_armonica": 0.65},
        {"felicidad": 0.38, "bailabilidad": 0.52, "energia": 0.70,
         "nostalgia": 0.65, "agresividad": 0.28})
 
    c16 = cancion(16, datetime(1979, 11, 30), "Comfortably Numb",
        {"ritmo": 0.35, "tono": 0.55, "escala_melodica": 0.40,
         "distorsion": 0.40, "densidad_armonica": 0.80},
        {"felicidad": 0.20, "bailabilidad": 0.18, "energia": 0.50,
         "nostalgia": 0.92, "agresividad": 0.12})
 
    #QUEEN 
    c17 = cancion(17, datetime(1975, 10, 31), "Bohemian Rhapsody",
        {"ritmo": 0.60, "tono": 0.65, "escala_melodica": 0.50,
         "distorsion": 0.38, "densidad_armonica": 0.95},
        {"felicidad": 0.42, "bailabilidad": 0.50, "energia": 0.85,
         "nostalgia": 0.75, "agresividad": 0.35})
 
    c18 = cancion(18, datetime(1980, 6, 30), "Another One Bites the Dust",
        {"ritmo": 0.84, "tono": 0.50, "escala_melodica": 0.45,
         "distorsion": 0.30, "densidad_armonica": 0.60},
        {"felicidad": 0.55, "bailabilidad": 0.88, "energia": 0.88,
         "nostalgia": 0.50, "agresividad": 0.50})
 
    #EMINEM 
    c19 = cancion(19, datetime(2002, 5, 26), "Lose Yourself",
        {"ritmo": 0.88, "tono": 0.55, "escala_melodica": 0.30,
         "distorsion": 0.20, "densidad_armonica": 0.55},
        {"felicidad": 0.40, "bailabilidad": 0.75, "energia": 0.98,
         "nostalgia": 0.45, "agresividad": 0.82})
 
    c20 = cancion(20, datetime(2000, 5, 23), "The Real Slim Shady",
        {"ritmo": 0.85, "tono": 0.58, "escala_melodica": 0.50,
         "distorsion": 0.15, "densidad_armonica": 0.50},
        {"felicidad": 0.60, "bailabilidad": 0.82, "energia": 0.88,
         "nostalgia": 0.30, "agresividad": 0.65})
 
    todas_las_canciones = [
        c01, c02, c03, c04, c05, c06, c07, c08, c09, c10,
        c11, c12, c13, c14, c15, c16, c17, c18, c19, c20
    ]
 
    
    #ARTISTAS
    
    a01 = artista("Nirvana",         datetime(1987, 1,  1),  [c01, c02])
    a02 = artista("Black Sabbath",   datetime(1968, 1,  1),  [c03, c04])
    a03 = artista("AC/DC",           datetime(1973, 1,  1),  [c05, c06])
    a04 = artista("Guns N' Roses",   datetime(1985, 1,  1),  [c07, c08])
    a05 = artista("Led Zeppelin",    datetime(1968, 9,  1),  [c09, c10])
    a06 = artista("Michael Jackson", datetime(1964, 1,  1),  [c11, c12])
    a07 = artista("The Beatles",     datetime(1960, 1,  1),  [c13, c14])
    a08 = artista("Pink Floyd",      datetime(1965, 1,  1),  [c15, c16])
    a09 = artista("Queen",           datetime(1970, 6, 27),  [c17, c18])
    a10 = artista("Eminem",          datetime(1972, 10, 17), [c19, c20])
 
    todos_los_artistas = [a01, a02, a03, a04, a05, a06, a07, a08, a09, a10]
 
    
    #PLAYLISTS
  
    pl1 = playlist(1, "Hard Rock & Metal",
                   datetime(2020, 1, 1),  [c01, c03, c04, c05, c06, c07, c10])
    pl2 = playlist(2, "Epic Ballads",
                   datetime(2019, 6, 1),  [c08, c09, c16, c17])
    pl3 = playlist(3, "Pop & Groove Legends",
                   datetime(2021, 3, 15), [c11, c12, c13, c14, c18])
    pl4 = playlist(4, "Rap Attack",
                   datetime(2022, 8, 10), [c19, c20])
    pl5 = playlist(5, "Psychedelic Vibes",
                   datetime(2018, 11, 1), [c14, c15, c16, c09])
 
    todas_las_playlists = [pl1, pl2, pl3, pl4, pl5]
 
   
    #CATALOGO
    cat = catalogo(
        canciones=todas_las_canciones,
        artistas=todos_los_artistas,
        playlist=todas_las_playlists
    )
 
     # cadena de responsabilidad 
    manejador_sentimientos = ManejadorSentimientos(sucesor=None)
    manejador_sonoro       = ManejadorSonor(sucesor=manejador_sentimientos)
 
    # imprime el perfil de la sesion
    
    def mostrar_perfil(sesion):
        s = sesion.get_sonor_stat()
        e = sesion.get_sentimental_stat()

        campos_s = ["ritmo", "tono", "escala_melodica", "distorsion", "densidad_armonica"]
        campos_e = ["felicidad", "bailabilidad", "energia", "nostalgia", "agresividad"]

        print("\nATRIBUTO SONORO - media - desviacion")
        print("-------------------------------------")

        for k in campos_s:
            print(k, "-", round(s["media"][k], 2), "-", round(s["desviacion"][k], 2))

        print("\nATRIBUTO SENTIMENTAL - media - desviacion")
        print("-----------------------------------------")

        for k in campos_e:
            print(k, "-", round(e["media"][k], 2), "-", round(e["desviacion"][k], 2))
   
    #imprime las 3 recomendaciones de una vez
    
    def mostrar_recomendaciones(sistema, sesion):
        rc = sistema.get_recomendacion("canciones", sesion)
        ra = sistema.get_recomendacion("artistas",  sesion)
        rp = sistema.get_recomendacion("playlist",  sesion)
        co = rc.get("cancion");  print(f"  Canción  → {co.titulo  if co else 'ninguna (sin match)'}")
        ao = ra.get("artista");  print(f"  Artista  → {ao.nombre  if ao else 'ninguno (sin match)'}")
        po = rp.get("playlist"); print(f"  Playlist → {po.titulo  if po else 'ninguna (sin match)'}")
 
    #perfil 1: Adam

    print("\n" + "═" * 62)
    print(" P1 — perfil METAL / HARD-ROCK")
    print("═" * 62)
 
    sesion_adam = SesionEscucha(ventana_max=4, manejador=manejador_sonoro)
    adam = Usuario(id=1, nombre="Adam",
                   sesion=sesion_adam, fecha_registro=datetime(2024, 1, 1))
 
    for c in [c01, c03, c05, c07]:          # Nirvana · Sabbath · AC/DC · GNR
        adam.escuchar_cancion(c, datetime.now())
        print(f"  ♪  {c.titulo}")
 
    mostrar_perfil(sesion_adam)
 
    sistema = Sistema_recomendador()
    sistema.configurar_recomendacion(cat, orden_alfabetico())
 
    print("\n  ── Alfabética ──────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_adam)
 
    sistema.establecer_estrategia(orden_temporal())
    print("\n  ── Temporal ────────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_adam)
 
    sistema.establecer_estrategia(forma_aleatoria())
    print("\n  ── Aleatoria ───────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_adam)
 
    
    # perfil 2: Ana
    print("\n" + "═" * 62)
    print("— perfil PSICODÉLICO / NOSTÁLGICO")
    print("═" * 62)
 
    sesion_ana = SesionEscucha(ventana_max=4, manejador=manejador_sonoro)
    ana = Usuario(id=2, nombre="Ana",
                  sesion=sesion_ana, fecha_registro=datetime(2024, 2, 1))
 
    for c in [c14, c16, c08, c09]:          # Beatles · Floyd · GNR ballad · Zeppelin
        ana.escuchar_cancion(c, datetime.now())
        print(f"{c.titulo}")
 
    mostrar_perfil(sesion_ana)
 
    sistema.establecer_estrategia(orden_alfabetico())
    print("\n  ── Alfabética ──────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_ana)
 
    sistema.establecer_estrategia(orden_temporal())
    print("\n  ── Temporal ────────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_ana)
 
    #perfil3: Luis
    
    print("\n" + "═" * 62)
    print(" P3— perfil POP / FUNK / BAILABLE")
    print("═" * 62)
 
    sesion_luis = SesionEscucha(ventana_max=4, manejador=manejador_sonoro)
    luis = Usuario(id=3, nombre="Luis",
                   sesion=sesion_luis, fecha_registro=datetime(2024, 3, 1))
 
    for c in [c11, c12, c18, c20]:          # MJ Billie Jean · MJ Beat It · Queen · Eminem
        luis.escuchar_cancion(c, datetime.now())
        print(f"{c.titulo}")
 
    mostrar_perfil(sesion_luis)
 
    sistema.establecer_estrategia(orden_alfabetico())
    print("\n  ── Alfabética ──────────────────────────────────────")
    mostrar_recomendaciones(sistema, sesion_luis)
 
    sistema.establecer_estrategia(forma_aleatoria())
    print("\n  ── Aleatoria (vía usuario) ─────────────────────────")
    ru_c = luis.pedir_recomendacion(RecomendarCancion (cat, sesion_luis, forma_aleatoria()))
    ru_a = luis.pedir_recomendacion(RecomendadorArtista(cat, sesion_luis, forma_aleatoria()))
    ru_p = luis.pedir_recomendacion(RecomendadorPlaylist(cat, sesion_luis, forma_aleatoria()))
    co = ru_c.get("cancion");  print(f" Canción  → {co.titulo  if co else 'ninguna (sin match)'}")
    ao = ru_a.get("artista");  print(f" Artista  → {ao.nombre  if ao else 'ninguno (sin match)'}")
    po = ru_p.get("playlist"); print(f" Playlist → {po.titulo  if po else 'ninguna (sin match)'}")
 
    # singleton – verificación final
    sistema_b = Sistema_recomendador()
    print(f"\n  Singleton funciona : {sistema is sistema_b}")
    
    


    
    # KAFKA - PRODUCTOR + CONSUMIDOR
    #
    # Requisitos:
    #   pip install kafka-python
    #   Kafka corriendo en localhost:9092
    #   docker run -d -p 9092:9092 apache/kafka:3.7.0
    #
    # El producer.py publica eventos {usuario_id, cancion_id} cada 2 s.
    # El consumer.py los recibe, busca la cancion en el catalogo,
    # actualiza la sesion de escucha y pide una recomendacion.
    
    try:
        import threading
        import time
        import random as _random
        from producer import Producer
        from consumer import Consumer
 
        TOPIC    = "escuchas"
        FREQ_SEG = 2      # segundos entre publicaciones del productor
        N_MSG    = 10     # cuantos mensajes publica antes de parar
 
        sistema.establecer_estrategia(forma_aleatoria())
 
        # cadena de responsabilidad propia para el flujo Kafka
        mj_k = ManejadorSentimientos(sucesor=None)
        ms_k = ManejadorSonor(sucesor=mj_k)
 
        consumer = Consumer(
            topic            = TOPIC,
            catalogo         = cat,
            sistema          = sistema,
            manejador_sonoro = ms_k
        )
 
        # el productor se lanza en un hilo separado para que
        # el consumer pueda leer en el hilo principal al mismo tiempo
        def lanzar_productor():
            prod = Producer(TOPIC, FREQ_SEG)
            for _ in range(N_MSG):
                evento = {"usuario_id": 1, "cancion_id": _random.choice(prod.ids_canciones)}
                prod.producer.send(TOPIC, value=evento)
                print(f"[PRODUCER] Enviado: {evento}")
                time.sleep(FREQ_SEG)
            prod.producer.flush()
            prod.producer.close()
            print("[PRODUCER] Publicacion completada.")
 
        print("\n" + "=" * 62)
        print("  KAFKA - PRODUCTOR / CONSUMIDOR EN TIEMPO REAL")
        print("=" * 62)
 
        t_prod = threading.Thread(target=lanzar_productor, daemon=True)
        t_prod.start()
 
        # el consumer bloquea el hilo principal hasta procesar N_MSG mensajes
        consumer.iniciar_consumicion()
 
        t_prod.join(timeout=N_MSG * FREQ_SEG + 10)
 
        print("\n" + "=" * 62)
        print("  Bloque Kafka completado.")
        print("=" * 62 + "\n")
 
    except ImportError as e:
        print(f"\n[KAFKA] Modulo no encontrado: {e}")
        print("  Asegurate de tener producer.py y consumer.py en la misma carpeta")
        print("  y kafka-python instalado:  pip install kafka-python\n")