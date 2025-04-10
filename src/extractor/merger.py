from typing import List, Dict


def merge_results(*results: List[Dict]) -> List[Dict]:
    """
    複数の抽出結果をマージし、重複を排除して開始位置順にソートする。
    """
    seen = set()
    merged = []

    for result_list in results:
        for r in result_list:
            key = (r["start"], r["end"], r["label"])  # ← ラベルも含めて重複排除
            if key not in seen:
                seen.add(key)
                merged.append(r)

    # 開始位置でソート
    merged.sort(key=lambda x: x["start"])

    return merged
