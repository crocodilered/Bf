import cherrypy
from webapp.controllers.abstract_controller import AbstractController


__all__ = ['App']


class App(AbstractController):

    @cherrypy.expose
    @cherrypy.tools.render(template='app/index.html')
    def index(self, **params):
        """
        Точка входа.
        Необходимо запросить логин/пароль и проверить их
        """
        url_to_redirect = "/calculation/"

        # Если пользователь уже залогинен, направляем его в список графиков
        if self.get_logged_in_user():
            raise cherrypy.HTTPRedirect("/calculation/")

        error_code = 0
        if cherrypy.request.method == "POST":
            email = params["email"] if "email" in params else None
            password = params["password"] if "password" in params else None
            return_url = params["return_url"] if "return_url" in params else None
            if email and password:
                # TODO: отсюда вываливается куча значений error_code, как-то не прозрачно. Нужно сделать прозрачно.
                user = cherrypy.tools.auth.start_session(email, password)
                if user:
                    raise cherrypy.HTTPRedirect(return_url or url_to_redirect)
                else:
                    # Логин/пароль не подошли
                    error_code = 2
            else:
                # Логин/пароль не ввели
                error_code = 1
        return self.wrap_template_params({
            "error_code": error_code
        })
