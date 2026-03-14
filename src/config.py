from dataclasses import dataclass
from pathlib import Path

from enums import SupportKind


@dataclass(frozen=True)
class SupportDirectory:
    kind: SupportKind
    path: Path
