import sys
import traceback

from pycodeowners._pycodeowners.models.parsing_context import ParsingContext


class CodeownerSyntaxError(ValueError):
    def __init__(
        self, message: str, pc: ParsingContext | None, col: int | None
    ) -> None:
        self.message = message
        super().__init__(message)

        if pc:
            self.loc = f"{pc.path}:{pc.line}"
            if col:
                self.loc += f":{col}"

            self.add_note(self.loc)

    def print(self, verbose: bool = False) -> None:
        print(f"{self.loc} {self.message}", file=sys.stderr)
        if verbose:
            print(traceback.format_exc(), file=sys.stderr)


class InvalidOwnerError(ValueError):
    pass
