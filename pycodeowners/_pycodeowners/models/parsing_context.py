from dataclasses import dataclass


@dataclass
class ParsingContext:
    path: str
    line: int

    line_content: str
