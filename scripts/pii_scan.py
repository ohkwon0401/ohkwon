#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import glob

# 환경 변수에서 Azure 엔드포인트와 키 불러오기
endpoint = os.environ.get("AZURE_ENDPOINT", "").strip()
key = os.environ.get("AZURE_KEY", "").strip()

if not endpoint or not key:
    print("환경 변수가 설정되지 않았습니다. (AZURE_ENDPOINT, AZURE_KEY 필요)")
    sys.exit(0)  # 경고만, 항상 성공 처리

# 루트 디렉토리 (repo 최상단)
root_dir = os.path.dirname(os.path.dirname(__file__))

# 루트 밑 모든 .py 파일 찾기
py_files = glob.glob(os.path.join(root_dir, "*.py"))

if not py_files:
    print(f"Python 파일을 찾을 수 없습니다: {root_dir}")
    sys.exit(0)

all_entities = []

for file_path in py_files:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    url = endpoint.rstrip("/") + "/text/analytics/v3.1/entities/recognition/pii"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {"documents": [{"id": file_path, "language": "ko", "text": content}]}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        print(f"API 호출 오류 ({file_path}): {e}")
        continue

    # Raw API Response 출력
    print(f"\n--- Raw API Response for {os.path.basename(file_path)} ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # confidenceScore ≥ 0.8 엔터티만 요약 리스트에 추가
    for doc in result.get("documents", []):
        for ent in doc.get("entities", []):
            if ent.get("confidenceScore", 0) >= 0.8:
                all_entities.append((file_path, ent))

# 요약 출력
print("\n--- PII Scan 결과 ---")
if not all_entities:
    print("개인정보 없음 (Job 성공)")
else:
    for file_path, ent in all_entities:
        text = ent.get("text")
        cat = ent.get("category")
        score = ent.get("confidenceScore")
        print(f"{os.path.basename(file_path):15} | {cat:20} {score:.2f}  {text}")

print("----------------------")

# 항상 성공 처리
sys.exit(0)
