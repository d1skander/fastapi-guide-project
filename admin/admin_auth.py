from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend

from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

#тест
class AdminAuth(AuthenticationBackend):
    from datetime import datetime, timezone

    import jwt

    async def login(self, request: Request) -> RedirectResponse | bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == "admin" and password == "password":
            token = self.jwt.encode({"exp": self.datetime.now(tz=self.timezone.utc)}, 
                                    "secret",
                                    algorithm="HS256")
            request.session.update({"token": token})
            return True
        
        raise ValueError("incorrect username and password")


    async def logout(self, request: Request) -> RedirectResponse | bool:
        request.session.clear()

        return True


    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            self.jwt.decode(token, 
                            "secret",
                            algorithm=["HS256"])
            return True
        except self.jwt.ExpiredSignatureError:
            raise ValueError("The session has ended")