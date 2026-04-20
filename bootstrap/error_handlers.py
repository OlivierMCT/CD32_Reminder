from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions.reminder_error import ReminderError


async def reminder_error_handler(request: Request, error: Exception) -> JSONResponse:
    if not isinstance(error, ReminderError):
        return JSONResponse(status_code=500, content=str(error))

    status_code = 400
    if error.code == 666:
        status_code = 404
    elif error.code == 999:
        status_code = 403
    elif error.code == 222:
        status_code = 400
    return JSONResponse(status_code=status_code, content=error.message)


