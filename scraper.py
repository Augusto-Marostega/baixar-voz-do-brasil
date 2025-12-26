import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from audio import Audio


# Função para buscar os links de áudio e criar os objetos Audio considerando os últimos X dias
def obter_url_audio_scraping(url_base="https://radiogov.ebc.com.br/programas/a-voz-do-brasil-download",dias=1):

    # Realiza a requisição para o site
    response = requests.get(url_base)
    if response.status_code != 200:
        logging.error("Erro ao acessar o site. Verifique a conexão.")
        return []

    # Parseia o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os cards de programas na página (ajuste a classe conforme o site)
    cards = soup.find_all('div', class_='card')  # Verifique a classe correta na página real

    audio_list = []

    # Obter a data atual
    data_atual = datetime.now()

    # Iterar sobre todos os cards
    for card in cards:
        try:
            # Encontrar a data do programa dentro do card
            data_programa_str = card.find('div', class_='titulo-noticia').text.strip()

            # Converter a string da data para o formato datetime
            try:
                data_programa = datetime.strptime(data_programa_str, "%d/%m/%Y")
            except ValueError:
                logging.error(f"Erro ao processar a data: {data_programa_str}")
                continue

            # Verificar se a data do programa é dentro dos últimos 'dias' dias
            if data_atual - timedelta(days=dias) <= data_programa <= data_atual:
                # Encontrar o título da notícia
                titulo = card.find('div', class_='titulo-noticia').text.strip()

                # Encontrar a hora
                hora = card.find('div', class_='hora-noticia').text.strip()

                # Encontrar a URL de download do MP3
                url_down_mp3 = card.find('a', class_='download-btn')['href']

                # Criar a instância do modelo Audio e adicionar à lista
                audio = Audio(titulo, hora, url_down_mp3)
                audio_list.append(audio)

        except Exception as e:
            logging.error(f"Erro ao processar um card: {e}")

    return audio_list
