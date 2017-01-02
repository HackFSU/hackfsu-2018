/**
 * Gulp Configuration
 *
 * Builds webapp, deploys server
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
dirs.webapp = __dirname + '/webapp';
dirs.build = dirs.webapp + '/build/static';
dirs.src = dirs.webapp;
dirs.viewSrc = dirs.src + '/views';
dirs.viewDst = dirs.webapp + '/build/views';

function getViewFiles(directory, extension) {
    return [
        directory + '/**/*.' + extension,
        '!' + directory + '/**/_*',
        '!' + directory + '/_*',
        '!' + directory + '/_*/**',
        '!' + dirs.build + '/*',
        '!' + dirs.build + '/**/*',
        '!' + dirs.static + '/*',
        '!' + dirs.static + '/**/*'
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
 * Each html file is run through the Django template engine.
 */
gulp.task('html', function() {
    var pug = require('gulp-pug');
    var locals = require(dirs.src + '/_pug/locals.js');

    return gulp.src(getViewFiles(dirs.viewSrc, 'pug'))
        .pipe(pug({
            pretty: true,
            locals: locals
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
    var gutil = require('gulp-util');

    return gulp.src(getViewFiles(dirs.src, 'js'))
        .pipe(sourceMaps.init())
        .pipe(header(banner, {pkg : pkg}))
        .pipe(uglify({
            mangle: true,
            compress: true
        }).on('error', gutil.log))
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
    var demoServer = require('./demoServer');
    demoServer.boot();
});

gulp.task('build', ['bower', 'css', 'html', 'js']);

gulp.task('watch', ['build'], function(){
    return gulp.watch([dirs.src + '/**/*'], ['build']);
});

gulp.task('default', ['build']);
