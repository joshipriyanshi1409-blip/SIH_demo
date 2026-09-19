import pytest

from compiler.lexer.lexer import Lexer
from compiler.parser.errors import ParserError
from compiler.parser.parser import Parser


def parse(source: str) -> dict:
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_parse_single_dns_check():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
}"""

    result = parse(source)

    assert result == {
        "type": "investigation",
        "host": "HOST01",
        "checks": ["DNS"],
    }


def test_parse_full_investigation():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
}"""

    result = parse(source)

    assert result == {
        "type": "investigation",
        "host": "HOST01",
        "checks": [
            "PROCESSES",
            "NETWORK",
            "DNS",
            "LOGS",
        ],
    }


def test_parse_multiple_checks():
    source = """INVESTIGATE SERVER01 {
    CHECK PROCESSES
    CHECK DNS
}"""

    result = parse(source)

    assert result["host"] == "SERVER01"
    assert result["checks"] == [
        "PROCESSES",
        "DNS",
    ]


def test_missing_investigate_keyword():
    source = """HOST01 {
    CHECK DNS
}"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected 'INVESTIGATE'" in str(error.value)


def test_missing_host():
    source = """INVESTIGATE {
    CHECK DNS
}"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected host identifier" in str(error.value)


def test_missing_opening_brace():
    source = """INVESTIGATE HOST01
    CHECK DNS
}"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected '{'" in str(error.value)


def test_unknown_check():
    source = """INVESTIGATE HOST01 {
    CHECK CPU
}"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected one of" in str(error.value)


def test_missing_closing_brace():
    source = """INVESTIGATE HOST01 {
    CHECK DNS"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected '}'" in str(error.value)


def test_unexpected_text_after_investigation():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
}
HELLO"""

    with pytest.raises(ParserError) as error:
        parse(source)

    assert "expected end of input" in str(error.value)