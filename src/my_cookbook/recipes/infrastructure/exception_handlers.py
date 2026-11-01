from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.infrastructure.error_response import ErrorResponse
from my_cookbook.recipes.infrastructure.recipe_error_code import RecipeErrorCode

ERROR_CODE_BY_DOMAIN_EXCEPTION: dict[type[Exception], RecipeErrorCode] = {
    InvalidRecipeName: RecipeErrorCode.INVALID_RECIPE_NAME,
}


def bad_request(code: RecipeErrorCode, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(code=code, detail=detail).model_dump(mode="json"),
    )


def answer_domain_exception(request: Request, exception: Exception) -> JSONResponse:
    return bad_request(ERROR_CODE_BY_DOMAIN_EXCEPTION[type(exception)], str(exception))


def answer_invalid_request(request: Request, exception: Exception) -> JSONResponse:
    assert isinstance(exception, RequestValidationError)
    detail = "; ".join(
        f"{'.'.join(str(step) for step in error['loc'])}: {error['msg']}"
        for error in exception.errors()
    )
    return bad_request(RecipeErrorCode.INVALID_REQUEST, detail)


def register_exception_handlers(app: FastAPI) -> None:
    for domain_exception in ERROR_CODE_BY_DOMAIN_EXCEPTION:
        app.add_exception_handler(domain_exception, answer_domain_exception)
    app.add_exception_handler(RequestValidationError, answer_invalid_request)
