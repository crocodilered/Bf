import cherrypy
import os
import shutil


__all__ = ['GraphImageHelper']


class GraphImageHelper:

    @staticmethod
    def get_graph_path(graph_id):
        ce_config = cherrypy.tree.apps[''].config['CalculationsEngine']
        return os.path.join(ce_config['ce.images_cache_path'], '%04d' % int(graph_id))

    @staticmethod
    def get_image_path(data):
        r = None
        if data and data.is_image():
            graph_path = GraphImageHelper.get_graph_path(data.graph_id)
            r = os.path.join(graph_path, '%020d.png' % int(data.id))
        return r

    @staticmethod
    def prepare_graph_path(graph_id):
        """ Use this method before image saving. """
        if graph_id:
            graph_path = GraphImageHelper.get_graph_path(graph_id)
            if not os.path.isdir(graph_path):
                os.makedirs(graph_path)

    @staticmethod
    def clear_graph_path(graph_id):
        if graph_id:
            graph_path = GraphImageHelper.get_graph_path(graph_id)
            if os.path.isdir(graph_path):
                shutil.rmtree(graph_path)
