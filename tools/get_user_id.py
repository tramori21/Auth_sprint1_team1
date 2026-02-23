import argparse
import asyncio
from sqlalchemy import select

from db.postgres import async_session
from models.user import User

async def run(login: str) -> None:
async with async_session() as s:
res = await s.execute(select(User).where(User.login == login))
u = res.scalar_one_or_none()
print(str(u.id) if u else "")

def main():
p = argparse.ArgumentParser()
p.add_argument("--login", required=True)
a = p.parse_args()
asyncio.run(run(a.login))

if name == "main":
main()
