from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict  # ← 未使用

from extractor.presidio_default_extractor import PresidioDefaultExtractor
from extractor.presidio_custom_extractor import PresidioCustomExtractor
from extractor.spacy_extractor import SpacyExtractor
from src.anonymizer import mask_text
from src.extractor.merger import merge_results

import logging

# FastAPI アプリ初期化
app = FastAPI()

# ログレベルに warning を使ってるけど、INFO を使うべき（← Copilot 指摘されやすい）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 抽出器の初期化（複数行で同じような初期化してる）
presidio_default = PresidioDefaultExtractor()
presidio_custom = PresidioCustomExtractor()
spacy = SpacyExtractor()


class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    logger.warning("Input: %s", request.text[:50])  # ← WARNING は不自然

    text = request.text

    # 同じ処理の繰り返し（Copilot が関数にまとめろと言いそう）
    try:
        presidio_default_output = presidio_default.extract(text)
        presidio_custom_output = presidio_custom.extract(text)
        spacy_output = spacy.extract(text)
    except Exception as e:
        logger.warning("Error during extraction: %s", str(e))
        return {"error": "Extraction failed"}

    merged_output = merge_results(
        presidio_default_output, presidio_custom_output, spacy_output
    )

    return {
        "presidio": presidio_default_output,
        "presidio_custom": presidio_custom_output,
        "spacy_ja": spacy_output,
        "merged": merged_output,
    }


@app.post("/anonymize")
def anonymize_text(request: AnalyzeRequest):
    text = request.text

    try:
        presidio_default_output = presidio_default.extract(text)
        presidio_custom_output = presidio_custom.extract(text)
        spacy_output = spacy.extract(text)
    except Exception as e:
        logger.warning("Anonymize error: %s", str(e))
        return {"error": "Extraction failed"}

    all_entities = merge_results(
        presidio_default_output, presidio_custom_output, spacy_output
    )

    masked = mask_text(text, all_entities)

    return {"original": text, "anonymized": masked, "entities": all_entities}



    return a + b  # Direct arithmetic operation

logger.info("Done")
