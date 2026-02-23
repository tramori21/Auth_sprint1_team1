from pathlib import Path
import re

p = Path("src/models/user.py")
t = p.read_text(encoding="utf-8")

t2 = t

# Частые варианты: default=False / server_default=false / nullable
t2 = re.sub(r"(is_active\s*=\s*Column\([^\)]*default\s*=\s*)False", r"\g<1>True", t2)
t2 = re.sub(r"(is_active\s*=\s*Column\([^\)]*server_default\s*=\s*)['\"]false['\"]", r"\g<1>'true'", t2, flags=re.I)

if t2 == t:
    print("SKIP: user.py not changed (no default=False/server_default=false found)")
else:
    p.write_text(t2, encoding="utf-8")
    print("OK: user.py updated (is_active default -> True)")
