import os
import requests
import json
import sys

# 환경 변수에서 Azure 엔드포인트와 키 불러오기
endpoint = os.environ.get("AZURE_ENDPOINT")
key = os.environ.get("AZURE_KEY")

if not endpoint or not key:
    print("환경 변수가 설정되지 않았습니다.")
    sys.exit(1)

# 검사할 파일 지정 (여기서는 test.py)
file_to_scan = "test.py"
try:
    with open(file_to_scan, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_to_scan}")
    sys.exit(1)

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

print("Status Code:", response.status_code)
print("Raw Response:", response.text)  # 디버깅용

try:
    result = response.json()
except Exception as e:
    print("JSON 파싱 실패:", e)
    sys.exit(1)

print("분석 결과(JSON):")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 빌드 실패 조건 설정
fail_threshold = 0.8  # 신뢰도 점수 80% 이상이면 실패로 간주

detected = False
for doc in result.get("documents", []):
    for ent in doc.get("entities", []):
        if ent.get("confidenceScore", 0) >= fail_threshold:
            print(f"Detected PII: {ent['text']} "
                  f"({ent['category']}, score={ent['confidenceScore']})")
            detected = True

if detected:
    print("개인정보가 발견되어 Job을 실패 처리합니다.")
    sys.exit(1)
else:
    print("개인정보가 발견되지 않았습니다. Job을 성공 처리합니다.")
    sys.exit(0)
