from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import auth, user, post, role

async def rank_out_of_bound_handler(request: Request, exc: RequestValidationError):

    validation_errors = exc.errors()
    for err in validation_errors:
        # You could check for other things here as well, e.g. the error type.
        if "rank" in err["loc"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Rank must be in range [0, 1000000]."}
            )

    # Default response in every other case.
    return await request_validation_exception_handler(request, exc)


app = FastAPI(
  title="FastAPI & Mongo CRUD",
  description="Post API with User Authentication",
  version="1.0.0",
  exception_handlers={RequestValidationError: rank_out_of_bound_handler},
)

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(role.router, tags=['Roles'], prefix='/api/roles')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


