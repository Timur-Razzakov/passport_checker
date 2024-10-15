from typing import Union, List, Dict

from pydantic import BaseModel


class ControllerResult(BaseModel):
    result: bool = True
    data: Union[List, Dict, None] = None
    message: str = "Ok"
    error_key: str = None
    error_code: int = 0
