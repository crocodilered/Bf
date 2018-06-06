import cherrypy
import bcrypt
import uuid
from webapp.libs.models.user import User


__all__ = ["AuthTool"]


class AuthTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, "before_handler", self._auth)

    def _auth(self):
        if not AuthTool.match_session():
            raise cherrypy.HTTPError(401, "Unauthorized")

    @staticmethod
    def start_session(email, password):
        r = None
        user = AuthTool.find_enabled_user(credentials=(email, password))
        if user:
            token = AuthTool.generate_token()
            cherrypy.session["token"] = user.token = token
            r = user
        return r

    @staticmethod
    def match_session():
        return AuthTool.find_enabled_user(token=AuthTool.get_token())

    @staticmethod
    def drop_session():
        user = AuthTool.find_enabled_user(token=AuthTool.get_token())
        if user:
            user.token = None
        cherrypy.session["token"] = None

    @staticmethod
    def encode_password(password):
        password = str.encode(password, encoding="UTF-8")
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        return password_hash.decode("utf-8")

    @staticmethod
    def match_password(attempt, password):
        attempt = str.encode(attempt, encoding="UTF-8")
        password = str.encode(password, encoding="UTF-8")
        return bcrypt.checkpw(attempt, password)

    @staticmethod
    def find_enabled_user(credentials=None, token=None):
        r = None
        if isinstance(credentials, tuple) and len(credentials) == 2:
            email, password = credentials
            user = User.get_by_email(cherrypy.request.sa, email)
            if user and user.enabled and AuthTool.match_password(password, user.password):
                r = user

        if isinstance(token, str):
            user = User.get_by_token(cherrypy.request.sa, token)
            if user and user.enabled:
                r = user

        return r

    @staticmethod
    def get_token():
        return cherrypy.session.get("token", None)

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())
