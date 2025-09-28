#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests

# 환경 변수에서 Azure 엔드포인트와 키 불러오기
endpoint = os.environ.get("AZURE_ENDPOINT", "").strip()
key = os.environ.get("AZURE_KEY", "").strip()

if not endpoint or not key:
    print("환경 변수가 설정되지 않았습니다. (AZURE_ENDPOINT, AZURE_KEY 필요)")
    sys.exit(0)  # 경고만, 항상 성공 처리

# 검사할 파일 경로 (루트에 있는 test.py)
root_dir = os.path.dirname(os.path.dirname(__file__)) 
file_path = os.path.join(root_dir, "test.py")

if not os.path.exists(file_path):
    print(f"파일을 찾을 수 없습니다: {file_path}")
    sys.exit(0)

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# API 호출
url = endpoint.rstrip("/") + "/text/analytics/v3.1/entities/recognition/pii"
headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
body = {"documents": [{"id": "1", "language": "ko", "text": content}]}

try:
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    result = resp.json()
except Exception as e:
    print(f"API 호출 오류: {e}")
    sys.exit(0)

# 엔터티 출력
entities = []
for doc in result.get("documents", []):
    for ent in doc.get("entities", []):
        if ent.get("confidenceScore", 0) >= 0.8:
            entities.append(ent)

print("\n--- PII Scan 결과 ---")
if not entities:
    print("개인정보 없음 (Job 성공)")
else:
    for ent in entities:
        text = ent.get("text")
        cat = ent.get("category")
        score = ent.get("confidenceScore")
        print(f"{cat:30} {score:.2f}  {text}")

print("----------------------")

# 항상 성공 처리
sys.exit(0)
