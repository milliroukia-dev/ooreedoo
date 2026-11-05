#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚡ MATRIX BOT — OTP AUTO + PROXY"""

import requests, time, re, json, threading, logging, sys, uuid, base64, os, urllib3
from urllib.parse import urlencode
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from curl_cffi import requests as cffi_requests
except ImportError:
    print("❌ خطأ: يجب تثبيت curl_cffi. شغّل: pip install curl_cffi")
    sys.exit(1)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.FileHandler("bot.log", encoding="utf-8"), logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════════════
TG_TOKEN = "9031031074:AAHidY49JmeBrkxdozhvqROmN4CamZKBDm8"
ADMIN_ID = 1376499277
TG_API = f"https://api.telegram.org/bot{TG_TOKEN}"

OOREDOO_BFF = "https://apis.ooredoo.dz/api/ooredoo-bff"
OOREDOO_AUTH = "https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
SIG_OLD = "5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"
SIG_NEW = "c66054ba6166fe08d1a6a702fb10b151102a6f4ef058fcf3d995ee511ff0d267"

INTEGRITY_1 = "JWBTpxXcH7Lj62P2Co1K2MeNBT3Rs3zCoOecqTpHjjg22fg6Ia0Hs0eV+zSVHSTeI6aj9Te+ZCat/+nYgoVz6BJjGqfngWihy6l4cToHXIbqpd+8SxN+NZwHqX07Otv+xN2lQdw9EeLr7a/CTE75io3M3p5C3LliiPx8HhnAKWLs2nUG2nAjEvWwsGDBSDKR7OWiFvVxo96xYKYHBdYxQZgbNVlr2QpzRiH4qG6471/75qGmu5AFKA+Dw8LMqeOK5hpUQ3K7JUCzdXluRmVZifGlQMHdz+VzGpq/rdPqCXwTmo1RojPl/BjOXcW+4FxIW6ZYKHUjs0nrmZyN4WVb8J71dgZ8JcaTNziuTNoe3XXX/Cvxu272Z1bu624jJtboIO4S2zPz9sAHNLLlt1WgTHsXR5Jh+j1qD1y+LJWFhSkU83ez2kxjc/8mkRkJICuxJdBG+ZxafaSwHBJYIBVf7GKtVkzSNFpAsrQlZF/+G6pG71EydFiSWcuRMW7Ze/Hj5eXRYHmkLaZwrBNwR+u6xeAOVmHdo97BCHqnCHKaBHhk1wqjoerA3azue+O3Xjrp+XGaXK6fByY5C7ThIWsiODfPbV25FmhWmkfnrReB/O7kLOCAIZ6chSXYaa6o2xPsF32hWim8ll9lAog7Z1mPQYC474Djh0UxxyaOOgdC61YMrEjTt+XKLVdz8Qq8SDOqlBZTQEbSNAe5mRIB/WpEKKgL46sn2bMvS4HFIDughHmOpfh0KeA2zW8P2h0M"
INTEGRITY_2 = "JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/UgaNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9AwKwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GPuJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQsEDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlDhZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjwrOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4HWXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW"

# ✅ تم إضافة البروكسي الجزائري هنا
PROXY_URL = "http://ykomqegpms-pool-res-country-DZ-state-2485920-mode-hold-tier-premium-session-6aec530e79283:nJt4EINSN3trVnya@185.185.51.243:9999"

# ════════════════════════════════════════════════════════════════════════════
# SESSIONS
# ════════════════════════════════════════════════════════════════════════════
_oo = cffi_requests.Session(
    impersonate="chrome_android",
    proxies={"http": PROXY_URL, "https": PROXY_URL}
)
_tg = cffi_requests.Session()

logger.info("✅ Proxy enabled: 185.185.51.243:9999")

_users, _sess = {}, {}

def save():
    try: open("data.json","w").write(json.dumps({str(k):v for k,v in _users.items()}))
    except: pass

def load():
    try:
        for k,v in json.load(open("data.json")).items(): _users[int(k)] = v
    except: pass

def new_iid():
    u = uuid.uuid4().hex
    return f"{u[:8]}-{u[8:12]}-11{u[12:16]}-{u[16:20]}-{u[20:32]}{int(time.time()*1000)}"

def new_psig(iid):
    p = json.dumps({"platform":"android","is-physical-device":True,"device-id":iid}, separators=(',',':'))
    return base64.b64encode(p.encode()).decode()

