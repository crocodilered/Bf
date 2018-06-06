import cherrypy


__all__ = ["SaTool"]


class SaTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, "on_start_resource", self.bind_session, priority=20)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach("on_end_resource", self.commit_transaction, priority=80)

    def bind_session(self):
        cherrypy.request.sa = cherrypy.engine.publish("bind-session").pop()
 
    def commit_transaction(self):
        if not hasattr(cherrypy.request, "sa"):
            return
        cherrypy.request.sa = None
        cherrypy.engine.publish("commit-session")
