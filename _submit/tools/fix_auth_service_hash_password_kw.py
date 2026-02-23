from pathlib import Path
import re

p = Path("src/services/auth_service.py")
t = p.read_text(encoding="utf-8")

# Убираем неверный kwargs из hash_password(...)
t2 = re.sub(r"hash_password\(\s*password\s*,\s*is_active\s*=\s*True\s*\)", "hash_password(password)", t)

# Гарантируем, что у User(...) есть is_active=True (в register)
# Ищем создание пользователя: User(login=..., password=...)
def repl_user(m):
    inside = m.group(1)
    if "is_active" in inside:
        return "User(" + inside + ")"
    return "User(" + inside.rstrip() + ", is_active=True)"

t3, n = re.subn(r"User\(\s*([^)]*login\s*=\s*login[^)]*password\s*=\s*hash_password\(\s*password\s*\)[^)]*)\)", repl_user, t2, count=1)

# Если конкретный паттерн не нашёлся — второй шанс: любой User(login=login, password=hash_password(password)) в файле
if n == 0:
    t3 = re.sub(r"User\(\s*login\s*=\s*login\s*,\s*password\s*=\s*hash_password\(\s*password\s*\)\s*\)",
                "User(login=login, password=hash_password(password), is_active=True)", t2, count=1)

p.write_text(t3, encoding="utf-8")
print("OK: fixed hash_password(...is_active=True) and ensured User(..., is_active=True)")
