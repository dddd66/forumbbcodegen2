from langcodes import Language, standardize_tag
from mko_bbcode.core.models import MovieFormData
from pathlib import Path
import re

def _fmt_size(n_bytes: int) -> str:
    """
    Resolve the size on a human-readable format.
    """

    if n_bytes >= 1024 ** 3:
        return f"{n_bytes / 1024 ** 3:.1f} GiB"
    if n_bytes >= 1024 ** 2:
        return f"{n_bytes / 1024 ** 2:.1f} MiB"
    return f"{n_bytes} B"

def _fmt_bitrate(parts: list[str] | None) -> str:
    """
    Resolve the bit-rate on a human-readable format.
    """

    if not parts:
        return ""
    m_info = "".join(parts)
    if "kb" in m_info and m_info.count(" ") >= 2:
        return m_info.replace(" ", "", 1)
    return m_info

def _fmt_frame_rate(value: str | None) -> str:
    """
    Resolve the frame-rate on a human-readable format.
    """

    if not value:
        return ""
    if "." not in value:
        return value
    idx = value.index(".")
    return value[:idx] if not value[idx:].strip(".0") else value

def _fmt_resolution(width, height, par: str | None) -> str:
    """
    Resolve the resolution (par).
    """

    w, h = str(width), str(height)
    if not par:
        return f"{w} x {h}"
    if not par.replace("0", "").replace(".", ""):
        return f"{w} x {h}"
    try:
        par_f = float(par)
    except ValueError:
        return f"{w} x {h}"
    wi, hi = int(width), int(height)
    if par_f > 1:
        return f"{w} x {h} ~> {round(wi * par_f)} x {hi}"
    if par_f < 1:
        return f"{w} x {h} ~> {wi} x {round(hi / par_f)}"
    return f"{w} x {h}"


def _fmt_aspect_ratio(width, height) -> str:
    """
    Resolve the aspect ratio.
    """

    try:
        ratio = int(width) / int(height)
        if ratio < 1.4:   return "Tela Cheia (4x3)"
        elif ratio < 1.8: return "Widescreen (16x9)"
        elif ratio < 2.3: return "Widescreen (2.35:1)"
        else:             return "Widescreen (2.39:1)"
    except Exception:
        return "Widescreen (16x9)"


def _fmt_video_codec(audio_format: str) -> str:
    """
    Resolve the video codec.
    """

    _VIDEO_MAP = {
        "AVC":  "H.264 (AVC)",
        "HEVC": "H.265 (HEVC)",
        "AV1":  "AV1",
        "VP9":  "VP9",
        "XVID": "XviD",
        "DIVX": "DivX",
    }
    upper = (audio_format or "").upper()
    for key, label in _VIDEO_MAP.items():
        if key in upper:
            return label

def _fmt_audio_codec(fmt: str | None) -> str:
    """
    Resolve the audio codec.
    """

    if not fmt:
        return "-"
    lower = fmt.lower()
    if "e-ac-3" in lower or "eac3" in lower:  return "E-AC-3 (Dolby Digital Plus)"
    if "ac-3"   in lower or "ac3"  in lower:  return "AC-3 (Dolby Digital)"
    if "aac"    in lower:                      return "AAC"
    if "dts"    in lower:                      return "DTS"
    if "truehd" in lower:                      return "Dolby TrueHD"
    if "flac"   in lower:                      return "FLAC"
    if "mp3"    in lower or "mpeg audio" in lower: return "MP3"
    if "opus"   in lower:                      return "Opus"
    return fmt


def _fmt_container(fmt: str | None) -> str:
    """
    Resolve the container on a human-readable format.
    """

    if not fmt:
        return ""
    lower = fmt.lower()
    if "matroska" in lower: return "Matroska (MKV)"
    if "avi"      in lower: return "Audio Video Interleave (AVI)"
    return fmt


def _fmt_language(code: str | None) -> str | None:
    """
    Resolve a audio language.
    """

    if not code:
        return None
    try:
        tag = standardize_tag(code)
        return Language.get(tag).display_name("pt-BR").title()
    except Exception:
        return code


def _fmt_languages(codes: list[str | None]) -> str | list[str]:
    """
    Resolve a list of audio languages.
    """

    seen, unique = set(), []
    for code in codes:
        lang = _fmt_language(code)
        if lang and lang not in seen:
            seen.add(lang)
            unique.append(lang)
    if not unique:
        return ""
    return unique[0] if len(unique) == 1 else unique

