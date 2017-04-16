var gulp = require('gulp');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');
var del = require('del');
var merge = require('merge-stream');


gulp.task('default', function () {
    return runSequence(
        'build',
        'build-clean'
    );
});

gulp.task('build', ['install-deps', 'sass'], function () {
});

gulp.task('build-clean', function () {
    return del(['antraege/static/antraege/**/_*.scss', 'antraege/static/antraege/*.css', '!antraege/static/antraege/*min.css']); // delete build deps
});

gulp.task('install-deps', function () {
    var icons = gulp.src(['node_modules/material-design-icons/iconfont/**', '!**/README.md']) // install icons
        .pipe(gulp.dest('antraege/static/antraege/material-design-icons/iconfont'));
    var mdl_js = gulp.src('node_modules/material-design-lite/*.min.js') // install mdl js
        .pipe(gulp.dest('antraege/static/antraege/material-design-lite'));
    return merge(icons, mdl_js);
});

gulp.task('install-build-deps', function () {
    return gulp.src('node_modules/material-design-lite/material.css') // install mdl css
        .pipe(rename("_material.scss"))
        .pipe(gulp.dest('antraege/static/antraege/material-design-lite'));
});

gulp.task('sass', ['install-build-deps'], function () {
    return gulp.src('antraege/static/antraege/*.scss') // build sass
        .pipe(sass())
        .pipe(gulp.dest('antraege/static/antraege'))
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename({extname: '.min.css'}))
        .pipe(gulp.dest('antraege/static/antraege'));
});
