import cherrypy
import PIL
import os
from webapp.libs.graph_image_helper import GraphImageHelper
from cherrypy.lib.static import serve_file
from PIL import Image
from webapp.controllers.abstract_controller import AbstractController
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Graph as GraphModel, \
    Data as DataModel


__all__ = ['Calculation']


class Calculation(AbstractController):

    @cherrypy.expose
    @cherrypy.tools.render(template="calculation/index.html")
    @cherrypy.tools.auth()
    def index(self):
        """ Список алгоритмов """
        return self.wrap_template_params({
            "index": CalculationModel.list(cherrypy.request.sa)
        })

    @cherrypy.expose
    @cherrypy.tools.render(template="calculation/item_points.html")
    @cherrypy.tools.auth()
    def item_points(self, calculation_id):
        """ Список рассчетов выбранного алгоритма. Результат -- графики. """
        return self.wrap_template_params({
            "calculation": CalculationModel.get(cherrypy.request.sa, calculation_id)
        })

    @cherrypy.expose
    @cherrypy.tools.render(template="calculation/item_images.html")
    @cherrypy.tools.auth()
    def item_images(self, calculation_id):
        """ Список рассчетов выбранного алгоритма. Результат -- мультики. """
        return self.wrap_template_params({
            "calculation": CalculationModel.get(cherrypy.request.sa, calculation_id)
        })

    @cherrypy.expose
    @cherrypy.tools.render(template="calculation/graph.html")
    @cherrypy.tools.auth()
    def graph(self, graph_id):
        graph = GraphModel.get(cherrypy.request.sa, graph_id)
        calculation = CalculationModel.get(cherrypy.request.sa, graph.calculation_id)
        return self.wrap_template_params({
            "calculation": calculation,
            "graph": graph
        })

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def graph_points_list(self, graph_id):
        """ Вернуть список ТОЧЕК рассчета """
        r = []
        graph = GraphModel.get(cherrypy.request.sa, graph_id)
        if graph:
            for item in graph.data:
                r.append([item.point_x, item.point_y])
        return r

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def graph_images_list(self, graph_id):
        """ Вернуть список ИЗОБРАЖЕНИЙ рассчета """
        r = []
        graph = GraphModel.get(cherrypy.request.sa, graph_id)
        if graph:
            for item in graph.data:
                r.append({
                    'src': item.href(),
                    'w': item.image_width,
                    'h': item.image_height
                })
        return r

    @cherrypy.expose
    @cherrypy.tools.auth()
    def graph_image(self, data_id):
        """ Вернуть одно изображение ('image/png') """
        data = DataModel.get(cherrypy.request.sa, data_id)
        image_file = GraphImageHelper.path(data)
        if image_file:
            if not os.path.isfile(image_file):
                cherrypy.log(image_file)
                img = PIL.Image.frombytes(data.image_mode, (data.image_width, data.image_height), data.image_data)
                img.save(image_file, 'PNG')
            return serve_file(image_file, 'image/png')
        else:
            raise cherrypy.HTTPError(404)
