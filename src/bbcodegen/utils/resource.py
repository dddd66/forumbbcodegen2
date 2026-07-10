from pathlib import Path
import sys
import os

class Resource:
    @staticmethod
    def path(relative: str) -> Path:
        """
        Resolves an relative path.

        Note:
            Only needed to make things easier for pyinstaller,
            maybe change this on future, who knows :p

        Args:
            relative (str):
                The relative file path (from the root).
        
        Returns:
            The complete path.
        """

        base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent.parent.parent.parent))
        return base / relative