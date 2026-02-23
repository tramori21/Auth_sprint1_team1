from pathlib import Path
import re

p = Path("src/models/user.py")
t = p.read_text(encoding="utf-8")

t2 = t
# default=False -> default=True
t2 = re.sub(r"(is_active\s*=\s*Column\([^\)]*default\s*=\s*)False", r"\g<1>True", t2)
# server_default='false' -> 'true'
t2 = re.sub(r"(is_active\s*=\s*Column\([^\)]*server_default\s*=\s*)['\"]false['\"]", r"\g<1>'true'", t2, flags=re.I)

if t2 == t:
    print("SKIP: user.py not changed (no is_active default/server_default found)")
else:
    p.write_text(t2, encoding="utf-8")
    print("OK: user.py patched (is_active default -> True)")
