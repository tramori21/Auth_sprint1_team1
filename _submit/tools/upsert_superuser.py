import argparse
import asyncio
from sqlalchemy import select

from core.security import hash_password
from db.postgres import async_session
from models.user import User

async def run(login: str, password: str) -> None:
async with async_session() as s:
res = await s.execute(select(User).where(User.login == login))
u = res.scalar_one_or_none()
if not u:
u = User(login=login, password=hash_password(password), is_superuser=True, is_active=True)
s.add(u)
else:
u.is_superuser = True
u.is_active = True
u.password = hash_password(password)
s.add(u)
await s.commit()

def main():
p = argparse.ArgumentParser()
p.add_argument("--login", required=True)
p.add_argument("--password", required=True)
a = p.parse_args()
asyncio.run(run(a.login, a.password))
print("ok")

if name == "main":
main()
