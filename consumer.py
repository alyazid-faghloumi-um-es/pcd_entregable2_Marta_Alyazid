from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, topic, catalogo, sistema, manejador_sonoro):
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='nflx',
            auto_offset_reset='earliest',
            session_timeout_ms=10000,       # 10 segundos en vez de 45 (valor por defecto)
            heartbeat_interval_ms=3000      # envia un heartbeat cada 3 segundos
        )

        # referencias al sistema de recomendacion
        self._catalogo       = catalogo
        self._sistema        = sistema
        self._manejador      = manejador_sonoro

        # cada usuario tiene su propia sesion de escucha dentro del consumer
        # importamos aqui para evitar importacion circular si se usa en otro modulo
        from stream_musica_ultimaversion import SesionEscucha, Usuario        
        from datetime import datetime

        self._sesion = SesionEscucha(ventana_max=5, manejador=manejador_sonoro)
        self._usuario = Usuario(
            id=99,
            nombre="Kafka_User",
            sesion=self._sesion,
            fecha_registro=datetime.now()
        )

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        if isinstance(value, KafkaConsumer):
            self._consumer = value

    def iniciar_consumicion(self):
        self.receive_message()

    def receive_message(self):
        from stream_musica_ultimaversion import cancion
        from datetime import datetime

        print("\n[CONSUMER] Escuchando mensajes en el topic...\n")

        for mensaje in self._consumer:
            datos = mensaje.value

            # el productor solo manda usuario_id y cancion_id
            # buscamos la cancion real en el catalogo
            cancion_id = datos.get("cancion_id")
            usuario_id = datos.get("usuario_id")

            c = self._catalogo.get_cancion_por_id(cancion_id)

            if c is None:
                print(f"[CONSUMER] cancion_id={cancion_id} no encontrada en el catalogo.")
                continue

            print(f"[CONSUMER] Mensaje recibido  →  usuario_id={usuario_id}  cancion_id={cancion_id}  titulo='{c.titulo}'")

            # introducimos la cancion en la sesion de escucha
            # esto dispara automaticamente la cadena de responsabilidad
            # ManejadorSonor → ManejadorSentimientos
            self._usuario.escuchar_cancion(c, datetime.now())

            # mostramos el perfil actualizado de la sesion
            s = self._sesion.get_sonor_stat()
            e = self._sesion.get_sentimental_stat()

            if s and e:
                print("  Perfil sonoro actual:")
                for k, v in s["media"].items():
                    print(f"    {k:<22} media={v:.2f}  desviacion={s['desviacion'][k]:.2f}")

                print("  Perfil sentimental actual:")
                for k, v in e["media"].items():
                    print(f"    {k:<22} media={v:.2f}  desviacion={e['desviacion'][k]:.2f}")

            # pedimos recomendacion al sistema
            rc = self._sistema.get_recomendacion("canciones", self._sesion)
            ra = self._sistema.get_recomendacion("artistas",  self._sesion)
            rp = self._sistema.get_recomendacion("playlist",  self._sesion)

            co = rc.get("cancion");  print(f"  Cancion   → {co.titulo  if co else 'sin match'}")
            ao = ra.get("artista");  print(f"  Artista   → {ao.nombre  if ao else 'sin match'}")
            po = rp.get("playlist"); print(f"  Playlist  → {po.titulo  if po else 'sin match'}")
            print()
