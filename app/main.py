from fastapi import Request
from fastapi.responses import HTMLResponse
from app import app,templates

# Routers
from app.auth import router as auth_router
from app.bot import router as bot_router

#Auth Routers 
app.include_router(auth_router)
#bot Routers
app.include_router(bot_router)


@app.get('/',response_class=HTMLResponse)
async def root(request:Request):
    """Main Page
    """
    return templates.TemplateResponse("index.html", {"request": request})
