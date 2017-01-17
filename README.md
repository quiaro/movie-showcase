Movie Trailer Site
=====================

Demo project to view a list of movies and watch their trailers.

---

## Features
- See a listing of movie titles sorted alphabetically
- 'Cover flow'-like display of movie covers
- Clicking on the main movie cover shows its trailer
- Clicking on side movie covers results in scrolling
- Clicking on a movie title from the listing will show the corresponding movie cover
- Responsive design (movie covers will not be displayed in x-small devices; instead, clicking on a movie title will immediately launch its trailer)

---

## Setup
Clone this repo to a folder in your computer.
```
$ git clone https://github.com/quiaro/movie-showcase.git
```

Install project dependencies.
```
$ npm install
```

---

## Usage
Make sure you have python 2 installed.

Go to the project directory.
`$ cd movie-showcase`

Build the project. This should automatically open a local HTML file in your default browser with a selected list of movies. Enjoy!
`$ npm run build`

---

## Credits

- Drew lots of inspiration from ["Coverflow animation using CSS3 3D Transformations"](https://jbkflex.wordpress.com/2012/02/13/coverflow-animation-using-css3-3d-transformations-part1/) by Joseph Khan

---

## License

This project is licensed under the terms of the [**MIT**](https://opensource.org/licenses/MIT) license.
