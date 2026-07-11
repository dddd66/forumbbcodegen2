from pymediainfo import MediaInfo as pm_info
from pathlib import Path
import os

class MediaInfo:

    @staticmethod
    def from_path(path: Path | str) -> dict:
        """
        Parses the mediainfo out of a file path.

        Args:
            path (Path | str):
                The file path.
        
        Returns:
            dict:
                A dictionary containing the result.
        
        Raises:
            FileNotFoundError
                If path does not exist.
            ValueError
                If the file contains no video track.
        """

        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        mi = pm_info.parse(path)

        general = mi.general_tracks[0]
        video = mi.video_tracks[0] if mi.video_tracks else None
        audios = mi.audio_tracks

        if video is None:
            raise ValueError(f"No video track found in: {path}")

        audio = audios[0] if audios else None

        return {
            "release":      path.stem,
            "container":    general.format,
            "file_size":    general.file_size or os.path.getsize(path),
            "duration_ms":  general.duration or (video.duration if video else None),

            "video_format":       general.codecs_video or video.format,
            "video_bit_rate":     video.other_bit_rate,
            "video_width":        video.sampled_width  or video.width,
            "video_height":       video.sampled_height or video.height,
            "video_par":          video.pixel_aspect_ratio,
            "video_dar":          video.other_display_aspect_ratio,
            "video_frame_rate":   video.frame_rate,

            "audio_format":       general.audio_codecs or (audio.format if audio else None),
            "audio_format_raw":   audio.format         if audio else None,
            "audio_profile":      audio.format_profile if audio else None,
            "audio_bit_rate":     audio.other_bit_rate if audio else None,
            "audio_languages":    [t.language for t in audios] if audios else [],
        }