from src.metrics import (
    is_empty_or_whitespace,
    validate_required_fields_and_types,
    find_duplicate_prompts,
    find_duplicate_responses,
)


def test_empty_response():
    assert is_empty_or_whitespace("") is True
    assert is_empty_or_whitespace("   ") is True
    assert is_empty_or_whitespace("   \n\t  ") is True
    assert is_empty_or_whitespace(None) is True
    assert is_empty_or_whitespace(12345) is True
    assert is_empty_or_whitespace("Jawaban valid") is False


def test_required_fields():
    valid, errors = validate_required_fields_and_types({
        "id": 1,
        "prompt": "Apa itu Python?",
        "response": "Python adalah bahasa pemrograman."
    })
    assert valid is True
    assert errors == []


def test_missing_response():
    valid, errors = validate_required_fields_and_types({
        "id": 2,
        "prompt": "Apa itu Python?"
    })
    assert valid is False
    assert any("response" in err for err in errors)


def test_missing_prompt():
    valid, errors = validate_required_fields_and_types({
        "id": 3,
        "response": "Python adalah bahasa pemrograman."
    })
    assert valid is False
    assert any("prompt" in err for err in errors)


def test_invalid_types_in_fields():
    valid, errors = validate_required_fields_and_types({
        "id": 4,
        "prompt": 12345,
        "response": ["bukan", "string"]
    })
    assert valid is False
    assert len(errors) == 2


def test_non_dictionary_item():
    valid, errors = validate_required_fields_and_types("bukan_dict")
    assert valid is False
    assert errors == ["Entri data harus berupa dictionary (objek JSON)."]


def test_duplicate_prompts():
    items = [
        {"id": 1, "prompt": "Apa itu Python?", "response": "A"},
        {"id": 2, "prompt": " apa itu python? ", "response": "B"},
        {"id": 3, "prompt": "Pertanyaan unik", "response": "C"},
        "item_tidak_valid_diabaikan",
    ]
    duplicates = find_duplicate_prompts(items)
    assert "apa itu python?" in duplicates
    assert duplicates["apa itu python?"] == [1, 2]
    assert "pertanyaan unik" not in duplicates


def test_duplicate_responses():
    items = [
        {"id": 1, "prompt": "Pertanyaan A", "response": "Jawaban sama"},
        {"id": 2, "prompt": "Pertanyaan B", "response": " jawaban sama "},
        {"id": 3, "prompt": "Pertanyaan C", "response": "Jawaban beda"},
    ]
    duplicates = find_duplicate_responses(items)
    assert "jawaban sama" in duplicates
    assert duplicates["jawaban sama"] == [1, 2]
    assert "jawaban beda" not in duplicates
