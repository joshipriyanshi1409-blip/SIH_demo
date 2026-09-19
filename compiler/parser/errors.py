class ParserError(Exception):
    """Raised when JOCKY tokens do not match the language grammar."""

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column

        super().__init__(
            f"Parser error at line {line}, column {column}: {message}"
        )