import pytest
from datetime import datetime
from stream_musica_ultimaversion import (
    cancion, playlist, artista, catalogo,
    SesionEscucha, ManejadorSonor, ManejadorSentimientos,
    orden_alfabetico, Sistema_recomendador, Usuario
)


@pytest.fixture
def cancion_1():
    return cancion(1, datetime(1991, 9, 10), "Smells Like Teen Spirit",
                  {"ritmo": 0.8, "tono": 0.5}, {"felicidad": 0.3})

@pytest.fixture
def sesion_vacia():
    # Creamos la cadena de responsabilidad con los manejadores
    m_sent = ManejadorSentimientos(None)
    m_sono = ManejadorSonor(m_sent)
    return SesionEscucha(ventana_max=2, manejador=m_sono)

@pytest.fixture
def sistema(cancion_1): # instanciamos el sistema con una csncion para tener el catalogo listo 
    s = Sistema_recomendador()
    cat = catalogo([cancion_1], [], [])
    s.configurar_recomendacion(cat, orden_alfabetico())
    return s
#######----------------------------------------------test------------------------------------------------
def test_creacion_cancion(cancion_1):
    assert cancion_1.titulo == "Smells Like Teen Spirit"
    assert cancion_1.id == 1

def test_playlist_media():
    # creamos varias canciones
    c1 = cancion(1, datetime.now(), "S1", {"ritmo": 0.2}, {"f": 0.5})
    c2 = cancion(2, datetime.now(), "S2", {"ritmo": 0.8}, {"f": 0.5})

    pl = playlist(1, "Test", datetime.now(), [c1, c2])
    # La media de 0.2 y 0.8 = 0.2+0.8 /2 =0.5
    assert pl.calcular_media_sonora()["ritmo"] == 0.5


####cadena de responsabilidad 
def test_sesion_calcula_stats(sesion_vacia, cancion_1):
    sesion_vacia.agregar_cancion(cancion_1)
    # Verificamos que la cadena de manejadores ha llenado el diccionario stats
    assert "sonoros" in sesion_vacia.stats
    assert "sentimientos" in sesion_vacia.stats


# probamos que estrategia funcione bien 
def test_estrategia_alfabetica(cancion_1, sesion_vacia):
    est = orden_alfabetico()
    cat = catalogo([cancion_1], [], [])
    # Buscamos una canción en el catálogo que coincida con la sesión (vacia=True)
    resultado = est.buscar(cat, sesion_vacia, modo="canciones")
    assert resultado.titulo == "Smells Like Teen Spirit"



# comprobamos que el recomendador es un singleton y por lo tanto sea unico 
def test_singleton_instancia():
    s1 = Sistema_recomendador()
    s2 = Sistema_recomendador()
    assert s1 is s2

def test_error_catalogo_no_configurado():
    # creamos un fallo para ver si el sistema es capaz de detectarlo 
    s = Sistema_recomendador()
    s.catalogo_actual = None # Forzamos el error 
    with pytest.raises(RuntimeError): # Manejo de excepciones 
        s.get_recomendacion("canciones", None)



def test_usuario_escucha(cancion_1, sesion_vacia): # aqui comprobamos que el usuario alyazid y marta añade canciones a su sesion
    user = Usuario(1, "Alyazid y Marta", sesion_vacia, datetime.now())
    user.escuchar_cancion(cancion_1, datetime.now())
    assert len(user.sesion.canciones) == 1 # debe ser un 1 porque solo ha escuchado una cancion 