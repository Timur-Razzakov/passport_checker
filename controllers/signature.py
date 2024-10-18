import hashlib
import hmac

from fastapi import HTTPException

from schemas.checker_passport.passports import ErrorResponse


class Signature:
    def __init__(self, request, secret_key):
        self.request = request
        self.secret_key = secret_key

    def generate_signature(self, request_body: dict) -> str:
        sorted_keys = sorted(request_body.keys())
        concatenated_values = ".".join(str(request_body[key]) for key in sorted_keys)
        concatenated_values += self.secret_key
        signature = hmac.new(
            key=self.secret_key.encode(),
            msg=concatenated_values.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return signature

    def add_signature_to_headers(self, request_body: dict, headers: dict) -> dict:
        signature = self.generate_signature(request_body)
        headers['X-Request-Sign'] = signature
        return headers

    async def get_request_body(self):
        try:
            return await self.request.json()
        except Exception as e:
            raise Exception("Failed to parse request body") from e

    async def verify_request_signature(self):
        x_request_sign = self.request.headers.get("X-Request-Sign")
        if not x_request_sign:
            raise HTTPException(status_code=400, detail=ErrorResponse(
                result=False,
                error='Service error: Missing X-Request-Sign',
                code=400
            ).model_dump())
        request_body = await self.get_request_body()
        generated_signature = self.generate_signature(request_body)

        if x_request_sign != generated_signature:
            raise HTTPException(status_code=400, detail=ErrorResponse(
                result=False,
                error='Service error: Invalid X-Request-Sign',
                code=400
            ).model_dump())
        return x_request_sign
