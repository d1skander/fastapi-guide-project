from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend

from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse

from core.config import AdminConfig, CookieConfig, JWTConfig

from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

#тест
class AdminAuth(AuthenticationBackend):
    from datetime import datetime, timezone, timedelta

    import jwt

    admin_config = AdminConfig()
    cookie_config = CookieConfig()
    jwt_config = JWTConfig()

    async def login(self, request: Request) -> RedirectResponse | bool | HTMLResponse:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == self.admin_config.username and password == self.admin_config.password:
            token = self.jwt.encode({"exp": self.datetime.now(tz=self.timezone.utc) + self.timedelta(minutes=30)}, 
                                    self.cookie_config.admin_secret_key.get_secret_value(),
                                    algorithm=self.jwt_config.algorithm)
            request.session.update({"token": token})
            return True
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Incorrect username and password"}, status_code=401)
        #raise ValueError("incorrect username and password")


    async def logout(self, request: Request) -> RedirectResponse | bool:
        request.session.clear()

        return True


    async def authenticate(self, request: Request) -> RedirectResponse | bool | HTMLResponse:
        token = request.session.get("token")
        print(token)

        if not token:
            return False

        try:
            self.jwt.decode((token), 
                            self.cookie_config.admin_secret_key.get_secret_value(),
                            algorithms=[self.jwt_config.algorithm])
            return True
        except self.jwt.ExpiredSignatureError:
            return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "The session has ended"}, status_code=403)