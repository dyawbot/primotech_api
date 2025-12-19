from fastapi.templating import Jinja2Templates
from app.api.v2.webudget.users import user_router
from fastapi import APIRouter, Depends, HTTPException, Request,status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_webudget_db
from app.repository.webudget.helpers import verify_token
from app.repository.webudget.user_repo import activate_email as activate

templates = Jinja2Templates(directory="app/templates")


@user_router.get("/me")
async def verification_webudget(id:str, request: Request, db: AsyncSession = Depends(get_webudget_db)):

    verified_email= verify_token(id)
    
    if not isinstance(verified_email, str):
                print(type(verified_email))
                return verified_email
    _result = await activate(db=db,email=verified_email)

    if _result.code != 200:
        raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return templates.TemplateResponse("email_verified.html", {
        "request": request,
        "message": _result.message
    })