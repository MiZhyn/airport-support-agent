import json
import re
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def clean_content(content: str) -> str:
    # 第一步：去掉开头导航栏（"Arrival\n"之后才是真正内容）
    arrival_marker = "All\nFlights\nArrival"
    if arrival_marker in content:
        content = content.split(arrival_marker, 1)[1]

    # 第二步：去掉结尾Footer
    footer_marker = "Changi Airport \nAt Changi"
    if footer_marker in content:
        content = content.split(footer_marker, 1)[0]

    # 第三步：清理多余空行
    lines = [line.strip() for line in content.splitlines()]
    lines = [line for line in lines if line]  # 去掉空行
    content = "\n".join(lines)

    return content.strip()


def clean_name(name: str) -> str:
    # name字段也有噪音，只取第一行
    return name.strip().splitlines()[0]


def clean_file(filename: str):
    filepath = RAW_DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        records = json.load(f)

    cleaned = []
    for record in records:
        cleaned.append({
            "name": clean_name(record["name"]),
            "category": record["category"],
            "url": record["url"],
            "title": record["title"],
            "content": clean_content(record["content"])
        })

    output_path = PROCESSED_DATA_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Cleaned {filename} → {len(cleaned)} records")


def main():
    for json_file in RAW_DATA_DIR.glob("*.json"):
        clean_file(json_file.name)
    print("Done!")


if __name__ == "__main__":
    main()