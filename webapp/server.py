import os.path
import cherrypy
from webapp.libs.plugins.saplugin import SaPlugin
from webapp.libs.plugins.makoplugin import MakoTemplatePlugin
from webapp.libs.plugins.video_generator_plugin import VideoGeneratorPlugin
from webapp.libs.tools.makotool import MakoTool
from webapp.libs.tools.authtool import AuthTool
from webapp.libs.tools.satool import SaTool


def error_page(status, message, traceback, version):
    if cherrypy.response.status == 401:
        s = open('templates/errors/401.html', 'r', encoding='UTF-8').read()
        return_url = '%s?%s' % (cherrypy.request.path_info, cherrypy.request.query_string)
        return s % return_url.replace('?', '%3F').replace('/', '%2F')
    elif cherrypy.response.status == 404:
        return open('templates/errors/404.html', 'rb')


cherrypy.tools.sa = SaTool()
cherrypy.tools.render = MakoTool()
cherrypy.tools.auth = AuthTool()

from webapp.controllers.app import App
from webapp.controllers.calculation import Calculation
from webapp.controllers.api import Api

app = App()
app.calculation = Calculation()
app.api = Api()

curr_dir = os.path.abspath(os.path.dirname(__file__))
conf_file = os.path.join(curr_dir, 'conf', 'server.conf')

application = cherrypy.tree.mount(app, '/', conf_file)

cherrypy.config.update(conf_file)
cherrypy.config.update({'error_page.401': error_page})
cherrypy.config.update({'error_page.404': error_page})

MakoTemplatePlugin(cherrypy.engine,
                   os.path.join(curr_dir, 'templates'),
                   os.path.join(curr_dir, 'templates', '.cache')).subscribe()

ce_config = application.config['CalculationsEngine']
VideoGeneratorPlugin(cherrypy.engine,
                     ce_config['ce.ticks_to_generate_movie'],
                     ce_config['ce.movie_frame_rate']).subscribe()

db_config = application.config['Database']
mysql_connection_string = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (db_config['mysql.user'],
                                                                   db_config['mysql.password'],
                                                                   db_config['mysql.host'],
                                                                   db_config['mysql.port'],
                                                                   db_config['mysql.database'])
cherrypy.engine.sa = SaPlugin(cherrypy.engine, mysql_connection_string)
cherrypy.engine.sa.subscribe()


if __name__ == '__main__':
    cherrypy.engine.start()
