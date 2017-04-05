var gulp = require('gulp');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');


gulp.task('default', function () {
    runSequence(
        'build'
    );
});

gulp.task('build', function () {
    runSequence(
        'sass'
    );
    gulp.src(['node_modules/material-design-icons/iconfont/**', '!**/README.md'])
        .pipe(gulp.dest('antraege/static/antraege/material-design-icons/iconfont'));
    gulp.src(['node_modules/material-design-lite/*.min.js', 'node_modules/material-design-lite/*.min.css'])
        .pipe(gulp.dest('antraege/static/antraege/material-design-lite'))
});

gulp.task('sass', function () {
    gulp.src('antraege/static/antraege/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('antraege/static/antraege'))
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename({ extname: '.min.css' }))
        .pipe(gulp.dest('antraege/static/antraege'))
});