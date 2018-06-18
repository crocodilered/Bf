import cherrypy
from webapp.libs.graph_image_helper import GraphImageHelper
from cherrypy.lib.static import serve_file
from webapp.controllers.abstract_controller import AbstractController
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Data as DataModel


__all__ = ['Calculation']


class Calculation(AbstractController):

    @cherrypy.expose
    @cherrypy.tools.render(template='calculation/index.html')
    @cherrypy.tools.auth()
    def index(self):
        """ Список алгоритмов """
        return self.wrap_template_params({
            'index': CalculationModel.list(cherrypy.request.sa)
        })

    @cherrypy.expose
    @cherrypy.tools.render(template='calculation/item_points.html')
    @cherrypy.tools.auth()
    def item_points(self, calculation_id):
        """ Список рассчетов выбранного алгоритма. Результат -- графики. """
        return self.wrap_template_params({
            'calculation': CalculationModel.get(cherrypy.request.sa, calculation_id)
        })

    @cherrypy.expose
    @cherrypy.tools.render(template='calculation/item_images.html')
    @cherrypy.tools.auth()
    def item_images(self, calculation_id):
        """ Список рассчетов выбранного алгоритма. Результат -- мультики. """
        calculation = CalculationModel.get(cherrypy.request.sa, calculation_id)
        graph_movies = {}
        for graph in calculation.graphs:
            graph_movies[graph.id] = GraphImageHelper.get_movie_href(graph.id)
        return self.wrap_template_params({
            'calculation': calculation,
            'graph_movies': graph_movies
        })

    @cherrypy.expose
    @cherrypy.tools.auth()
    def graph_image(self, data_id):
        """ Вернуть одно изображение ('image/png') """
        data = DataModel.get(cherrypy.request.sa, data_id)
        image_file = GraphImageHelper.get_image_path(data)
        if image_file:
            return serve_file(image_file, 'image/png')
        else:
            raise cherrypy.HTTPError(404)

