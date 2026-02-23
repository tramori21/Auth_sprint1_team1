from pathlib import Path
import re

p = Path("src/api/deps.py")
t = p.read_text(encoding="utf-8")

# Нужные импорты (добавляем, если нет)
imports = [
    "import uuid",
    "from fastapi import Depends, HTTPException, status",
    "from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer",
    "from sqlalchemy import select",
    "from sqlalchemy.ext.asyncio import AsyncSession",
    "from db.postgres import get_session",
    "from core.security import decode_token",
    "from models.user import User",
]
for line in imports:
    if line not in t:
        # вставляем после блока импортов
        m = re.search(r"^(?:from .+\n|import .+\n)+", t, flags=re.M)
        if m:
            t = t[:m.end()] + line + "\n" + t[m.end():]
        else:
            t = line + "\n" + t

# Гарантируем bearer-схему
if "bearer_scheme = HTTPBearer()" not in t:
    t = t.rstrip() + "\n\nbearer_scheme = HTTPBearer()\n"

# Заменяем get_current_user целиком (если есть), иначе добавляем
replacement = """
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        user_id = uuid.UUID(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # is_active должен пропускать активных, а если поля нет — не валимся
    if hasattr(user, "is_active") and not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive")

    return user


"""

pat = r"(?ms)^async def get_current_user\([^\)]*\):\s*.*?(?=^\S|\Z)"
if re.search(r"(?m)^async def get_current_user\(", t):
    t, n = re.subn(pat, replacement, t, count=1)
    if n == 0:
        raise SystemExit("ERROR: found get_current_user but failed to replace")
else:
    t = t.rstrip() + "\n\n" + replacement

p.write_text(t, encoding="utf-8")
print("OK: deps.py patched (get_current_user v2)")
