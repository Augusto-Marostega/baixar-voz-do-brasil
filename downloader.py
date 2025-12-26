import logging
import os
import requests
from tqdm import tqdm  # Biblioteca para mostrar uma barra de progresso
import time


def criar_pasta(diretorio):
    """Cria a pasta de destino se ela não existir."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        logging.info(f"Pasta '{diretorio}' criada com sucesso.")
    else:
        logging.info(f"Pasta '{diretorio}' já existe.")


def verificar_integridade_arquivo(caminho_arquivo, tamanho_esperado):
    """Verifica se o arquivo foi baixado corretamente, comparando seu tamanho com o tamanho esperado."""
    tamanho_atual = os.path.getsize(caminho_arquivo)
    if tamanho_atual != tamanho_esperado:
        return False
    else:
        return True


def baixar_audio(audio_list, diretorio_destino="baixados"):
    """Baixa os áudios a partir da lista de objetos Audio e salva no diretório especificado."""

    # Certifique-se de que o diretório de destino existe
    criar_pasta(diretorio_destino)

    # Verifica se a lista de áudios não está vazia
    if not audio_list:
        logging.warning(f"Nenhum áudio na lista para baixar.")
        return

    # Barra de progresso para o total de arquivos
    with tqdm(total=len(audio_list), desc="Baixando áudios", unit="áudio", dynamic_ncols=True) as pbar_total:
        # Itera sobre cada objeto Audio na lista com a barra de progresso
        for i, audio in enumerate(audio_list):
            try:
                # Definir o nome do arquivo com base no título e na data (ou outro identificador único)
                nome_arquivo_temp = f"{audio.titulo.replace('/', '-')}-a-voz-do-brasil.temp"
                nome_arquivo_final = f"{audio.titulo.replace('/', '-')}-a-voz-do-brasil.mp3"
                caminho_arquivo_temp = os.path.join(diretorio_destino, nome_arquivo_temp)
                caminho_arquivo_final = os.path.join(diretorio_destino, nome_arquivo_final)
                # Fazendo o download do áudio
                response = requests.get(audio.url_down_mp3, stream=True)

                # Verifica se o request foi bem-sucedido
                if response.status_code == 200:
                    total_tamanho = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
                    #bytes_baixados = 0  # Bytes baixados até agora

                    # Abre o arquivo para escrever os dados
                    with open(caminho_arquivo_temp, 'wb') as f:  # Abre arquivo como escrita em formato binário
                        # Barra de progresso para o download do arquivo
                        with tqdm(total=total_tamanho, unit='B', unit_scale=True, desc=nome_arquivo_temp,
                                  dynamic_ncols=True) as pbar_arquivo:
                            for chunk in response.iter_content(chunk_size=1024*1024):  # Baixa o arquivo em pedaços
                                if chunk:
                                    f.write(chunk)  # Grava no arquivo
                                    #bytes_baixados += len(chunk)
                                    pbar_arquivo.update(len(chunk))  # Atualiza a barra de progresso do arquivo
                                    pbar_arquivo.set_postfix()
                    if verificar_integridade_arquivo(caminho_arquivo_temp, total_tamanho):
                        os.rename(caminho_arquivo_temp, caminho_arquivo_final)
                        logging.info(f"Arquivo '{nome_arquivo_final}'foi baixado com sucesso.")
                    else:
                        logging.error(f"!!! O arquivo '{caminho_arquivo_temp}' está corrompido. !!!")
                        os.remove(caminho_arquivo_temp)
                        logging.error(f"!!! O Arquivo '{caminho_arquivo_temp}' corrompido foi removido. !!!")

                else:
                    logging.error(f"Erro ao baixar '{nome_arquivo_final}': Status {response.status_code}")

            except Exception as e:
                logging.error(f"Erro ao baixar o áudio '{nome_arquivo_final}': {e}")
                os.remove(caminho_arquivo_temp)
                logging.error(f"!!! O Arquivo '{caminho_arquivo_temp}' corrompido foi removido. !!!")

            # Atualiza a barra de progresso global para o total de arquivos baixados
            pbar_total.update(1)
