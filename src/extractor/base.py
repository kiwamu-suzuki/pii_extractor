from abc import ABC, abstractmethod
from typing import List, Dict


class BasePIIExtractor(ABC):
    """
    PII抽出器の共通インターフェース。
    すべての抽出器はこのクラスを継承して extract() を実装すること。
    """

    @abstractmethod
    def extract(self, text: str) -> List[Dict]:
        """
        入力テキストから個人情報エンティティを抽出し、
        エンティティ情報のリストを返す。

        戻り値の各要素は以下の形式の辞書とする：
        {
            "entity": str,      # 実際の文字列
            "label": str,       # エンティティ種別（PERSON, EMAIL など）
            "start": int,       # テキスト内の開始インデックス
            "end": int          # 終了インデックス
        }
        """
        pass
