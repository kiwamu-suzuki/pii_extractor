# まとめ

## 📋 個人情報抽出ツールの比較まとめ

| 方法                            | 説明                                     | 精度                          |
|---------------------------------|------------------------------------------|-------------------------------|
| **Presidio + デフォルト**       | 英語のみ対応                             | ◎（英語） / ×（日本語）       |
| **SpaCy + GiNZA**              | 日本語NERに強い                          | ◎（日本語）                   |
| **Presidio + カスタム正規表現** | 電話番号・メールなど定型情報の検出に強い | ○（ルール依存）               |
| **両方併用**                    | 今回採用方                | ◎（多言語・高精度）           |



起動方法
```
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```




Presidio + デフォルト
SpaCy + GiNZA
Presidio + カスタム正規表現


```
TEXT=$(cat sample2.md | jq -Rs .)
curl -X POST http://localhost:8000/anonymize \
  -H "Content-Type: application/json" \
  -d "{\"text\": $TEXT}" | jq .
```
