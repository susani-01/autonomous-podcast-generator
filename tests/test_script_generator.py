from podcast_app.script_generator import parse_script, generate_script


# ── parse_script tests ───────────────────────────────────────
def test_parse_script_basic():
    raw = """HOST1: Hello everyone welcome to the show.
HOST2: Thanks for having me Alex, great to be here.
HOST1: So today we are talking about artificial intelligence.
HOST2: Yes it is a fascinating topic with many implications."""

    result = parse_script(raw)
    assert len(result) == 4
    assert result[0]["speaker"] == "HOST1"
    assert result[1]["speaker"] == "HOST2"


def test_parse_script_alternates():
    raw = """HOST1: First line here.
HOST2: Second line here.
HOST1: Third line here.
HOST2: Fourth line here."""

    result = parse_script(raw)
    speakers = [line["speaker"] for line in result]
    assert speakers == ["HOST1", "HOST2", "HOST1", "HOST2"]


def test_parse_script_ignores_invalid_lines():
    raw = """HOST1: Valid line here.
This line has no speaker prefix.
HOST2: Another valid line.

HOST1: Final valid line."""

    result = parse_script(raw)
    assert len(result) == 3


def test_parse_script_extracts_text():
    raw = "HOST1: This is the extracted text."
    result = parse_script(raw)
    assert result[0]["text"] == "This is the extracted text."


def test_parse_script_empty():
    result = parse_script("")
    assert result == []


# ── generate_script tests ────────────────────────────────────
def test_generate_script_returns_list():
    text = "AI is transforming healthcare with machine learning models."
    result = generate_script(text)
    assert isinstance(result, list)


def test_generate_script_has_both_hosts():
    text = "AI is transforming healthcare with machine learning models."
    result = generate_script(text)
    speakers = [line["speaker"] for line in result]
    assert "HOST1" in speakers
    assert "HOST2" in speakers


def test_generate_script_minimum_lines():
    text = "AI is transforming healthcare with machine learning models."
    result = generate_script(text)
    assert len(result) >= 6


def test_generate_script_no_empty_lines():
    text = "AI is transforming healthcare with machine learning models."
    result = generate_script(text)
    for line in result:
        assert line["text"].strip() != ""
