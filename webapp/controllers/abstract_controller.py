import cherrypy
from webapp.libs.models.user import User


__all__ = ["AbstractController"]


class AbstractController:
    def __init__(self):
        self._logged_user_account = None

    def get_logged_in_user(self):
        """
        Get logged in user account
        :return: user account (User object)
        """
        token = cherrypy.tools.auth.get_token()
        self._logged_user_account = User.get_by_token(cherrypy.request.sa, token) if token else None
        return self._logged_user_account

    def wrap_template_params(self, params=None):
        """
        Append general parameters
        :param params: Input parameters
        :return: Full set (result) of parameters
        """
        account = self.get_logged_in_user()
        appendix = {"account": account} if account else {}
        # merge data
        return {**params, **appendix} if params and isinstance(params, dict) else appendix
