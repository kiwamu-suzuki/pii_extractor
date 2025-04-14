from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

from extractor.presidio_default_extractor import PresidioDefaultExtractor
from extractor.presidio_custom_extractor import PresidioCustomExtractor
from extractor.spacy_extractor import SpacyExtractor
from src.anonymizer import mask_text
from src.extractor.merger import merge_results


# FastAPI アプリ初期化
app = FastAPI()

# ロギングの設定
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 抽出器の初期化
presidio_default = PresidioDefaultExtractor()
presidio_custom = PresidioCustomExtractor()
spacy = SpacyExtractor()


# リクエストボディのスキーマ
class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    logger.info("analyze_text called with input: %s", request.text[:50] + ("..." if len(request.text) > 50 else ""))
    text = request.text

    # 各抽出器でPIIを検出
    presidio_default_output = presidio_default.extract(text)
    presidio_custom_output = presidio_custom.extract(text)
    spacy_output = spacy.extract(text)

    # 統合処理（必要に応じてマージ or 分離出力）
    merged_output = merge_results(
        presidio_default_output, presidio_custom_output, spacy_output
    )

    response = {
        "presidio": presidio_default_output,
        "presidio_custom": presidio_custom_output,
        "spacy_ja": spacy_output,
        "merged": merged_output,
    }
    logger.info("analyze_text response: %s", response)
    return response


@app.post("/anonymize")
def anonymize_text(request: AnalyzeRequest):
    print("anonymize_text called")
    text = request.text

    # 各抽出器で検出
    presidio_default_output = presidio_default.extract(text)
    presidio_custom_output = presidio_custom.extract(text)
    spacy_output = spacy.extract(text)

    all_entities = merge_results(
        presidio_default_output, presidio_custom_output, spacy_output
    )

    masked = mask_text(text, all_entities)

    return {"original": text, "anonymized": masked, "entities": all_entities}
