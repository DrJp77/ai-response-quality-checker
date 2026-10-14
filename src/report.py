import json
import sys
from pathlib import Path

# Pastikan root direktori proyek ada dalam sys.path saat dijalankan langsung
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.metrics import (
    is_empty_or_whitespace,
    validate_required_fields_and_types,
    find_duplicate_prompts,
    find_duplicate_responses,
)


def generate_report(data, output_file=None):
    """Membuat ringkasan kualitas dataset respons AI."""
    if not isinstance(data, list):
        raise ValueError("Data utama harus berupa list JSON.")

    total = len(data)
    empty_responses = []
    invalid_items = []
    duplicate_prompts = find_duplicate_prompts(data)
    duplicate_responses = find_duplicate_responses(data)

    for index, item in enumerate(data):
        item_id = item.get("id", index + 1) if isinstance(item, dict) else index + 1

        valid, errors = validate_required_fields_and_types(item)

        if not valid:
            invalid_items.append({
                "id": item_id,
                "errors": errors,
            })
            continue

        if is_empty_or_whitespace(item.get("response")):
            empty_responses.append(item_id)

    report = {
        "total_items": total,
        "empty_responses": empty_responses,
        "invalid_items": invalid_items,
        "duplicate_prompts": duplicate_prompts,
        "duplicate_responses": duplicate_responses,
    }

    if output_file is not None:
        save_report(report, output_file)

    return report


def save_report(report, output_path=None):
    """Menyimpan ringkasan laporan ke file JSON."""
    if output_path is None:
        output_path = PROJECT_ROOT / "reports" / "quality_report.json"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return output_path


def main():
    data_path = PROJECT_ROOT / "data" / "sample_responses.json"
    output_path = PROJECT_ROOT / "reports" / "quality_report.json"

    with data_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    report = generate_report(data)
    saved_file = save_report(report, output_path)

    print("=== LAPORAN KUALITAS DATA AI ===")
    print(f"Total data: {report['total_items']}")
    print(f"Respons kosong: {report['empty_responses']}")
    print(f"Data tidak valid: {len(report['invalid_items'])}")

    for item in report["invalid_items"]:
        print(f"  ID {item['id']}: {'; '.join(item['errors'])}")

    print(f"Grup prompt duplikat: {len(report['duplicate_prompts'])}")
    print(f"Grup respons duplikat: {len(report['duplicate_responses'])}")
    print(f"Laporan berhasil disimpan ke: {saved_file}")


if __name__ == "__main__":
    main()
