import logging
import os
from scraper import obter_url_audio_scraping
from downloader import baixar_audio

# Configura pasta de logs
os.makedirs("logs", exist_ok=True)

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/logs.log"),
        logging.StreamHandler()
    ]
)

def main():
    # Configurar os dias para buscar os áudios
    url_site = "https://radiogov.ebc.com.br/programas/a-voz-do-brasil-download"
    dias = 1  # Exemplo: Baixar áudios dos últimos 3 dias
    diretorio_destino = r"baixados"  # Diretório de destino

    # Obter a lista de áudios
    audio_list = obter_url_audio_scraping(url_base=url_site,dias=dias)

    # Baixar os áudios
    if audio_list:
        baixar_audio(audio_list, diretorio_destino)
    else:
        logging.info(f"Nenhum áudio encontrado para o período especificado.")

if __name__ == "__main__":
    logging.info(f"|| INICIANDO   PROGRAMA ||")
    main()
    logging.info(f"|| FINALIZANDO PROGRAMA ||\n\n")