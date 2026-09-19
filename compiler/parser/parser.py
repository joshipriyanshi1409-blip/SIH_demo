from compiler.lexer.token import Token, TokenType

from .errors import ParserError


CHECK_TOKEN_TYPES = {
    TokenType.PROCESSES: "PROCESSES",
    TokenType.NETWORK: "NETWORK",
    TokenType.DNS: "DNS",
    TokenType.LOGS: "LOGS",
}


class Parser:
    """Parse JOCKY tokens into a structured representation."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> dict:
        investigation = self._parse_investigation()

        self._expect(
            TokenType.EOF,
            "expected end of input",
        )

        return investigation

    def _parse_investigation(self) -> dict:
        self._expect(
            TokenType.INVESTIGATE,
            "expected 'INVESTIGATE'",
        )

        host_token = self._expect(
            TokenType.IDENTIFIER,
            "expected host identifier after 'INVESTIGATE'",
        )

        self._expect(
            TokenType.LBRACE,
            "expected '{' after host identifier",
        )

        checks = []

        while not self._check(TokenType.RBRACE):
            if self._check(TokenType.EOF):
                token = self._current()

                raise ParserError(
                    "expected '}' before end of input",
                    token.line,
                    token.column,
                )

            checks.append(self._parse_check())

        self._expect(
            TokenType.RBRACE,
            "expected '}' to close investigation",
        )

        return {
            "type": "investigation",
            "host": host_token.value,
            "checks": checks,
        }

    def _parse_check(self) -> str:
        self._expect(
            TokenType.CHECK,
            "expected 'CHECK'",
        )

        token = self._current()

        check_name = CHECK_TOKEN_TYPES.get(token.type)

        if check_name is None:
            raise ParserError(
                "expected one of: PROCESSES, NETWORK, DNS, LOGS",
                token.line,
                token.column,
            )

        self._advance()

        return check_name

    def _current(self) -> Token:
        return self.tokens[self.position]

    def _advance(self) -> Token:
        token = self._current()

        if token.type != TokenType.EOF:
            self.position += 1

        return token

    def _check(self, token_type: TokenType) -> bool:
        return self._current().type == token_type

    def _expect(
        self,
        token_type: TokenType,
        message: str,
    ) -> Token:
        if not self._check(token_type):
            token = self._current()

            raise ParserError(
                message,
                token.line,
                token.column,
            )

        return self._advance()