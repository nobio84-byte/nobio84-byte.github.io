#!/usr/bin/env python3
# Tesla Fleet API 파트너 등록 스크립트
#
# 하는 일:
#   1) 파트너 인증 토큰 발급
#   2) 내 도메인(nobio84-byte.github.io)을 Tesla에 등록
#   3) Tesla가 내 도메인의 공개키를 제대로 가져가는지 확인
#
# 실행 방법 (Termux / Codespace / PC):
#   TESLA_CLIENT_SECRET=여기에시크릿 python3 register_tesla.py
#
#   * Client ID는 비밀이 아니라서 아래에 미리 넣어뒀어요.
#   * Client Secret은 환경변수로만 넘기세요. 이 파일에 적지 마세요.

import os, json, urllib.request, urllib.parse, urllib.error

CLIENT_ID     = "b60e10ca-556c-44bd-98c6-19dbb43c7bb3"   # 비밀 아님
CLIENT_SECRET = os.environ.get("TESLA_CLIENT_SECRET")
DOMAIN        = "nobio84-byte.github.io"
AUDIENCE      = "https://fleet-api.prd.na.vn.cloud.tesla.com"   # 한국=NA 지역
AUTH_URL      = "https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token"
SCOPES        = "openid vehicle_device_data vehicle_location"

if not CLIENT_SECRET:
    raise SystemExit("먼저 TESLA_CLIENT_SECRET 환경변수를 설정하세요.")

def post_form(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# 1) 파트너 인증 토큰
print("[1] 파트너 토큰 발급 중...")
try:
    tok = post_form(AUTH_URL, {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPES,
        "audience": AUDIENCE,
    })
    token = tok["access_token"]
    print("    성공!")
except urllib.error.HTTPError as e:
    print("    실패:", e.code, e.read().decode())
    raise SystemExit

# 2) 파트너 계정 등록
print("[2] 도메인 등록 중:", DOMAIN)
reg = urllib.request.Request(
    f"{AUDIENCE}/api/1/partner_accounts",
    data=json.dumps({"domain": DOMAIN}).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST")
try:
    with urllib.request.urlopen(reg) as r:
        print("    등록 성공 (HTTP", r.status, ")")
        print(json.dumps(json.loads(r.read()), indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print("    등록 응답:", e.code)
    print(e.read().decode())

# 3) 공개키 인식 확인 (Tesla가 내 도메인에서 키를 가져갔는지)
print("[3] 공개키 인식 확인 중...")
chk = urllib.request.Request(
    f"{AUDIENCE}/api/1/partner_accounts/public_key?domain={DOMAIN}",
    headers={"Authorization": f"Bearer {token}"}, method="GET")
try:
    with urllib.request.urlopen(chk) as r:
        print("    HTTP", r.status)
        print(json.dumps(json.loads(r.read()), indent=2, ensure_ascii=False))
        print("\n>>> public_key 값이 보이면 등록+호스팅 모두 성공입니다!")
except urllib.error.HTTPError as e:
    print("    응답:", e.code, e.read().decode())
