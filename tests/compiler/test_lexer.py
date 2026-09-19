import pytest

from compiler.lexer.errors import LexerError
from compiler.lexer.lexer import Lexer
from compiler.lexer.token import TokenType


def test_lex_simple_check():
    source = "CHECK DNS"

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens] == [
        TokenType.CHECK,
        TokenType.DNS,
        TokenType.EOF,
    ]


def test_lex_full_investigation():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
}"""

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens] == [
        TokenType.INVESTIGATE,
        TokenType.IDENTIFIER,
        TokenType.LBRACE,
        TokenType.CHECK,
        TokenType.PROCESSES,
        TokenType.CHECK,
        TokenType.NETWORK,
        TokenType.CHECK,
        TokenType.DNS,
        TokenType.CHECK,
        TokenType.LOGS,
        TokenType.RBRACE,
        TokenType.EOF,
    ]


def test_keywords_are_case_insensitive():
    source = "check dns"

    tokens = Lexer(source).tokenize()

    assert tokens[0].type == TokenType.CHECK
    assert tokens[1].type == TokenType.DNS


def test_identifier_preserves_original_value():
    source = "HOST_01"

    tokens = Lexer(source).tokenize()

    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "HOST_01"


def test_comments_are_ignored():
    source = """# comment
CHECK DNS # another comment
"""

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens] == [
        TokenType.CHECK,
        TokenType.DNS,
        TokenType.EOF,
    ]


def test_braces_are_tokenized():
    source = "{}"

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens] == [
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.EOF,
    ]


def test_line_and_column_are_tracked():
    source = """CHECK DNS
CHECK LOGS"""

    tokens = Lexer(source).tokenize()

    assert tokens[0].line == 1
    assert tokens[0].column == 1

    assert tokens[1].line == 1
    assert tokens[1].column == 7

    assert tokens[2].line == 2
    assert tokens[2].column == 1


def test_invalid_character_raises_error():
    source = "CHECK @"

    with pytest.raises(LexerError) as error:
        Lexer(source).tokenize()

    assert "unexpected character '@'" in str(error.value)
    assert "line 1" in str(error.value)
    assert "column 7" in str(error.value)