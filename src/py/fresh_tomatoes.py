import webbrowser
import os
import re

output_file_name = os.path.abspath(__file__ + '/../../../dist/fresh_tomatoes.html')

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/coverflow.css">

    <script src="js/coverflow.js"></script>
    <script type="text/javascript" charset="utf-8">
        var movieDisplay;

        function showTrailer(trailerYouTubeId) {
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
            $('#trailer').modal('show')
        }

        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
          // Remove the src so the player itself gets removed, as this is the only
          // reliable way to ensure the video stops playing in IE
          $("#trailer-video-container").empty();
        });

        // When clicking on a movie cover, if the movie cover is active then play
        // the trailer; otherwise, just set it to active.
        // Start playing the video when the trailer modal is opened
        $(document).on('click', '#movie-covers img', function (event) {
            var $this = $(this);
            var selectedIdx = $this.index();
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')

            if (selectedIdx === movieDisplay.getCurrentIndex()) {
                showTrailer(trailerYouTubeId);
            } else {
                $titles = $('#movie-titles a');
                movieDisplay.moveTo(selectedIdx);
                $titles.removeClass('active');
                $titles.eq(selectedIdx).addClass('active');
            }
        });

        // When clicking on a movie title, if the resolution is extra-small (i.e. phones)
        // play the trailer immediately. Otherwise, set its corresponding movie cover to active.
        $(document).on('click', '#movie-titles li', function (event) {
            var $this = $(this);
            var selectedIdx = $this.index()
            var trailerYouTubeId;

            // Clear active status on movie titles
            $('#movie-titles a').removeClass('active');
            $this.find('a').addClass('active');

            if (window.matchMedia("(min-width: 768px)").matches) {
              // viewport matches S, M and L devices
              movieDisplay.moveTo(selectedIdx);
            } else {
              // the viewport matches x-small devices
              trailerYouTubeId = $('#movie-covers img').eq(selectedIdx).attr('data-trailer-youtube-id');
              showTrailer(trailerYouTubeId);
            }
        });

        $(document).ready(function () {
          movieDisplay = new Coverflow('movie-covers', {
            angleInactive: 60,
            current: 0,
            gap: 30,
            zActive: 300
          });
          movieDisplay.init();

          if (window.matchMedia("(min-width: 768px)").matches) {
            // Show the first movie as selected for S, M and L devices
            $('#movie-titles a').first().addClass('active');
          }
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row-fluid">
        <div class="col-md-4 col-sm-6">
          <ul id="movie-titles">
              {movie_titles}
          </ul>
        </div>
        <div id="mc-container" class="col-md-8 col-sm-6 hidden-xs">
          <div id="movie-covers">
              {movie_images}
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_cover_content = '''
    <img src="{poster_image_url}"
         width="220"
         height="342"
         data-trailer-youtube-id="{trailer_youtube_id}">
'''

# A single movie entry html template
movie_title_content = '''
<li><a href="#">{movie_title}</a></li>
'''

def create_movie_images_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie cover with its content filled in
        content += movie_cover_content.format(
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

def create_movie_titles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        content += movie_title_content.format(
            movie_title=movie.title.encode('utf-8')
        )
    return content

def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open(output_file_name, 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_titles=create_movie_titles_content(movies),
        movie_images=create_movie_images_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
