import json
import pytest
from src.report import generate_report, save_report


def test_generate_report_invalid_input_type():
    with pytest.raises(ValueError, match="Data utama harus berupa list JSON."):
        generate_report("bukan_list")

    with pytest.raises(ValueError, match="Data utama harus berupa list JSON."):
        generate_report(None)


def test_generate_report_empty_dataset():
    report = generate_report([])
    assert report["total_items"] == 0
    assert report["empty_responses"] == []
    assert report["invalid_items"] == []
    assert report["duplicate_prompts"] == {}
    assert report["duplicate_responses"] == {}


def test_generate_report_valid_and_invalid_data():
    dataset = [
        {"id": 1, "prompt": "Halo", "response": "Hai"},
        {"id": 2, "prompt": "Halo", "response": "   "},
        {"id": 3, "prompt": 123, "response": "Tes"},
    ]
    report = generate_report(dataset)

    assert report["total_items"] == 3
    assert report["empty_responses"] == [2]
    assert len(report["invalid_items"]) == 1
    assert report["invalid_items"][0]["id"] == 3
    assert "duplicate_prompts" in report


def test_generate_report_with_non_dict_items():
    """Pastikan item yang bukan dictionary (string, angka, None) dilaporkan sebagai tidak valid."""
    dataset = [
        "string_saja",
        12345,
        None,
        {"id": 4, "prompt": "Valid", "response": "Jawaban valid"}
    ]
    report = generate_report(dataset)

    assert report["total_items"] == 4
    assert len(report["invalid_items"]) == 3
    assert report["invalid_items"][0]["id"] == 1
    assert report["invalid_items"][0]["errors"] == ["Entri data harus berupa dictionary (objek JSON)."]
    assert report["invalid_items"][1]["id"] == 2
    assert report["invalid_items"][2]["id"] == 3


def test_save_report_creates_valid_json(tmp_path):
    """Pastikan save_report menghasilkan file JSON yang valid dan bisa dibaca kembali."""
    dummy_report = {
        "total_items": 1,
        "empty_responses": [],
        "invalid_items": [],
        "duplicate_prompts": {},
        "duplicate_responses": {},
    }
    target_file = tmp_path / "reports_sub" / "test_report.json"
    saved_path = save_report(dummy_report, target_file)

    # File harus ada setelah disimpan
    assert saved_path.exists()

    # Isi file harus identik dengan data aslinya
    with saved_path.open("r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == dummy_report


def test_generate_report_auto_saves(tmp_path):
    """Pastikan generate_report menyimpan file otomatis jika output_file diberikan."""
    dataset = [{"id": 1, "prompt": "Hai", "response": "Halo"}]
    target_file = tmp_path / "auto_saved_report.json"
    report = generate_report(dataset, output_file=target_file)

    assert target_file.exists()
    with target_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data["total_items"] == 1
    assert saved_data["total_items"] == report["total_items"]


def test_report_contains_all_required_keys():
    """Pastikan struktur kunci laporan selalu lengkap."""
    report = generate_report([])
    required_keys = {"total_items", "empty_responses", "invalid_items",
                     "duplicate_prompts", "duplicate_responses"}
    assert required_keys == set(report.keys())


def test_all_invalid_items_have_id_and_errors():
    """Pastikan setiap item tidak valid di laporan selalu memiliki 'id' dan 'errors'."""
    dataset = [
        {"id": 10, "prompt": 999, "response": None},
        "bukan_dict",
    ]
    report = generate_report(dataset)
    for invalid in report["invalid_items"]:
        assert "id" in invalid
        assert "errors" in invalid
        assert isinstance(invalid["errors"], list)
        assert len(invalid["errors"]) > 0
