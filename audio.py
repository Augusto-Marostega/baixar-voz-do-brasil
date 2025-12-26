class Audio:
    def __init__(self, titulo, hora, url_down_mp3):
        self.titulo = titulo  # Título da notícia
        self.hora = hora  # Hora do programa
        self.url_down_mp3 = url_down_mp3  # URL do arquivo MP3 para download

    def __repr__(self):
        return f"Audio(titulo='{self.titulo}', hora='{self.hora}', url_down_mp3='{self.url_down_mp3}')"
