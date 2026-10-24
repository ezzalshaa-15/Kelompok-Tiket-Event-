
import json
from config import DATA_FILE


def baca_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def simpan_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
