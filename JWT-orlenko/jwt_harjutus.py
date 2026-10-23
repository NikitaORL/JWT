import base64
import hashlib
import hmac
import json
from datetime import datetime
from zoneinfo import ZoneInfo

token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz"
         "dWIiOiIxMDI0IiwibmFtZSI6Ik1hcmkgTWFhc2lrYXMiLCJyb2x"
         "lIjoic3R1ZGVudCIsImlhdCI6MTc2MTIwNjQwMCwiZXhwIjoxNzYxM"
         "EwMDAwfQ.ZL6DsKKTa2hRmEkkMASGBI7hZW8ot5bJS2I8oOxVTwM")

def b64url_decode(tekst):
    tekst += "=" * (-len(tekst) % 4)
    return base64.urlsafe_b64decode(tekst)

def b64url_encode(baidid):
    return base64.urlsafe_b64encode(baidid).rstrip(b"=").decode()


pais_b64, payload_b64, allkiri_b64 = token.split(".")
pais = json.loads(b64url_decode(pais_b64))
payload = json.loads(b64url_decode(payload_b64))
print("Päis:", pais)
print("Payload:", payload)

tz = ZoneInfo("Europe/Tallinn")
print("Väljastatud:", datetime.fromtimestamp(payload["iat"], tz))
print("Aegub:", datetime.fromtimestamp(payload["exp"], tz))
print("Kehtib praegu:", datetime.now(tz).timestamp() < payload["exp"])



def allkirjasta(pais_b64, payload_b64, voti):
    sisend = f"{pais_b64}.{payload_b64}".encode()
    raasi = hmac.new(voti.encode(), sisend, hashlib.sha256).digest()
    return b64url_encode(raasi)

arvutatud_allkiri = allkirjasta(pais_b64, payload_b64, "saladus123")
print("Arvutatud allkiri:", arvutatud_allkiri)
print("Tokeni allkiri:    ", allkiri_b64)



print("Õige võti:", arvutatud_allkiri.strip() == allkiri_b64.strip())



voltsitud = dict(payload, role="admin")
voltsitud_b64 = b64url_encode(json.dumps(voltsitud, separators=(",", ":")).encode())
voltsitud_token = f"{pais_b64}.{voltsitud_b64}.{allkiri_b64}"
print("Võltsing läbib kontrolli:", allkirjasta(pais_b64, voltsitud_b64, "saladus123") == allkiri_b64)