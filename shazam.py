import os
import asyncio
import ffmpeg
import tkinter as tk
import argparse
import shutil
from tkinter import filedialog, messagebox
from shazamio import Shazam

parser = argparse.ArgumentParser(description="Identifica músicas em vídeos usando Shazam")
parser.add_argument("--verbose", action="store_true", help="Exibir detalhes adicionais")
# When imported as a module, ignore command line arguments
args = parser.parse_args([])

def selecionar_pasta(titulo):
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title=titulo)
    root.destroy()
    return pasta

def selecionar_arquivo(titulo):
    root = tk.Tk()
    root.withdraw()
    arquivo = filedialog.asksaveasfilename(title=titulo, defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt")])
    root.destroy()
    return arquivo

async def reconhecer_musica(audio_path):
    shazam = Shazam()
    try:
        resultado = await shazam.recognize(audio_path)
        if "track" in resultado:
            return f"{resultado['track']['title']} - {resultado['track']['subtitle']}"
    except Exception as e:
        if args.verbose:
            print(f"❌ Erro ao reconhecer {audio_path}: {e}")
    return None

def extrair_audio(video_path, audio_path):
    try:
        ffmpeg.input(video_path).output(audio_path, format="mp3", acodec="mp3", ar="44100").run(overwrite_output=True, quiet=True)
    except ffmpeg.Error as e:
        if args.verbose:
            print(f"❌ Erro ao converter {video_path}: {e}")

def limpar_pasta(pasta):
    if os.path.exists(pasta):
        shutil.rmtree(pasta)
        if args.verbose:
            print(f"🗑️ Pasta temporária removida: {pasta}")

async def processar_videos(pasta_videos, pasta_resultados):
    if not pasta_videos or not pasta_resultados:
        messagebox.showerror("Erro", "Selecione os diretórios corretamente!")
        return

    pasta_audios = os.path.join(pasta_videos, "audios_temp")
    os.makedirs(pasta_audios, exist_ok=True)

    musicas_encontradas = {}
    
    print("\n🎬 Iniciando processamento...\n")

    for arquivo in os.listdir(pasta_videos):
        if arquivo.lower().endswith((".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv")):
            caminho_video = os.path.join(pasta_videos, arquivo)
            caminho_audio = os.path.join(pasta_audios, f"{os.path.splitext(arquivo)[0]}.mp3")

            print(f"🔄 Processando: {arquivo}")
            extrair_audio(caminho_video, caminho_audio)

            musica = await reconhecer_musica(caminho_audio)

            if musica:
                if musica not in musicas_encontradas:
                    print(f"🎵 Música encontrada: {musica}")
                    musicas_encontradas[musica] = arquivo
                else:
                    print(f"⚠️ Música duplicada ignorada: {musica}")
            else:
                print("❌ Nenhuma música identificada")
        elif arquivo.lower().endswith((".mp3", ".wav", ".flac")):
            caminho_audio = os.path.join(pasta_videos, arquivo)
            print(f"🔄 Processando áudio: {arquivo}")
            musica = await reconhecer_musica(caminho_audio)

            if musica:
                if musica not in musicas_encontradas:
                    print(f"🎵 Música encontrada: {musica}")
                    musicas_encontradas[musica] = arquivo
                else:
                    print(f"⚠️ Música duplicada ignorada: {musica}")
            else:
                print("❌ Nenhuma música identificada")

    if musicas_encontradas:
        with open(pasta_resultados, "w", encoding="utf-8") as f:
            for musica, arquivo in musicas_encontradas.items():
                f.write(f"{arquivo}: {musica}\n")
        print(f"\n✅ Processamento finalizado! Resultados salvos em: {pasta_resultados}")
    else:
        print("\n⚠️ Nenhuma música foi encontrada nos vídeos.")

    limpar_pasta(pasta_audios)

if __name__ == "__main__":
    # Parse real command line arguments when running directly
    args = parser.parse_args()

    pasta_videos = selecionar_pasta("Selecione a pasta com os vídeos")
    pasta_resultados = selecionar_arquivo("Escolha onde salvar o arquivo de resultados")
    
    asyncio.run(processar_videos(pasta_videos, pasta_resultados))
