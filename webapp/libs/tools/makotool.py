import cherrypy
from mako import exceptions


__all__ = ['MakoTool']


class MakoTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_finalize', self._render, priority=10)

    def _render(self, template=None):
        """
        Applied once your page handler has been called. It looks up the template from the various template directories
        defined in the mako plugin then renders it with whatever dictionary the page handler returned.
        """

        # retrieve the data returned by the handler
        data = cherrypy.response.body or {}

        if template:
            template = cherrypy.engine.publish("lookup-template", template).pop()
            if template and isinstance(data, dict):
                try:
                    cherrypy.response.body = template.render(**data)
                except:
                    cherrypy.response.body = exceptions.html_error_template().render()
