import re

from .models import MovieFormData, MovieMetadata


def generate_bb_code(data: MovieFormData, metadata: MovieMetadata) -> str:
    match = re.search("^.*tt[0-9]{7}", data.imdb_url)
    if match:
        imdb = match.group()
    bbcode = (
        f"[tablePrinc]"
        f"[tr][titMasc]Título do Filme[/titMasc][/tr]"
        f"[tr]"
        f"[titTrad]{data.title_br}[/titTrad]"
        f"[titOri]{data.title}[/titOri]"
        f"[release]{metadata.release}[/release]"
        f"[/tr]"
        f"[tr]"
        f"[posterMasc]Poster[/posterMasc]"
        f"[sinopseMasc]Sinopse[/sinopseMasc]"
        f"[/tr]"
        f"[tr]"
        f"[poster][posterIma]{data.poster}[/posterIma][/poster]"
        f"[sinopse]{data.synopsis}[/sinopse]"
        f"[tableScreen]Screenshots[/tableScreen]"
    )
    side: str = ""
    for n in range(len(data.screenshots.split(","))):
        if n % 2 == 0:
            if n != 0:
                bbcode += "[/tr]"
            bbcode += "[tr]"
        if n % 2 == 0:
            side = "screenLeft"
        else:
            side = "screenRight"
        bbcode += f"[{side}][screenIma]{data.screenshots.split(',')[n]}[/screenIma][/{side}]"
    bbcode += "[/tr]"
    bbcode += (
        f"[closeTab][/closeTab]"
        f"[/tr]"
        f"[/tablePrinc]"
        f"[tablePrinc]"
        f"[tr]"
        f"[posterMasc]Elenco[/posterMasc]"
        f"[infoMasc]Informações sobre o filme[/infoMasc]"
        f"[infoMasc]Informações sobre o release[/infoMasc]"
        f"[/tr]"
        f"[tr]"
        f"[elenco]{data.cast}[/elenco]"
        f"[info]"
        f"[b]Gênero: [/b]{data.genre}\n"
        f"[b]Diretor: [/b]{data.director}\n"
        f"[b]Duração: [/b]{data.duration} minutos\n"
        f"[b]Ano de Lançamento: [/b]{data.year}\n"
        f"[b]País de Origem: [/b]{data.country}\n"
        f"[b]Idioma do Áudio: [/b]{data.audio_language}\n"
        f"[b]IMDB: [/b][url={imdb}]{imdb}[/url]\n"
        f"[/info]"
        f"[info]"
        f"[b]Qualidade de Vídeo: [/b]{data.quality}\n"
        f"[b]Container: [/b]{metadata.container}\n"
        f"[b]Vídeo Codec: [/b]{metadata.video_codec}\n"
        f"[b]Vídeo Bitrate: [/b]{metadata.video_bitrate}\n"
        f"[b]Áudio Codec: [/b]{metadata.audio_codec}\n"
        f"[b]Áudio Bitrate: [/b]{metadata.audio_bitrate}\n"
        f"[b]Resolução: [/b]{metadata.resolution}\n"
        f"[b]Formato de Tela: [/b]{metadata.aspect_ratio}\n"
        f"[b]Frame Rate: [/b]{metadata.frame_rate} FPS\n"
        f"[b]Tamanho: [/b]{metadata.size}\n"
        f"[b]Legendas: [/b]{data.subtitles}"
        f"[/info]"
        f"[/tr]"
    )
    if data.awards.strip():
        bbcode += (
            f"[tr][infoExtraMasc]Premiações[/infoExtraMasc][/tr]"
            f"[tr][infoExtra]{data.awards}[/infoExtra][/tr]\n"
        )
    if data.trivia.strip():
        bbcode += (
            f"[tr][infoExtraMasc]Curiosidades[/infoExtraMasc][/tr]"
            f"[tr][infoExtra]{data.trivia}[/infoExtra][/tr]\n"
        )
    if data.review.strip():
        bbcode += (
            f"[tr][infoExtraMasc]Crítica[/infoExtraMasc][/tr]"
            f"[tr][infoExtra]{data.review}[/infoExtra][/tr]\n"
        )
    bbcode += (
        "[tr][rodape]"
        "Coopere, deixe semeando ao menos duas vezes o tamanho do arquivo que baixar."
        "[/rodape][/tr][/tablePrinc]"
    )
    return bbcode
