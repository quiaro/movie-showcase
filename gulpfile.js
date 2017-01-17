const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const browserSync = require('browser-sync').create();
const eslint = require('gulp-eslint');
const babel = require('gulp-babel');

/*
 * Compiles sass, lints and tranpiles scripts and
 * starts a local server that watches for changes to
 * the styles and the scripts. (*Does not* run tests)
 */
gulp.task('default', [
    'styles', 'lint', 'scripts'
], function defaultTask() {
    gulp.watch('src/sass/**/*.scss', ['styles']);

    gulp.watch('src/js/**/*.js').on('change', function() {
        gulp.start('lint');
        gulp.start('scripts');
        browserSync.reload();
    });

    browserSync.init({server: './dist'});
});

/*
 * Run tests, lint and transpiles scripts, and transpile sass files.
 * Per the [Gulp API doc](https://github.com/gulpjs/gulp/blob/master/docs/API.md),
 * since the tasks will run in parallel (all at once), the stream is not stopped
 * if a test fails (since there's not much gain in doing so).
 */
gulp.task('build', ['lint', 'scripts', 'styles']);

/*
 * Lint scripts with ESLint
 */
gulp.task('lint', function lintTask() {
    // ESLint ignores files with "node_modules" paths.
    // So, it's best to have gulp ignore the directory as well.
    // Also, Be sure to return the stream from the task;
    // Otherwise, the task may end before the stream has finished.
    return gulp.src(['src/js/**/*.js', '!node_modules/**'])
    // eslint() attaches the lint output to the "eslint" property
    // of the file object so it can be used by other modules.
        .pipe(eslint())
    // eslint.format() outputs the lint results to the console.
    // Alternatively use eslint.formatEach() (see Docs).
        .pipe(eslint.format())
    // To have the process exit with an error code (1) on
    // lint error, return the stream and pipe to failAfterError last.
        .pipe(eslint.failAfterError());
});

/*
 * Transpile scripts
 */
gulp.task('scripts', function scriptsTask() {
    // Transform ES6 code to ES5
    gulp.src('src/js/**/*.js')
      .pipe(babel({
        presets: ['es2015']
      }))
      .pipe(gulp.dest('dist/js'));
});

/*
 * Compile sass files
 */
gulp.task('styles', function stylesTask() {
    gulp.src(['src/sass/main.scss', 'src/sass/coverflow.scss'])
      .pipe(sass().on('error', sass.logError))
      .pipe(autoprefixer({browsers: ['last 2 versions']}))
      .pipe(gulp.dest('dist/css'))
      .pipe(browserSync.stream());
});
