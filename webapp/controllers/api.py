import cherrypy
import requests
import datetime
import json
from webapp.libs.models.calculation import \
    Calculation as CalculationModel, \
    Graph as GraphModel, \
    Data as DataModel


__all__ = ["Api"]


class Api(object):

    @cherrypy.expose(["run-graph"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def run_graph(self):
        """ RUN """
        calculation_id = cherrypy.request.json["calculation_id"]
        title = cherrypy.request.json["title"]
        params = cherrypy.request.json["params"]

        # TODO: check params

        sess = cherrypy.request.sa

        # Кладем данные в БД
        graph = GraphModel(calculation_id, title, str(params).replace("'", "\""))
        sess.add(graph)
        sess.flush()

        # Запускаем процесс на стороне
        ce_config = cherrypy.tree.apps[""].config["CalculationsEngine"]
        ce_url = "http://%s:%s/" % (ce_config["ce.host"], ce_config["ce.port"])
        ce_params = {
            "cmd": "start",
            "calculation_id": calculation_id,
            "graph_id": graph.id,
            "params": params
        }
        err_code = 0
        err_message = ""
        try:
            resp = requests.post(ce_url, json=ce_params)
            if resp.status_code == 200:
                rest_json = json.loads(resp.text)
                if "error" in rest_json and rest_json["error"] != 0:
                    err_code = 3
                    err_message = "Got error code (%s) from engine side." % rest_json["error"]
            else:
                # HTTP error while engine requesting
                err_code = 2
                err_message = "Got HTTP error %s" % resp.status_code
                sess.delete(graph)
        except requests.exceptions.ConnectionError:
            # System error while engine requesting
            err_code = 1
            err_message = "Cant connect to %s" % ce_url
            sess.delete(graph)

        return {"error": err_code, "message": err_message}

    @cherrypy.expose(["finish-graph"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def finish_graph(self):
        err_code = 1
        if "graph_id" in cherrypy.request.json:
            graph_id = cherrypy.request.json["graph_id"]
            graph = GraphModel.get(cherrypy.request.sa, graph_id)
            graph.updated = datetime.datetime.now()
            graph.finished = True
            err_code = 0
        return {"error": err_code}

    @cherrypy.expose(["delete-graph"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def delete_graph(self):
        err_code = 1
        if "graph_id" in cherrypy.request.json:
            graph_id = cherrypy.request.json["graph_id"]
            sess = cherrypy.request.sa
            graph = GraphModel.get(sess, graph_id)
            sess.delete(graph)
            sess.commit()
            err_code = 0
        return {"error": err_code}

    @cherrypy.expose(["update-graph"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def update_graph(self):
        graph_id = cherrypy.request.json["graph_id"]
        x = cherrypy.request.json["x"]
        y = cherrypy.request.json["y"]

        cherrypy.log(json.dumps(cherrypy.request.json))

        sess = cherrypy.request.sa

        # Data
        data = DataModel(graph_id, x, y)
        sess.add(data)
        sess.flush()

        updated = datetime.datetime.now()

        # Graph
        graph = GraphModel.get(sess, graph_id)
        graph.updated = updated

        # Calculation
        calc = CalculationModel.get(sess, graph.calculation_id)
        calc.updated = updated

        return {"error": 0}

    @cherrypy.expose(["create-calculation"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def create_calculation(self):
        title = cherrypy.request.json["title"]
        description = cherrypy.request.json["description"]
        params_template = cherrypy.request.json["params_template"]

        sess = cherrypy.request.sa

        calculation = CalculationModel(title, description, params_template)
        sess.add(calculation)
        sess.flush()

        return {"error": 0}
