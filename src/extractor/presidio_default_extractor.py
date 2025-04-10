from presidio_analyzer import AnalyzerEngine
from typing import List, Dict
from .base import BasePIIExtractor


class PresidioDefaultExtractor(BasePIIExtractor):
    def __init__(self):
        # PresidioのAnalyzerを初期化
        self.analyzer = AnalyzerEngine()

    def extract(self, text: str) -> List[Dict]:
        # デフォルトのエンティティ（EMAIL, PHONE_NUMBER, PERSONなど）を全件抽出
        results = self.analyzer.analyze(
            text=text, language="en"  # 英語のみ対応（Presidioデフォルト）
        )

        return [
            {
                "entity": text[r.start : r.end],
                "label": r.entity_type,
                "start": r.start,
                "end": r.end,
            }
            for r in results
        ]
