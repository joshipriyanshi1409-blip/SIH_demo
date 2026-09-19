class LexerError(Exception):
    """Raised when JOCKY source cannot be tokenized."""

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column

        super().__init__(
            f"Lexer error at line {line}, column {column}: {message}"
        )
        