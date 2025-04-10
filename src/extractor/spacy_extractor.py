import spacy
from typing import List, Dict
from .base import BasePIIExtractor


class SpacyExtractor(BasePIIExtractor):
    def __init__(self, model_name: str = "ja_ginza"):
        """
        SpaCyの日本語モデルをロードする。
        例: "ja_ginza", "ja_core_news_sm", "ja_core_news_trf" など
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError as e:
            raise RuntimeError(
                f"spaCyモデル '{model_name}' の読み込みに失敗しました。事前にダウンロードしてください。"
            ) from e

    def extract(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        return [
            {
                "entity": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            }
            for ent in doc.ents
        ]
