import cherrypy
import requests
import datetime
import json
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Graph as GraphModel, \
    Data as DataModel


__all__ = ['Api']


class Api(object):

    ERR_OK = 0
    ERR_BAD_PARAMS = 1
    ERR_DATA_NOT_FOUND = 2
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

    @cherrypy.expose(['delete-graph'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def delete_graph(self):
        error = self.ERR_OK
        if 'graph_id' in cherrypy.request.json:
            sess = cherrypy.request.sa
            graph_id = cherrypy.request.json['graph_id']
            graph = GraphModel.get(sess, graph_id)
            if graph:
                sess.delete(graph)
                sess.commit()
            else:
                error = self.ERR_DATA_NOT_FOUND
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
        Append point to graph data.
        :return: Json with error code
        """
        error = self.ERR_OK
        if 'graph_id' in cherrypy.request.json and \
                'x' in cherrypy.request.json and \
                'y' in cherrypy.request.json:

            graph_id = cherrypy.request.json['graph_id']
            sess = cherrypy.request.sa

            # Test if there is graph with given id
            graph = GraphModel.get(sess, graph_id)
            if graph:
                # Append data
                x = cherrypy.request.json['x']
                y = cherrypy.request.json['y']
                data = DataModel(graph_id, x, y)
                sess.add(data)
                sess.flush()
                # Update Graph and  Calculation
                calc = CalculationModel.get(sess, graph.calculation_id)
                calc.updated = graph.updated = datetime.datetime.now()
            else:
                error = self.ERR_DATA_NOT_FOUND
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
            else:
                error = self.ERR_DATA_NOT_FOUND
        else:
            error = self.ERR_BAD_PARAMS
        return {'error': error}
