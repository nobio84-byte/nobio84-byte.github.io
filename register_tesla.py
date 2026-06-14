import os, json, urllib.request, urllib.parse
cid = "b60e10ca-556c-44bd-98c6-19dbb43c7bb3"
cs = os.environ["TESLA_CLIENT_SECRET"]
dom = "nobio84-byte.github.io"
aud = "https://fleet-api.prd.na.vn.cloud.tesla.com"
body = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": cid, "client_secret": cs, "scope": "openid vehicle_device_data vehicle_location", "audience": aud}).encode()
tok = json.load(urllib.request.urlopen(urllib.request.Request("https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token", data=body)))
t = tok["access_token"]
print("[1] token OK")
req = urllib.request.Request(aud + "/api/1/partner_accounts", data=json.dumps({"domain": dom}).encode(), headers={"Authorization": "Bearer " + t, "Content-Type": "application/json"})
print("[2] register:", urllib.request.urlopen(req).read().decode())
chk = urllib.request.Request(aud + "/api/1/partner_accounts/public_key?domain=" + dom, headers={"Authorization": "Bearer " + t})
print("[3] public_key:", urllib.request.urlopen(chk).read().decode())