def new_fp(): return uuid.uuid4().hex + uuid.uuid4().hex[:32]
def new_corr(): return uuid.uuid4().hex + str(int(time.time()*1000))
def now_ms(): return str(int(time.time()*1000))
def now_iso(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def mask(m):
    if not m: return "—"
    s = str(m).strip()
    if s.startswith("213") and len(s) == 12: s = "0" + s[3:]
    return s[:2] + "x"*(len(s)-4) + s[-2:] if len(s) >= 8 else s

def http(method, url, headers, body="", timeout=25):
    try:
        if method == "GET": r = _oo.get(url, headers=headers, timeout=timeout, verify=False)
        else: r = _oo.post(url, headers=headers, data=body, timeout=timeout, verify=False)
        try: j = r.json()
        except: j = None
        return {"code": r.status_code, "body": r.text, "headers": {k.lower(): v for k, v in r.headers.items()}, "json": j}
    except Exception as e:
        logger.error(f"HTTP Error: {e}")
        return None

def base_h(msisdn, fp, corr, ts, iid, psig):
    return {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn, "x-device-fingerprint": fp, "x-platform-origin": "mobile-android", "x-correlation-id": corr, "platform": "android", "x-version": "1.5.17", "x-signature": SIG_OLD, "accept": "*/*", "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid}

# ════════════════════════════════════════════════════════════════════════════
# OTP LOGIC
# ════════════════════════════════════════════════════════════════════════════
def send_otp(msisdn):
    iid = new_iid(); psig = new_psig(iid); fp = new_fp()
    for _ in range(2):
        try:
            ts = now_ms()
            http("GET", f"{OOREDOO_BFF}/users/status?msisdn={msisdn}", base_h(msisdn, fp, new_corr(), ts, iid, psig), timeout=15)
            h3 = base_h(msisdn, fp, new_corr(), ts, iid, psig)
            h3.update({"content-type": "application/json; charset=utf-8", "x-native-integrity-token": INTEGRITY_1, "x-path": "/api/auth/realms/myooredoo/protocol/openid-connect/token", "x-method": "POST"})
            r3 = http("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, "{}")
            if not r3: continue
            nonce = r3["headers"].get("x-nonce-id"); chronos = r3["headers"].get("x-chronos-id")
            if not nonce: continue
            h4 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn, "x-device-fingerprint": fp, "x-nonce-id": nonce, "x-platform-origin": "mobile-android", "platform": "android", "x-version": "1.5.17", "x-signature": SIG_OLD, "x-chronos-id": chronos, "x-timestamp": ts, "x-platform-info": psig, "x-force-update": "true", "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded"}
            r4 = http("POST", OOREDOO_AUTH, h4, urlencode({"client_id": "myooredoo-app", "grant_type": "password", "username": msisdn}), timeout=20)
            if r4 and r4["code"] in (200, 401, 403): return {"ok": True, "iid": iid, "psig": psig, "fp": fp}
        except: time.sleep(3)
    return {"error": "failed"}

def verify_otp(msisdn, otp, device):
    iid = device["iid"]; psig = device["psig"]; fp = device["fp"]
    for _ in range(2):
        try:
            ts = now_ms()
            h6 = base_h(msisdn, fp, new_corr(), ts, iid, psig)
            h6.update({"content-type": "application/json; charset=utf-8", "x-native-integrity-token": INTEGRITY_2, "x-path": "/api/auth/realms/myooredoo/protocol/openid-connect/token", "x-method": "POST"})
            r6 = http("POST", f"{OOREDOO_BFF}/checkpoint/token", h6, "{}")
            if not r6: continue
            n2 = r6["headers"].get("x-nonce-id"); c2 = r6["headers"].get("x-chronos-id")
            if not n2: continue
            h7 = {"User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip", "x-msisdn": msisdn, "x-device-fingerprint": fp, "x-nonce-id": n2, "x-platform-origin": "mobile-android", "platform": "android", "x-version": "1.5.17", "x-signature": SIG_OLD, "x-chronos-id": c2, "x-timestamp": ts, "x-platform-info": psig, "x-force-update": "true", "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded"}
            r7 = http("POST", OOREDOO_AUTH, h7, urlencode({"client_id": "myooredoo-app", "grant_type": "password", "username": msisdn, "otp": otp}), timeout=20)
            if not r7: continue
            if r7["code"] in (401, 403): return "wrong_otp"
            if r7["code"] == 200 and r7.get("json", {}).get("access_token"):
                return {"access_token": r7["json"]["access_token"], "refresh_token": r7["json"].get("refresh_token", ""), "iid": iid, "psig": psig}
        except: time.sleep(3)
    return False

# ════════════════════════════════════════════════════════════════════════════
# BUNDLES
# ════════════════════════════════════════════════════════════════════════════
def refresh_token(user):
    rt = user.get("refresh_token")
    if not rt: return False
    h = {"User-Agent": "Dart/3.11 (dart:io)", "Content-Type": "application/x-www-form-urlencoded", "x-msisdn": user["msisdn"], "platform": "android", "x-version": "1.5.17", "x-signature": SIG_OLD}
    r = http("POST", OOREDOO_AUTH, h, urlencode({"client_id": "myooredoo-app", "grant_type": "refresh_token", "refresh_token": rt}), timeout=20)
    if r and r["code"] == 200: return r["json"]
    return False

def buy_bundle(user, bundle_code, bundle_name):
    new_tok = refresh_token(user)
    if new_tok:
        user["access_token"] = new_tok["access_token"]
        if "refresh_token" in new_tok: user["refresh_token"] = new_tok["refresh_token"]
        save()

    iid = user.get("iid") or new_iid()
    psig = user.get("psig") or new_psig(iid)
    body = json.dumps({"bundleCode": bundle_code}, separators=(',',':'))
    h = {"x-msisdn": user["msisdn"], "user-agent": "Dart/3.11 (dart:io)", "x-device-fingerprint": new_fp(), "accept-encoding": "gzip", "x-platform-origin": "mobile-android", "authorization": f"Bearer {user['access_token']}", "x-correlation-id": new_corr(), "content-type": "application/json; charset=utf-8", "platform": "android", "x-version": "1.5.17", "x-signature": SIG_NEW, "accept": "*/*", "content-length": str(len(body)), "host": "apis.ooredoo.dz", "x-platform-data-signature": psig, "x-timestamp": now_iso(), "x-instance-id": iid}
    r = http("POST", f"{OOREDOO_BFF}/cvm/dynamic-bundle-purchase", h, body, timeout=20)
    if not r: return "net"
    c = r["code"]; b = (r.get("body") or "").lower()
    if c in (200, 201, 204): return "success"
    if c == 401: return "auth"
    if c in (400, 409, 500) and any(k in b for k in ["already","deja","مسبق","استفدت","used","24h"]): return "already"
    return f"HTTP {c}"

# ════════════════════════════════════════════════════════════════════════════
# TELEGRAM
# ════════════════════════════════════════════════════════════════════════════
def tg_req(method, **kw):
    try: return _tg.post(f"{TG_API}/{method}", json=kw, timeout=10).json()
    except: return None

def tg_send(cid, txt, kb=None):
    p = {"chat_id": cid, "text": txt, "parse_mode": "HTML"}
    if kb is not None: p["reply_markup"] = {"keyboard": kb, "resize_keyboard": True}
    else: p["reply_markup"] = {"remove_keyboard": True}
    return tg_req("sendMessage", **p)

def tg_btn(cid, txt, rows): return tg_send(cid, txt, [[{"text": b} for b in r] for r in rows])

def menu_main(cid):
    tg_btn(cid, "اختر 👇🏻", [
        ["🎁 هدية 2Go", "🎯 اشتراك الوفاء 1Go"],
        ["💎 L'AFFAIRE 90DA", "🚪 خروج"]
    ])

def do_2go(cid, user):
    tg_send(cid, "⏳ تفعيل 2Go...")
    res = buy_bundle(user, "BTL_24H_DATA_Free_2Go", "2Go")
    if res == "success": tg_btn(cid, "🎉 تم تفعيل 2Go!", [["🔙 رجوع"]])
    elif res == "already": tg_btn(cid, "⚠️ استفدت مسبقاً", [["🔙 رجوع"]])
    elif res == "auth": tg_btn(cid, "❌ التوكن منتهي. أرسل /start وضع توكن جديد.", [["🔙 رجوع"]])
    else: tg_btn(cid, f"❌ فشل: {res}", [["🔙 رجوع"]])

def do_wafaa(cid, user):
    tg_send(cid, "⏳ تفعيل اشتراك الوفاء 1Go...")
    res = buy_bundle(user, "BTL_24H_DATA_20DZD_1Go", "وفاء 1Go")
    if res == "success": tg_btn(cid, f"🎉 تم التفعيل!\n📱 {mask(user['msisdn'])}", [["🔙 رجوع"]])
    elif res == "already": tg_btn(cid, "⚠️ استفدت مسبقاً", [["🔙 رجوع"]])
    elif res == "auth": tg_btn(cid, "❌ التوكن منتهي. أرسل /start وضع توكن جديد.", [["🔙 رجوع"]])
    else: tg_btn(cid, f"❌ فشل: {res}", [["🔙 رجوع"]])

def do_affaire(cid, user):
    tg_send(cid, "⏳ تفعيل L'AFFAIRE 90...")
    res = buy_bundle(user, "ATL_24H_DATA_90DZD_5Go", "L'AFFAIRE 90")
    if res == "success": tg_btn(cid, "🎉 تم تفعيل 5Go!", [["🔙 رجوع"]])
    elif res == "already": tg_btn(cid, "⚠️ استفدت مسبقاً", [["🔙 رجوع"]])
    elif res == "auth": tg_btn(cid, "❌ التوكن منتهي. أرسل /start وضع توكن جديد.", [["🔙 رجوع"]])
    else: tg_btn(cid, f"❌ فشل: {res}", [["🔙 رجوع"]])

def handle(cid, txt):
    txt = txt.strip()
    s, u = _sess.get(cid, {}), _users.get(cid)
    
    if txt == "/start":
        if u and u.get("access_token"): return menu_main(cid)
        _sess[cid] = {"state": "phone"}
        return tg_send(cid, "👋 أرسل رقم أوريدو (05XXXXXXXX):")
    
    if s.get("state") == "phone":
        dg = "".join(c for c in txt if c.isdigit())
        if not re.match(r'^0[567]\d{8}$', dg): return tg_send(cid, "❌ رقم خطأ")
        msisdn = "213" + dg[1:]
        
        _sess[cid] = {"state": "otp", "msisdn": msisdn}
        tg_btn(cid, "⏳ جاري إرسال OTP عبر البروكسي...", [["📱 تغيير الرقم"]])
        
        def _bg():
            res = send_otp(msisdn)
            if res.get("ok"):
                _sess[cid]["device"] = res
                tg_btn(cid, "✅ تم إرسال OTP.\n🔑 أدخل الرمز:", [["🔄 تجديد", "📱 تغيير الرقم"]])
            else:
                tg_btn(cid, "⚠️ فشل الإرسال، حاول لاحقاً.", [["📱 تغيير الرقم"]])
        threading.Thread(target=_bg, daemon=True).start()
        return

    if s.get("state") == "otp":
        if txt == "📱 تغيير الرقم":
            _sess[cid] = {"state": "phone"}
            return tg_send(cid, "📱 أرسل رقمك:")
        if txt == "🔄 تجديد":
            msisdn = s["msisdn"]
            tg_btn(cid, "⏳ جاري الإرسال...", [["📱 تغيير الرقم"]])
            def _resend():
                res = send_otp(msisdn)
                if res.get("ok"):
                    _sess[cid]["device"] = res
                    tg_btn(cid, "✅ تم الإرسال.\n🔑 أدخل الرمز:", [["🔄 تجديد", "📱 تغيير الرقم"]])
                else: tg_btn(cid, "⚠️ فشل", [["📱 تغيير الرقم"]])
            threading.Thread(target=_resend, daemon=True).start()
            return
        
        if not txt.isdigit() or len(txt) != 6:
            return tg_btn(cid, "❌ OTP = 6 أرقام", [["🔄 تجديد", "📱 تغيير الرقم"]])
        
        device = s.get("device")
        if not device: return tg_send(cid, "❌ انتهت الجلسة. أعد المحاولة.")
        
        tg_send(cid, "⏳ جاري التحقق...")
        res = verify_otp(s["msisdn"], txt, device)
        if res == "wrong_otp": return tg_btn(cid, "❌ رمز خاطئ", [["🔄 تجديد", "📱 تغيير الرقم"]])
        if not res: return tg_send(cid, "❌ فشل التحقق.")
        
        _users[cid] = {"msisdn": s["msisdn"], **res}
        save(); _sess.pop(cid, None)
        tg_send(cid, "🎉 تم الدخول!")
        return menu_main(cid)

    if not u or not u.get("access_token"):
        _sess[cid] = {"state": "phone"}
        return tg_send(cid, "📱 أرسل رقمك:")
    
    if txt == "🎁 هدية 2Go": return threading.Thread(target=do_2go, args=(cid, u), daemon=True).start()
    if txt == "🎯 اشتراك الوفاء 1Go": return threading.Thread(target=do_wafaa, args=(cid, u), daemon=True).start()
    if txt == "💎 L'AFFAIRE 90DA": return threading.Thread(target=do_affaire, args=(cid, u), daemon=True).start()
    
    if txt == "🚪 خروج":
        _users.pop(cid, None); save()
        return tg_send(cid, "✅ خرجت. /start للبدء.")
    if txt == "🔙 رجوع": return menu_main(cid)
    menu_main(cid)

def poll():
    _tg.get(f"{TG_API}/deleteWebhook", params={"drop_pending_updates": "true"})
    off = None
    while True:
        try:
            r = _tg.get(f"{TG_API}/getUpdates", params={"timeout":15,"offset":off}, timeout=(10,20)).json()
            if r.get("ok"):
                for u in r.get("result",[]):
                    off = u["update_id"] + 1
                    if msg := u.get("message"):
                        cid = msg.get("chat",{}).get("id"); txt = msg.get("text","").strip()
                        if cid and txt: threading.Thread(target=handle, args=(cid, txt), daemon=True).start()
        except: time.sleep(2)

if __name__ == "__main__":
    load()
    try: poll()
    except KeyboardInterrupt: save()