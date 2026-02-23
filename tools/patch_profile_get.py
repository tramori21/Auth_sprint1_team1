from __future__ import annotations

from pathlib import Path
import re

path = Path("src/api/v1/auth.py")
text = path.read_text(encoding="utf-8")

# Если уже есть GET /profile — ничего не делаем
if re.search(r"@router\.get\(\s*['\"]/profile['\"]\s*\)", text):
    print("SKIP: GET /profile already exists")
    raise SystemExit(0)

# Пытаемся вставить GET /profile перед существующим PATCH /profile
m = re.search(r"^@router\.patch\(\s*['\"]/profile['\"]\s*\)\s*$", text, flags=re.M)
if not m:
    print("ERROR: cannot find @router.patch('/profile') in src/api/v1/auth.py")
    raise SystemExit(2)

insert_pos = m.start()

snippet = """
@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    return current_user


"""

# Убедимся, что Depends уже импортирован; если нет — добавим в импорт из fastapi
if "Depends" not in text:
    text = re.sub(r"^from fastapi import (.+)$", lambda mm: mm.group(0) + ", Depends" if "Depends" not in mm.group(1) else mm.group(0), text, flags=re.M)

# Убедимся, что get_current_user импортирован/доступен в файле; если нет — добавим импорт
if "get_current_user" not in text:
    # типичный случай: from api.deps import ...
    if re.search(r"^from api\.deps import .+$", text, flags=re.M):
        text = re.sub(r"^from api\.deps import (.+)$", lambda mm: ("from api.deps import " + mm.group(1).rstrip() + ", get_current_user") if "get_current_user" not in mm.group(1) else mm.group(0), text, flags=re.M)
    else:
        # добавим отдельной строкой после импортов fastapi
        text = re.sub(r"^(from fastapi import .+\n)", r"\1from api.deps import get_current_user\n", text, flags=re.M)

# Вставка
text = text[:insert_pos] + snippet + text[insert_pos:]
path.write_text(text, encoding="utf-8")
print("OK: inserted GET /profile into src/api/v1/auth.py")
