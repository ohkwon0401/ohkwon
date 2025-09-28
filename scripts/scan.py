import os
import requests
import json
import sys

# 환경 변수에서 Azure 엔드포인트와 키 불러오기
endpoint = os.environ["AZURE_ENDPOINT"]
key = os.environ["AZURE_KEY"]

# 검사할 파일 지정 (여기서는 test.py)
file_to_scan = "test.py"
with open(file_to_scan, "r", encoding="utf-8") as f:
    content = f.read()

# Azure PII API 엔드포인트
url = f"{endpoint}/text/analytics/v3.1/entities/recognition/pii"

# 요청 헤더
headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

# 요청 바디 (test.py 내용을 전송)
body = {
    "documents": [
        {"id": "1", "language": "ko", "text": content}
    ]
}

# API 호출
response = requests.post(url, headers=headers, json=body)
result = response.json()

# 결과 출력 (JSON 전체)
print("분석 결과(JSON):")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 빌드 실패 조건 설정
fail_threshold = 0.8  # 신뢰도 점수 80% 이상이면 실패로 간주

detected = False
for doc in result.get("documents", []):
    for ent in doc.get("entities", []):
        if ent.get("confidenceScore", 0) >= fail_threshold:
            print(f"Detected PII: {ent['text']} ({ent['category']}, score={ent['confidenceScore']})")
            detected = True

# PII가 탐지되면 Job 실패 처리
if detected:
    print("개인정보가 발견되어 Job을 실패 처리합니다.")
    sys.exit(1)
else
