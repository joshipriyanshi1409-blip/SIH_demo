from .errors import LexerError
from .token import Token, TokenType


KEYWORDS = {
    "INVESTIGATE": TokenType.INVESTIGATE,
    "CHECK": TokenType.CHECK,
    "PROCESSES": TokenType.PROCESSES,
    "NETWORK": TokenType.NETWORK,
    "DNS": TokenType.DNS,
    "LOGS": TokenType.LOGS,
}


class Lexer:
    """Convert JOCKY source code into a sequence of tokens."""

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while not self._at_end():
            current = self._peek()

            if current in " \t\r":
                self._advance()
                continue

            if current == "\n":
                self._advance_line()
                continue

            if current == "#":
                self._skip_comment()
                continue

            if current == "{":
                tokens.append(
                    self._make_single_character_token(
                        TokenType.LBRACE
                    )
                )
                self._advance()
                continue

            if current == "}":
                tokens.append(
                    self._make_single_character_token(
                        TokenType.RBRACE
                    )
                )
                self._advance()
                continue

            if self._is_identifier_start(current):
                tokens.append(self._read_identifier())
                continue

            raise LexerError(
                f"unexpected character {current!r}",
                self.line,
                self.column,
            )

        tokens.append(
            Token(
                type=TokenType.EOF,
                value="",
                line=self.line,
                column=self.column,
            )
        )

        return tokens

    def _peek(self) -> str:
        return self.source[self.position]

    def _advance(self) -> str:
        character = self.source[self.position]
        self.position += 1
        self.column += 1
        return character

    def _advance_line(self) -> None:
        self.position += 1
        self.line += 1
        self.column = 1

    def _at_end(self) -> bool:
        return self.position >= len(self.source)

    def _skip_comment(self) -> None:
        while not self._at_end() and self._peek() != "\n":
            self._advance()

    def _is_identifier_start(self, character: str) -> bool:
        return character.isalpha() or character == "_"

    def _is_identifier_part(self, character: str) -> bool:
        return character.isalnum() or character == "_"

    def _read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column

        characters: list[str] = []

        while (
            not self._at_end()
            and self._is_identifier_part(self._peek())
        ):
            characters.append(self._advance())

        value = "".join(characters)
        normalized = value.upper()

        token_type = KEYWORDS.get(
            normalized,
            TokenType.IDENTIFIER,
        )

        return Token(
            type=token_type,
            value=value,
            line=start_line,
            column=start_column,
        )

    def _make_single_character_token(
        self,
        token_type: TokenType,
    ) -> Token:
        return Token(
            type=token_type,
            value=self._peek(),
            line=self.line,
            column=self.column,
        )