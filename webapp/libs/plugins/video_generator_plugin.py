from cherrypy.process import plugins
from webapp.libs.video_generator import VideoGenerator
from webapp.libs.graph_image_helper import GraphImageHelper


__all__ = ['VideoGeneratorPlugin']


class VideoGeneratorPlugin(plugins.SimplePlugin):
    def __init__(self, bus, ticks_to_generate_movie, movie_frame_rate):
        """ Simply constructor """
        plugins.SimplePlugin.__init__(self, bus)

        # Params for video generation
        self.movie_frame_rate = movie_frame_rate
        self.frame_size = (710, 710)
        self.ticks_to_generate_movie = ticks_to_generate_movie

        # We have to gen video not each time event called but
        # each 5-10th iteration let's say. So we have to remember
        # who is in process
        self.processing_graphs = {}

    def start(self):
        """ Starting plugin """
        self.bus.subscribe('update-graph-image', self.update_graph_image)
        self.bus.subscribe('finish-graph', self.finish_graph)
        self.bus.log('VideoGenerator plugin started.')

    def stop(self):
        """ Stopping plugin """
        self.bus.unsubscribe('update-graph-image', self.update_graph_image)
        self.bus.unsubscribe('finish-graph', self.finish_graph)
        self.bus.log('VideoGenerator plugin stopped.')

    def update_graph_image(self, graph_id):
        if graph_id not in self.processing_graphs:
            self.processing_graphs[graph_id] = {
                'updates_count': 1,
                'images_dir_path': GraphImageHelper.get_graph_path(graph_id),
                'output_file_path': GraphImageHelper.get_movie_path(graph_id)}
        if self.processing_graphs[graph_id]['updates_count'] % self.ticks_to_generate_movie:
            self.generate_movie(graph_id)
        self.processing_graphs[graph_id]['updates_count'] += 1

    def finish_graph(self, graph_id):
        if graph_id in self.processing_graphs:
            self.generate_movie(graph_id)
            self.processing_graphs.pop(graph_id, None)

    def generate_movie(self, graph_id):
        if graph_id in self.processing_graphs:
            images_dir_path = self.processing_graphs[graph_id]['images_dir_path']
            output_file_path = self.processing_graphs[graph_id]['output_file_path']
            VideoGenerator.run(images_dir_path, output_file_path, self.movie_frame_rate, self.frame_size)
