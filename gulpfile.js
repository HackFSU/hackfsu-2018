/**
 * Gulp Configuration
 *
 * Builds website, deploys server
 */

'use strict';

var gulp = require('gulp');
var pkg = require('./package.json');

var banner =
    '/** \n' +
    ' * <%= pkg.name %> - <%= pkg.description %>\n' +
    ' * @version v<%= pkg.version %>\n' +
    ' * @link <%= pkg.homepage %>\n' +
    ' * @license <%= pkg.license %>\n' +
    ' */\n\n';

var dirs = {};
dirs.website = __dirname + '/website';
dirs.build = dirs.website + '/static_build';
dirs.viewsSrc = dirs.website + '/views';
dirs.viewsDest = dirs.build + '/views';

function getViewFiles(extension) {
    return [
        dirs.viewsSrc + '/**/*.' + extension,
        '!' + dirs.viewsSrc + '/**/_*',
        '!' + dirs.viewsSrc + '/_*',
        '!' + dirs.viewsSrc + '/_*/**'
    ];
}


/**
 * CSS
 */
gulp.task('css', function() {
    var sass = require('gulp-sass');
    var autoPrefixer = require('gulp-autoprefixer');
    var sourceMaps = require('gulp-sourcemaps');

    return gulp.src(getViewFiles('scss'))
        .pipe(sourceMaps.init())
        .pipe(sass.sync({
            outputStyle: 'compact',
        }).on('error', sass.logError))
        .pipe(autoPrefixer({
            cascade: false
        }))
        .pipe(sourceMaps.write('./',{
            addComment: true,
            includeContent: true
        }))
        .pipe(gulp.dest(dirs.viewsDest));
});


/**
 * HTML
 */
gulp.task('html', function() {
    var pug = require('gulp-pug');

    return gulp.src(getViewFiles('pug'))
        .pipe(pug({
            pretty: true,
            locals: require(dirs.viewsSrc + '/_pug/locals.js')
        }))
        .pipe(gulp.dest(dirs.viewsDest));
});


/**
 * JS
 */
gulp.task('js', function() {
    var sourceMaps = require('gulp-sourcemaps');
    var uglify = require('gulp-uglify');
    var header = require('gulp-header');

    return gulp.src(getViewFiles('js'))
        .pipe(sourceMaps.init())
        .pipe(header(banner, {pkg : pkg}))
        .pipe(uglify({
            mangle: true,
            compress: true
        }))
        .pipe(sourceMaps.write('./', {
            addComment: true,
            includeContent: true
        }))
        .pipe(gulp.dest(dirs.viewsDest));
});


gulp.task('bower', function() {
    var bower = require('gulp-bower');
    return bower();
});

gulp.task('demo', ['bower'], function() {
    var demoServer = require('./website/demoServer');
    demoServer.boot();
});

gulp.task('build', ['css', 'html', 'js']);

gulp.task('watch', ['build'], function(){
    return gulp.watch([dirs.viewsSrc + '/**/*'], ['build']);
});

gulp.task('default', ['build']);
