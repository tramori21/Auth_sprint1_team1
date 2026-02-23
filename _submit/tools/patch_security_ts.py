from pathlib import Path
import re

p = Path("src/core/security.py")
t = p.read_text(encoding="utf-8")

# 2.1) В импорт "from datetime import ..." добавляем timezone, если его нет
t2 = t
m = re.search(r"(?m)^from datetime import ([^\n]+)$", t2)
if m and "timezone" not in m.group(1):
    t2 = re.sub(r"(?m)^from datetime import ([^\n]+)$", lambda mm: "from datetime import " + mm.group(1).rstrip() + ", timezone", t2, count=1)

# 2.2) Меняем _ts(dt) так, чтобы naive datetime трактовался как UTC
# Было: def _ts(dt: datetime) -> int: return int(dt.timestamp())
# Станет: return int(dt.replace(tzinfo=timezone.utc).timestamp())
pat = r"(?ms)^def _ts\(\s*dt\s*:\s*datetime\s*\)\s*->\s*int\s*:\s*\n\s*return\s+int\(\s*dt\.timestamp\(\)\s*\)\s*\n"
rep = "def _ts(dt: datetime) -> int:\n    return int(dt.replace(tzinfo=timezone.utc).timestamp())\n"
t3, n = re.subn(pat, rep, t2, count=1)

if n == 0:
    # fallback: если формат чуть другой — заменяем строку return int(dt.timestamp())
    t3, n2 = re.subn(r"(?m)^\s*return\s+int\(\s*dt\.timestamp\(\)\s*\)\s*$",
                     "    return int(dt.replace(tzinfo=timezone.utc).timestamp())",
                     t2, count=1)
    if n2 == 0:
        raise SystemExit("ERROR: cannot patch _ts(dt) in src/core/security.py")

p.write_text(t3, encoding="utf-8")
print("OK: patched _ts(dt) to use UTC-aware timestamp")