class BBCode:

    @staticmethod
    def new(data: MovieFormData, m_info: dict) -> str:

        # resolved fields
        release      = m_info["release"]
        container    = _fmt_container(m_info["container"])
        size         = _fmt_size(m_info["file_size"])
        duration_min = str(round(float(m_info["duration_ms"]) / 60_000)) if m_info["duration_ms"] else ""
        video_codec  = _fmt_video_codec(m_info["video_format"])
        video_bitrate = _fmt_bitrate(m_info["video_bit_rate"])
        resolution   = _fmt_resolution(m_info["video_width"], m_info["video_height"], m_info["video_par"])
        aspect_ratio = _fmt_aspect_ratio(m_info["video_width"], m_info["video_height"])
        frame_rate   = _fmt_frame_rate(m_info["video_frame_rate"])
        audio_codec  = _fmt_audio_codec((m_info["audio_format"] or "").split("/")[0].strip())
        audio_bitrate = _fmt_bitrate(m_info["audio_bit_rate"])
        languages    = _fmt_languages(m_info["audio_languages"])
        audio_language = ", ".join(languages) if isinstance(languages, list) else languages

        match = re.search(r"^.*tt[0-9]{7}", data.imdb_url)
        imdb  = match.group() if match else data.imdb_url

        bbcode = (
            f"[tablePrinc]\n"
            f"[tr][titMasc]Título do Filme[/titMasc][/tr]\n"
            f"[tr]\n"
            f"[titTrad]{data.title_br}[/titTrad]\n"
            f"[titOri]{data.title}[/titOri]\n"
            f"[release]{release}[/release]\n"
            f"[/tr]\n"
            f"[tr]\n"
            f"[posterMasc]Poster[/posterMasc]\n"
            f"[sinopseMasc]Sinopse[/sinopseMasc]\n"
            f"[/tr]\n"
            f"[tr]\n"
            f"[poster][posterIma]{data.poster}[/posterIma][/poster]\n"
            f"[sinopse]{data.synopsis}[/sinopse]\n"
            f"[tableScreen]Screenshots[/tableScreen]\n"
        )

        screenshots = [s.strip() for s in data.screenshots.split(",") if s.strip()]
        for n, shot in enumerate(screenshots):
            if n % 2 == 0:
                if n != 0:
                    bbcode += "[/tr]"
                bbcode += "[tr]"
            side = "screenLeft" if n % 2 == 0 else "screenRight"
            bbcode += f"[{side}][screenIma]{shot}[/screenIma][/{side}]"
        bbcode += "[/tr]"

        bbcode += (
            f"[closeTab][/closeTab]\n"
            f"[/tr]\n"
            f"[/tablePrinc]\n"
            f"[tablePrinc]\n"
            f"[tr]\n"
            f"[posterMasc]Elenco[/posterMasc]\n"
            f"[infoMasc]Informações sobre o filme[/infoMasc]\n"
            f"[infoMasc]Informações sobre o release[/infoMasc]\n"
            f"[/tr]\n"
            f"[tr]\n"
            f"[elenco]{data.cast}[/elenco]\n"
            f"[info]\n"
            f"[b]Gênero: [/b]{data.genre}\n"
            f"[b]Diretor: [/b]{data.director}\n"
            f"[b]Duração: [/b]{data.duration} minutos\n"
            f"[b]Ano de Lançamento: [/b]{data.year}\n"
            f"[b]País de Origem: [/b]{data.country}\n"
            f"[b]Idioma do Áudio: [/b]{data.audio_language}\n"
            f"[b]IMDB: [/b][url={imdb}]{imdb}[/url]\n"
            f"[/info]\n"
            f"[info]\n"
            f"[b]Qualidade de Vídeo: [/b]{data.quality}\n"
            f"[b]Container: [/b]{container}\n"
            f"[b]Vídeo Codec: [/b]{video_codec}\n"
            f"[b]Vídeo Bitrate: [/b]{video_bitrate}\n"
            f"[b]Áudio Codec: [/b]{audio_codec}\n"
            f"[b]Áudio Bitrate: [/b]{audio_bitrate}\n"
            f"[b]Resolução: [/b]{resolution}\n"
            f"[b]Formato de Tela: [/b]{aspect_ratio}\n"
            f"[b]Frame Rate: [/b]{frame_rate} FPS\n"
            f"[b]Tamanho: [/b]{size}\n"
            f"[b]Legendas: [/b]{data.subtitles}\n"
            f"[/info]\n"
            f"[/tr]\n"
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