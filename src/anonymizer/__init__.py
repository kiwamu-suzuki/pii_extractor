from typing import List, Dict


def mask_text(
    text: str, entities: List[Dict], placeholder_fmt: str = "[{label}]"
) -> str:
    """
    抽出されたエンティティをマスキングして置換後のテキストを返す。
    - label: ラベル名を使ったプレースホルダに変換（例：[EMAIL_ADDRESS]）
    """
    # 開始位置で逆順にソート（置換ずれ防止）
    sorted_entities = sorted(entities, key=lambda e: e["start"], reverse=True)
    masked_text = text

    for ent in sorted_entities:
        placeholder = placeholder_fmt.format(label=ent["label"])
        masked_text = (
            masked_text[: ent["start"]] + placeholder + masked_text[ent["end"] :]
        )

    return masked_text
