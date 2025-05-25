from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.core.database import engine
from app.database.base_class import Base
from app.routes.api import router


def init_db():
    Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(router)


# Global exception handler for RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}

    for error in exc.errors():
        loc = error["loc"]
        field = loc[1] if len(loc) > 1 and loc[0] == "body" else loc[-1]

        if field not in errors:
            errors[field] = []

        msg = error["msg"]

        # Custom message for required fields
        if error["type"] == "value_error":
            if isinstance(error["ctx"].get("error"), tuple) and len(error["ctx"]["error"]) >= 2:
                _, custom_errors = error["ctx"]["error"]
                for f, m in custom_errors.items():
                    errors[f] = m
            else:
                msg = "The field is required."

        errors[field].append(msg)

    return JSONResponse(
        status_code=422,
        content={
            "message": "The given data was invalid",
            "errors": errors
        }
    )


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = {}
#
#     for error in exc.errors():
#         field = ".".join(str(loc) for loc in error["loc"][1:])  # skip 'body'
#         if field not in errors:
#             errors[field] = []
#         errors[field].append(error["msg"])
#
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "message": "The given data was invalid",
#             "errors": errors
#         }
#     )


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgresSQL"}
