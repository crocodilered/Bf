import cherrypy
from webapp.controllers.abstract_controller import AbstractController
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Graph as GraphModel


__all__ = ['Calculation']


class Calculation(AbstractController):

    @cherrypy.expose([""])
    @cherrypy.tools.render(template="calculation/index.html")
    @cherrypy.tools.auth()
    def index(self):
        """ Список алгоритмов """
        index = CalculationModel.list(cherrypy.request.sa)
        return self.wrap_template_params({
            "index": index
        })

    @cherrypy.expose(["c"])
    @cherrypy.tools.render(template="calculation/calculation.html")
    @cherrypy.tools.auth()
    def calculation(self, calculation_id):
        """ Список рассчетов выбранного алгоритма """
        calculation = CalculationModel.get(cherrypy.request.sa, calculation_id)
        return self.wrap_template_params({
            "calculation": calculation
        })

    @cherrypy.expose(["g"])
    @cherrypy.tools.render(template="calculation/graph.html")
    @cherrypy.tools.auth()
    def graph(self, graph_id):
        graph = GraphModel.get(cherrypy.request.sa, graph_id)
        calculation = CalculationModel.get(cherrypy.request.sa, graph.calculation_id)
        return self.wrap_template_params({
            "calculation": calculation,
            "graph": graph
        })

    @cherrypy.expose(['g_json'])
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def graph_json_data(self, graph_id):
        r = []
        graph = GraphModel.get(cherrypy.request.sa, graph_id)
        if graph:
            for point in graph.data:
                r.append([point.x, point.y])
        return r
