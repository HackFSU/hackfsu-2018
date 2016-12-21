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
dirs.build = dirs.website + '/build/static';
dirs.src = dirs.website + '/src';
dirs.viewSrc = dirs.src + '/views';
dirs.viewDst = dirs.website + '/build/views';

function getViewFiles(directory, extension) {
    return [
        directory + '/**/*.' + extension,
        '!' + directory + '/**/_*',
        '!' + directory + '/_*',
        '!' + directory + '/_*/**'
    ];
}


/**
 * CSS
 */
gulp.task('css', function() {
    var sass = require('gulp-sass');
    var autoPrefixer = require('gulp-autoprefixer');
    var sourceMaps = require('gulp-sourcemaps');

    return gulp.src(getViewFiles(dirs.src, 'scss'))
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
        .pipe(gulp.dest(dirs.build));
});


/**
 * HTML
 * These are separated from the rest to be loaded by Django individually.
 */
gulp.task('html', function() {
    var pug = require('gulp-pug');

    return gulp.src(getViewFiles(dirs.viewSrc, 'pug'))
        .pipe(pug({
            pretty: true,
            locals: require(dirs.src + '/_pug/locals.js')
        }))
        .pipe(gulp.dest(dirs.viewDst));
});


/**
 * JS
 */
gulp.task('js', function() {
    var sourceMaps = require('gulp-sourcemaps');
    var uglify = require('gulp-uglify');
    var header = require('gulp-header');

    return gulp.src(getViewFiles(dirs.src, 'js'))
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
        .pipe(gulp.dest(dirs.build));
});


gulp.task('bower', function() {
    var bower = require('gulp-bower');
    return bower();
});

gulp.task('demo', function() {
    var demoServer = require('./website/demoServer');
    demoServer.boot();
});

gulp.task('build', ['bower', 'css', 'html', 'js']);

gulp.task('watch', ['build'], function(){
    return gulp.watch([dirs.src + '/**/*'], ['build']);
});

gulp.task('default', ['build']);
