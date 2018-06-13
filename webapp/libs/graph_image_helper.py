import cherrypy
import os


__all__ = ['GraphImageHelper']


class GraphImageHelper:

    @staticmethod
    def path(data):
        r = None
        if data and data.is_image():
            ce_config = cherrypy.tree.apps[''].config['CalculationsEngine']
            images_path = ce_config['ce.images_cache_path']
            r = os.path.join(images_path, '%04d' % int(data.graph_id), '%020d.png' % int(data.id))
        return r
