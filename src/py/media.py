class Movie():
    '''Class encapsulating all attributes and methods of a movie'''

    def __init__(self, data):
        self.title = data['title'];
        self.trailer_youtube_url = data['trailer_youtube_url'];
        self.poster_image_url = data['poster_image_url'];
