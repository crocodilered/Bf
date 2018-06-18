from PIL import Image
import base64
import cherrypy
import requests
import datetime
import json
from webapp.libs.graph_image_helper import GraphImageHelper
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Graph as GraphModel, \
    Data as DataModel


__all__ = ['Api']


class Api(object):

    ERR_OK = 0
    ERR_BAD_PARAMS = 1
    ERR_BAD_DATA = 32
    ERR_OBJ_NOT_FOUND = 2
    ERR_REMOTE_HOST_SCRIPT_ERROR = 4
    ERR_REMOTE_HOST_HTTP_ERROR = 8
    ERR_REMOTE_HOST_UNREACHABLE = 16

    @cherrypy.expose(['run-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def run_graph(self):
        """ RUN """
        calculation_id = cherrypy.request.json['calculation_id']
        title = cherrypy.request.json['title']
        params = cherrypy.request.json['params']

        # TODO: check params

        sess = cherrypy.request.sa

        # Кладем данные в БД
        graph = GraphModel(calculation_id, title, str(params).replace('"', '\''))
        sess.add(graph)
        sess.flush()

        # Запускаем процесс на стороне
        ce_config = cherrypy.tree.apps[''].config['CalculationsEngine']
        ce_url = 'http://%s:%s/' % (ce_config['ce.host'], ce_config['ce.port'])
        ce_params = {
            'cmd': 'start',
            'calculation_id': calculation_id,
            'graph_id': graph.id,
            'params': params
        }
        error = self.ERR_OK
        err_message = ''
        try:
            resp = requests.post(ce_url, json=ce_params)
            if resp.status_code == 200:
                rest_json = json.loads(resp.text)
                if 'error' in rest_json and rest_json['error'] != 0:
                    error = self.ERR_REMOTE_HOST_SCRIPT_ERROR
                    err_message = 'Got error code (%s) from engine side.' % rest_json['error']
            else:
                error = self.ERR_REMOTE_HOST_HTTP_ERROR
                err_message = 'Got HTTP error %s' % resp.status_code
                sess.delete(graph)
        except requests.exceptions.ConnectionError:
            error = self.ERR_REMOTE_HOST_UNREACHABLE
            err_message = 'Cant connect to %s' % ce_url
            sess.delete(graph)

        return {'error': error, 'message': err_message}

    @cherrypy.expose(['stop-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def stop_graph(self):
        """ STOP """
        return {'error': 0}

    @cherrypy.expose(['delete-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def delete_graph(self):
        """ Delete graph and all it's data. """
        error = self.ERR_OK
        if 'graph_id' in cherrypy.request.json:
            sess = cherrypy.request.sa
            graph_id = cherrypy.request.json['graph_id']
            graph = GraphModel.get(sess, graph_id)
            if graph:
                sess.delete(graph)
                sess.commit()
                GraphImageHelper.clear_graph_path(graph_id)
            else:
                error = self.ERR_OBJ_NOT_FOUND
        else:
            error = self.ERR_BAD_PARAMS
        return {'error': error}

    @cherrypy.expose(['create-calculation'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def create_calculation(self):
        error = self.ERR_OK
        if 'title' in cherrypy.request.json and \
                'description' in cherrypy.request.json and \
                'params_template' in cherrypy.request.json:
            title = cherrypy.request.json['title']
            description = cherrypy.request.json['description']
            params_template = cherrypy.request.json['params_template']
            sess = cherrypy.request.sa
            calculation = CalculationModel(title, description, params_template)
            sess.add(calculation)
            sess.flush()
        else:
            error = self.ERR_BAD_PARAMS

        return {'error': error}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def graph_images_list(self, graph_id, last_one=False):
        """ Вернуть список ИЗОБРАЖЕНИЙ рассчета """
        r = []
        sess = cherrypy.request.sa
        graph = GraphModel.get(sess, graph_id)
        if graph:
            if last_one:
                item = graph.last_image(sess)
                if item:
                    r.append({
                        'src': item.href(),
                        'w': item.image_width,
                        'h': item.image_height
                    })
            else:
                for item in graph.data:
                    r.append({
                        'src': item.href(),
                        'w': item.image_width,
                        'h': item.image_height
                    })
        return r

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

    # **********************************************************************************************************
    #
    # Non secured methods coz of Engine doesnt support cookies
    # and we cannot init session to store user token there
    #

    # TODO: SOLVE THIS SOMEHOW!!!

    @cherrypy.expose(['update-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_graph(self):
        """
        Append data to graph. Data can be point(x, y), image(mode, width, height, bytes)
        :return: Json with error code
        """
        error = self.ERR_OK
        data = None
        params = cherrypy.request.json
        if 'graph_id' in params:
            sess = cherrypy.request.sa
            graph = GraphModel.get(sess, params['graph_id'])
            if graph:

                if 'image' in params and \
                        'mode' in params['image'] and \
                        'width' in params['image'] and \
                        'height' in params['image'] and \
                        'data' in params['image']:
                    # Image
                    image = Image.frombytes(params['image']['mode'],
                                            (params['image']['width'], params['image']['height']),
                                            base64.b64decode(params['image']['data'].encode('utf-8')))
                    image = image.resize((730, 730), Image.BICUBIC)
                    data = DataModel(graph.id,
                                     image_width=image.width,
                                     image_height=image.height)

                elif 'point' in params and \
                        'x' in params['point'] and \
                        'y' in params['point']:
                    # Point
                    data = DataModel(graph.id,
                                     point_x=params['point']['x'],
                                     point_y=params['point']['y'])

                else:
                    # В параметрах передали какую-то муть
                    error = self.ERR_BAD_DATA

                # Finalize
                if data is not None:
                    sess.add(data)
                    sess.flush()
                    # Update Graph and  Calculation
                    calc = CalculationModel.get(sess, graph.calculation_id)
                    calc.updated = graph.updated = datetime.datetime.now()
                    # save image if necessary
                    if 'image' in locals():
                        image_file_path = GraphImageHelper.get_image_path(data)
                        if image_file_path:
                            GraphImageHelper.prepare_graph_path(data.graph_id)
                            image.save(image_file_path, 'PNG')
                            # publish event to let plugin know when to generate video
                            cherrypy.engine.publish('update-graph-image', data.graph_id)
            else:
                error = self.ERR_OBJ_NOT_FOUND
        else:
            error = self.ERR_BAD_PARAMS

        return {'error': error}

    @cherrypy.expose(['finish-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def finish_graph(self):
        """
        Sets graph.finished flag to True value.
        :return: Json with error code
        """
        error = self.ERR_OK
        if 'graph_id' in cherrypy.request.json:
            graph_id = cherrypy.request.json['graph_id']
            graph = GraphModel.get(cherrypy.request.sa, graph_id)
            if graph:
                graph.updated = datetime.datetime.now()
                graph.finished = True
                cherrypy.engine.publish('finish-graph', graph.id)
            else:
                error = self.ERR_OBJ_NOT_FOUND
        else:
            error = self.ERR_BAD_PARAMS
        return {'error': error}
