from fastapi.security import HTTPBearer 
from fastapi import Request , HTTPException , status
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error= auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        crede = await super().__call__(request)


        token = crede.credentials
        token_data = decode_access_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token not refresh token"
            )

        return token_data


    def token_valid(self,token):
        token_data = decode_access_token(token)
        return True if token_data else False