const gulp = require('gulp');
const zip = require('gulp-zip');
const minimist = require('minimist');

const config = {
    region: 'ap-northeast-1',
    handler: 'index.handler',
    functionName: 'gulp',
    role: 'arn:aws:iam::xxxxxxxxxxxx:role/service-role/test-gulp-xxxx', // 再デプロイ時は省略可能
    runtime: 'nodejs12.x'
  };

const options = minimist(process.argv.slice(2), {
	string: 'path',
	default: {
		path: '' // 引数の初期値
	}
});
const path = options.path;

gulp.task('zip', () => {
    console.log(path);
    if (path = ''){
        return false;
    }
    return gulp.src('lambda/' + path + '/**')
        .pipe(zip('lambda.zip'))
        .pipe(gulp.dest('dist/' + path ));
});
