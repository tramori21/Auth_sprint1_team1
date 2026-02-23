from fastapi import FastAPI

from api.router import router

app = FastAPI(title='auth_service')
app.include_router(router)


@app.get('/health')
async def health():
    return {'status': 'ok'}
