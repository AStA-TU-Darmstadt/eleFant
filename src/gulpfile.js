var gulp = require('gulp');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');
var del = require('del');
var merge = require('merge-stream');


gulp.task('default', function () {
    return runSequence(
        'build'
    );
});

gulp.task('build', ['install-deps', 'sass'], function () {
});

gulp.task('build-clean', function () {
    return del(['elefant/static/elefant/**/_*.scss', 'elefant/static/elefant/*.css', '!elefant/static/elefant/*min.css']); // delete build deps
});

gulp.task('install-deps', function () {
    var icons = gulp.src(['node_modules/material-design-icons/iconfont/**', '!**/README.md', 'node_modules/material-design-icons/LICENSE']) // install icons
        .pipe(gulp.dest('elefant/static/elefant/material-design-icons'));
    var mdl_js = gulp.src(['node_modules/material-design-lite/*.min.js', 'node_modules/material-design-lite/LICENSE']) // install mdl js
        .pipe(gulp.dest('elefant/static/elefant/material-design-lite'));
    var roboto = gulp.src(['node_modules/roboto-slab-fontface-kit/**/*.ttf', 'node_modules/roboto-slab-fontface-kit/**/*.woff*', 'node_modules/roboto-slab-fontface-kit/**/*.scss']) // install roboto slab
        .pipe(gulp.dest('elefant/static/elefant/fonts/roboto-slab'));
    var raleway = gulp.src(['node_modules/typeface-raleway/*/*.eot', 'node_modules/typeface-raleway/**/*.woff*', 'node_modules/typeface-raleway/**/*.svg']) // install roboto slab
        .pipe(gulp.dest('elefant/static/elefant/fonts/raleway'));
    return merge(icons, mdl_js, roboto, raleway);
});

gulp.task('install-sass-build-deps', function () {
    return mdl_css = gulp.src('node_modules/material-design-lite/material.css') // install mdl css
        .pipe(rename("_material.scss"))
        .pipe(gulp.dest('elefant/static/elefant/material-design-lite'));
});

gulp.task('sass', ['install-sass-build-deps'], function () {
    return gulp.src('elefant/static/elefant/*.scss') // build sass
        .pipe(sass())
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename({extname: '.min.css'}))
        .pipe(gulp.dest('elefant/static/elefant'));
});
