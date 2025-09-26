import os
import requests

endpoint = os.environ["AZURE_ENDPOINT"]
key = os.environ["AZURE_KEY"]

# 테스트용: 리포지토리 안의 test.py 내용만 검사
file_to_scan = "test.py"
with open(file_to_scan, "r", encoding="utf-8") as f:
    content = f.read()

url = f"{endpoint}/text/analytics/v3.1/entities/recognition/pii"
headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
body = {"documents": [{"id": "1", "language": "ko", "text": content}]}

response = requests.post(url, headers=headers, json=body)
result = response.json()

print("📌 분석 결과:")
print(result)
