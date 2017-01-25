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
dirs.buildRoot = dirs.webapp + '/build';
dirs.build = dirs.buildRoot + '/static';
dirs.src = dirs.webapp;
dirs.viewSrc = dirs.src + '/views';
dirs.viewDst = dirs.buildRoot + '/views';

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
gulp.task('css:watch', ['css'], function() {
    return gulp.watch([
        dirs.src + '/_sass/**/*',
        dirs.src + '/css/**/*.scss',
        dirs.src + '/views/**/*.scss',
        '!' + dirs.build + '/**/*'
    ], ['css']);
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
gulp.task('html:watch', ['html'], function() {
    return gulp.watch([
        dirs.src + '/_pug/**/*',
        dirs.src + '/views/**/*.pug',
        dirs.src + '/views/**/*.html',
        dirs.src + '/views/**/*.md',
        '!' + dirs.build + '/**/*'
    ], ['html']);
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
gulp.task('js:watch', ['js'], function() {
    return gulp.watch([
        dirs.src + '/js/**/*.js',
        dirs.src + '/views/**/*.js',
        '!' + dirs.build + '/**/*'
    ], ['js']);
});

gulp.task('bower', function() {
    var bower = require('gulp-bower');
    return bower();
});


// Remove built files so they can be re-built freshly
gulp.task('clean', function(done) {
    var fs = require('fs-extra');
    console.log('rm -rf ' + dirs.buildRoot);
    fs.remove(dirs.buildRoot, function(err) {
        if (err) {
            console.log('Error:', err);
        }
        done();
    });
});

gulp.task('demo', function() {
    var demoServer = require('./demoServer');
    demoServer.boot();
});

gulp.task('build', ['bower', 'css', 'html', 'js']);

gulp.task('watch', ['build'], function(){
    return gulp.watch([
        dirs.src + '/**/*.pug',
        dirs.src + '/**/*.scss',
        dirs.src + '/**/*.js',
        '!' + dirs.build + '/**/*'
    ], ['build']);
});


gulp.task('default', ['build']);
