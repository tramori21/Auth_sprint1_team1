from pathlib import Path
import re

p = Path("src/core/security.py")
t = p.read_text(encoding="utf-8")

# гарантируем импорты time/datetime
need = [
    "import time",
    "from datetime import datetime, timedelta",
]
for line in need:
    if line not in t:
        # добавляем рядом с существующими импортами datetime
        t = re.sub(r"(?m)^(from datetime import .+)$", r"\1\n" + line, t, count=1)
        if line not in t:
            # если datetime импорта нет - вставим в начало после первых импортов
            m = re.search(r"^(?:from .+\n|import .+\n)+", t, flags=re.M)
            if m:
                t = t[:m.end()] + line + "\n" + t[m.end():]
            else:
                t = line + "\n" + t

# помощник: заменить тело функции create_access_token/create_refresh_token, если найдём сигнатуру
def replace_func(name, minutes_expr, days_expr):
    nonlocal_t = None

# create_access_token(...)
pat_access = r"(?ms)^def create_access_token\([^)]*\):\s*.*?(?=^def |^class |\Z)"
rep_access = """def create_access_token(payload: dict) -> str:
    data = payload.copy()
    ttl_minutes = int(getattr(settings, "access_token_expire_minutes", 15) or 15)
    if ttl_minutes <= 0:
        ttl_minutes = 15

    exp = int(time.time()) + ttl_minutes * 60
    data.update({"exp": exp})
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


"""

# create_refresh_token(...)
pat_refresh = r"(?ms)^def create_refresh_token\([^)]*\):\s*.*?(?=^def |^class |\Z)"
rep_refresh = """def create_refresh_token(payload: dict) -> str:
    data = payload.copy()
    ttl_days = int(getattr(settings, "refresh_token_expire_days", 30) or 30)
    if ttl_days <= 0:
        ttl_days = 30

    exp = int(time.time()) + ttl_days * 24 * 60 * 60
    data.update({"exp": exp})
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


"""

# применяем замены
if re.search(r"(?m)^def create_access_token\(", t):
    t, n1 = re.subn(pat_access, rep_access, t, count=1)
else:
    n1 = 0

if re.search(r"(?m)^def create_refresh_token\(", t):
    t, n2 = re.subn(pat_refresh, rep_refresh, t, count=1)
else:
    n2 = 0

if n1 == 0:
    raise SystemExit("ERROR: create_access_token() not found to patch")
if n2 == 0:
    raise SystemExit("ERROR: create_refresh_token() not found to patch")

p.write_text(t, encoding="utf-8")
print("OK: patched create_access_token/create_refresh_token (exp as unix timestamp)")
