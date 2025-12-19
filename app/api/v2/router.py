from fastapi import APIRouter


from app.api.v2.webudget.users import user_router

budgetRouter= APIRouter()


budgetRouter.include_router(user_router, prefix="/users", tags=["we-budget-users"])
budgetRouter.include_router(user_router, prefix="/email", tags=["we-budget-email-verification"])
