from pathlib import Path
import re

p = Path("src/services/auth_service.py")
t = p.read_text(encoding="utf-8")

# Ищем создание User(...) внутри register()
# добавляем ", is_active=True" если нет "is_active="
def add_is_active(m):
    inside = m.group(1)
    if "is_active" in inside:
        return "User(" + inside + ")"
    # аккуратно добавляем в конец аргументов
    inside2 = inside.rstrip()
    if inside2.endswith(","):
        inside2 = inside2 + " is_active=True"
    else:
        inside2 = inside2 + ", is_active=True"
    return "User(" + inside2 + ")"

t2, n = re.subn(r"User\(([^)]*)\)", add_is_active, t, count=1)
if n == 0:
    print("SKIP: auth_service.py not changed (User(...) not found)")
else:
    p.write_text(t2, encoding="utf-8")
    print("OK: auth_service.py patched (User(..., is_active=True))")
