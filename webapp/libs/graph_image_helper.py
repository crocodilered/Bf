import cherrypy
import os
import shutil


__all__ = ['GraphImageHelper']


class GraphImageHelper:

    @staticmethod
    def get_graph_path(graph_id):
        ce_config = cherrypy.tree.apps[''].config['CalculationsEngine']
        return os.path.join(ce_config['ce.images_path'], '%06d' % int(graph_id))

    @staticmethod
    def get_movie_href(graph_id):
        # TODO: write it right way
        return '/images/%06d/%06d.mp4' % (int(graph_id), int(graph_id))

    @staticmethod
    def get_movie_path(graph_id):
        graph_path = GraphImageHelper.get_graph_path(graph_id)
        movie_name = '%06d.mp4' % int(graph_id)
        return os.path.join(graph_path, movie_name)

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

    @staticmethod
    def clear_graph_movie(graph_id):
        path = GraphImageHelper.get_movie_path(graph_id)
        if os.path.isfile(path):
            os.remove(path)
