"""
Modul Metrik Kualitas Respons AI (Rule-Based).

PERINGATAN PENTING:
Fungsi-fungsi di dalam modul ini HANYA memeriksa kelengkapan data,
kebersihan teks, dan konsistensi struktur data (data hygiene).
Aturan ini TIDAK menilai atau menjamin apakah isi jawaban benar secara faktual.
"""

from typing import Any, Dict, List, Tuple


def is_empty_or_whitespace(text: Any) -> bool:
    """
    Memeriksa apakah sebuah teks bernilai kosong atau hanya berisi spasi/whitespace.

    Parameter:
        text (Any): Teks yang akan diperiksa (biasanya str).

    Mengembalikan:
        bool: True jika teks kosong, hanya spasi, atau bukan string; False jika berisi teks valid.

    Contoh:
        >>> is_empty_or_whitespace("")
        True
        >>> is_empty_or_whitespace("   \\n\\t  ")
        True
        >>> is_empty_or_whitespace("Halo dunia")
        False
    """
    if text is None:
        return True

    if not isinstance(text, str):
        return True

    # strip() menghapus spasi, tab, dan newline di awal dan akhir string
    return len(text.strip()) == 0


def validate_required_fields_and_types(item: Any) -> Tuple[bool, List[str]]:
    """
    Memeriksa apakah data respons memiliki field wajib ('prompt' dan 'response')
    dan memastikan kedua field tersebut bertipe string (str).

    Parameter:
        item (Any): Satu entri data (seharusnya dictionary).

    Mengembalikan:
        Tuple[bool, List[str]]:
            - bool: True jika struktur lengkap dan tipe data benar, False jika ada masalah.
            - List[str]: Daftar catatan/masalah yang ditemukan.

    Contoh:
        >>> validate_required_fields_and_types({"prompt": "Hai", "response": "Halo"})
        (True, [])
        >>> validate_required_fields_and_types({"prompt": 123})
        (False, ["Field 'response' tidak ditemukan.", "Tipe data 'prompt' harus string, bukan int."])
    """
    issues: List[str] = []

    # Pastikan item berbentuk dictionary
    if not isinstance(item, dict):
        return False, ["Entri data harus berupa dictionary (objek JSON)."]

    # 1. Periksa field 'prompt'
    if "prompt" not in item:
        issues.append("Field wajib 'prompt' tidak ditemukan.")
    elif not isinstance(item["prompt"], str):
        issues.append(f"Tipe data 'prompt' harus teks (str), tetapi ditemukan {type(item['prompt']).__name__}.")

    # 2. Periksa field 'response'
    if "response" not in item:
        issues.append("Field wajib 'response' tidak ditemukan.")
    elif not isinstance(item["response"], str):
        issues.append(f"Tipe data 'response' harus teks (str), tetapi ditemukan {type(item['response']).__name__}.")

    is_valid = len(issues) == 0
    return is_valid, issues


def find_duplicate_prompts(items: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Mendeteksi prompt yang muncul lebih dari satu kali dalam daftar data.

    Parameter:
        items (List[Dict[str, Any]]): Daftar entri data yang akan diperiksa.

    Mengembalikan:
        Dict[str, List[Any]]: Dictionary dengan prompt sebagai key dan
                              daftar ID (atau indeks) yang memiliki prompt tersebut.
                              Hanya prompt yang duplikat yang disertakan.

    Contoh:
        Input data dengan dua prompt sama -> {"Apa itu AI?": [1, 5]}
    """
    prompt_to_ids: Dict[str, List[Any]] = {}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue

        prompt = item.get("prompt")
        # Hanya periksa prompt yang berupa string yang valid
        if isinstance(prompt, str) and prompt.strip():
            # Normalisasi teks: hilangkan spasi berlebih dan ubah ke huruf kecil untuk perbandingan adil
            normalized_prompt = prompt.strip().lower()
            item_id = item.get("id", f"index_{index}")

            if normalized_prompt not in prompt_to_ids:
                prompt_to_ids[normalized_prompt] = []
            prompt_to_ids[normalized_prompt].append(item_id)

    # Ambil hanya prompt yang memiliki lebih dari satu kemunculan
    duplicates = {
        prompt: ids
        for prompt, ids in prompt_to_ids.items()
        if len(ids) > 1
    }

    return duplicates


def find_duplicate_responses(items: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Mendeteksi jawaban (response) yang identik/duplikat dalam daftar data.

    Parameter:
        items (List[Dict[str, Any]]): Daftar entri data yang akan diperiksa.

    Mengembalikan:
        Dict[str, List[Any]]: Dictionary dengan teks jawaban sebagai key dan
                              daftar ID yang memiliki jawaban tersebut.
                              Hanya jawaban yang duplikat yang disertakan.
    """
    response_to_ids: Dict[str, List[Any]] = {}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue

        response = item.get("response")
        if isinstance(response, str) and response.strip():
            normalized_response = response.strip().lower()
            item_id = item.get("id", f"index_{index}")

            if normalized_response not in response_to_ids:
                response_to_ids[normalized_response] = []
            response_to_ids[normalized_response].append(item_id)

    duplicates = {
        resp: ids
        for resp, ids in response_to_ids.items()
        if len(ids) > 1
    }

    return duplicates
