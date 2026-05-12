from os.path import basename
from pathlib import Path

from pymediainfo import MediaInfo

from .models import MovieMetadata


def format_bitrate(bitrate_in: list[str]) -> str:
    """format bitrate removing first whitespace when bitrate is as 'kb/s'"""

    bitrate: str = "".join(bitrate_in)
    if "kb" in bitrate and bitrate.count(" ") >= 2:
        newb: str = bitrate.replace(" ", "", 1)
        return newb
    return bitrate


def obtain_display_res(width: str, heigth: str, pixel_aspect_ratio: str) -> str:
    """Transform width and heith into string with display res, if
    pixel_aspect_ratio is provided, otherwise just return if it doens't exist or
    is 1."""

    # https://rendezvois.github.io/video/anamorphic/?h=sar
    # if not pixel_aspect_ratio:j
    # return f"{width} x {heigth}"
    tmp: list[str] = []
    for char in pixel_aspect_ratio:
        if char != "0":
            tmp.append(char)
    if len(tmp) == 1:
        return f"{width} x {heigth}"
    w: int = int(width)
    h: int = int(heigth)
    par: float = float(pixel_aspect_ratio)
    if par > 1:
        return f"{width} x {heigth} ~> {round(w * par)} x {h}"
    elif par < 1:
        return f"{width} x {heigth} ~> {w} x {round(h / par)}"
    else:
        return f"{width} x {heigth}"


def replace_codecs(name: str, mi: MediaInfo) -> str:
    """Perform codec name substitution in defined cases."""
    audio = mi.audio_tracks[0] if mi.audio_tracks else None
    if name == "AVC":
        return "h264"
    if audio:
        if audio.format == "MPEG Audio":
            match audio.format_profile:
                case "Layer 3":
                    return "MP3"
                case "Layer 2":
                    return "MP2"
                case "Layer 1":
                    return "MP1"
                case _:
                    return "not found"
    return name


def inspect_media(path: Path) -> MediaInfo:
    """Take path to file, return MediaInfo object."""
    info: MediaInfo = MediaInfo.parse(path)
    return info


def format_size(bytes: int) -> str:
    """Format bytes in GiB/MiB/Bytes."""
    match bytes:
        case n if n >= 1024**3:
            return f"{n / 1024**3:.1f} GiB"
        case n if n >= 1024**2:
            return f"{n / 1024**2:.1f} MiB"
        case _:
            return f"{bytes} B"


def format_frame_rate(frame_rate: str) -> str:
    """If framerate has only zeroes after the dot, return
    everything before the dot."""
    if not frame_rate:
        return ""
    if "." not in frame_rate:
        return frame_rate
    idx: int = frame_rate.index(".")
    if frame_rate[idx:].strip(".0") == "":
        return frame_rate[:idx]
    else:
        return frame_rate


def extract_metadata(path: Path) -> MovieMetadata | None:
    """Extract data from a video file.

    In case a video track is not present, return None immediatly.
    If it does contain a video track, continue processing and
    return a MovieMetadata object.
    """

    data: MediaInfo = inspect_media(path)
    video_track = data.video_tracks[0] if data.video_tracks else None
    general_track = data.general_tracks[0]

    if not video_track:
        return None

    audio_codec: str = "-"
    audio_bitrate: str = "-"
    video_codec: str = replace_codecs(general_track.codecs_video, data)
    video_bitrate: str = format_bitrate(video_track.other_bit_rate)
    video_width: str = video_track.sampled_width
    video_height: str = video_track.sampled_height
    video_par: str = video_track.pixel_aspect_ratio
    display_res: str = obtain_display_res(video_width, video_height, video_par)
    aspect_ratio: str = "".join(video_track.other_display_aspect_ratio)
    frame_rate: str = format_frame_rate(video_track.frame_rate)
    size: str = format_size(general_track.file_size)
    release: str = basename(general_track.file_name)
    ext: str = general_track.file_extension

    audio_track = data.audio_tracks[0] if data.audio_tracks else None
    if audio_track:
        audio_codec = general_track.audio_codecs
        if len(audio_codec) > 1:
            audio_codec = audio_codec.split("/")[0]
            audio_codec = replace_codecs(audio_codec, data)
        audio_bitrate = format_bitrate(audio_track.other_bit_rate)

    metadata = MovieMetadata(
        video_codec=video_codec,
        video_bitrate=video_bitrate,
        audio_codec=audio_codec,
        audio_bitrate=audio_bitrate,
        resolution=display_res,
        aspect_ratio=aspect_ratio,
        release=release,
        container=ext,
        frame_rate=frame_rate,
        size=size,
    )
    return metadata
