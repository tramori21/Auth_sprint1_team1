from __future__ import annotations

from pathlib import Path
import re

path = Path("src/api/deps.py")
text = path.read_text(encoding="utf-8")

# Гарантируем нужные импорты (аккуратно добавляем, если их нет)
need_lines = [
    "from fastapi import Depends, HTTPException, Header, status",
    "from sqlalchemy import select",
    "from sqlalchemy.ext.asyncio import AsyncSession",
    "from db.postgres import get_session",
    "from models.user import User",
    "from core.security import decode_token",
]
for line in need_lines:
    if line not in text:
        # вставляем после первых импортов
        m = re.search(r"^(from .+\n|import .+\n)+", text, flags=re.M)
        if m:
            text = text[:m.end()] + line + "\n" + text[m.end():]
        else:
            text = line + "\n" + text

# Универсальная замена функции get_current_user целиком
pattern = r"(?ms)^async def get_current_user\([^\)]*\):\s*.*?(?=^\S|\Z)"
replacement = """async def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    session: AsyncSession = Depends(get_session),
):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    token = parts[1]

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = (await session.execute(select(User).where(User.id == sub))).scalar_one_or_none()
    if not user or not getattr(user, "is_active", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


"""

if re.search(r"^async def get_current_user\(", text, flags=re.M):
    text2, n = re.subn(pattern, replacement, text, count=1)
    if n == 0:
        # если регулярка не сработала — делаем более грубо: вырезаем от def до следующего def/class/router
        m = re.search(r"(?m)^async def get_current_user\([^\)]*\):\s*$", text)
        if not m:
            raise SystemExit("ERROR: get_current_user() signature not found")
        start = m.start()
        m2 = re.search(r"(?m)^(async def |def |class |router\s*=|@)", text[m.end():])
        end = m.end() + (m2.start() if m2 else len(text))
        text2 = text[:start] + replacement + text[end:]
    text = text2
else:
    # если функции вообще нет — добавим в конец файла
    text = text.rstrip() + "\n\n" + replacement

path.write_text(text, encoding="utf-8")
print("OK: patched get_current_user() in src/api/deps.py")
