from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from typing import List, Dict
from .base import BasePIIExtractor


class PresidioCustomExtractor(BasePIIExtractor):
    def __init__(self):
        self.analyzer = AnalyzerEngine()

        # カスタムパターンの定義（必要に応じて追加）
        self._register_custom_patterns()

    def _register_custom_patterns(self):
        custom_patterns = [
            {
                "name": "JP_PHONE",
                "regex": r"\b0\d{1,4}-\d{1,4}-\d{4}\b",
                "entity": "JP_PHONE_NUMBER",
                "score": 0.85,
            },
            {
                "name": "JP_POSTAL",
                "regex": r"\b\d{3}-\d{4}\b",
                "entity": "JP_POSTAL_CODE",
                "score": 0.8,
            },
            {
                "name": "MY_NUMBER",
                "regex": r"\b\d{12}\b",
                "entity": "JP_MY_NUMBER",
                "score": 0.9,
            },
        ]

        for pattern in custom_patterns:
            recognizer = PatternRecognizer(
                supported_entity=pattern["entity"],
                patterns=[
                    Pattern(
                        name=pattern["name"],
                        regex=pattern["regex"],
                        score=pattern["score"],
                    )
                ],
            )
            self.analyzer.registry.add_recognizer(recognizer)

    def extract(self, text: str) -> List[Dict]:
        # 明示的にカスタムエンティティのみを抽出
        entities = ["JP_PHONE_NUMBER", "JP_POSTAL_CODE", "JP_MY_NUMBER"]
        results = self.analyzer.analyze(text=text, language="en", entities=entities)

        return [
            {
                "entity": text[r.start : r.end],
                "label": r.entity_type,
                "start": r.start,
                "end": r.end,
            }
            for r in results
        ]
