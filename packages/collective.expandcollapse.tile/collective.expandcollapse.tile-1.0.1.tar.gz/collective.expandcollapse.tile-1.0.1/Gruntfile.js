const sass = require('node-sass');

module.exports = function(grunt) {
  'use strict';

  require('load-grunt-tasks')(grunt);
  var productRoot = 'src/collective/expandcollapse/tile/browser/static';
  grunt.initConfig({
    sass: {
      options: {
        implementation: sass,
        sourceMap: true,
        outputStyle: 'compressed',
      },
      dist: {
        files: {
          './src/collective/expandcollapse/tile/browser/static/dist/styles.css':
            './src/collective/expandcollapse/tile/browser/static/styles.scss',
        },
      },
    },
    requirejs: {
      'expand-collapse-tile': {
        options: {
          baseUrl: './',
          generateSourceMaps: true,
          preserveLicenseComments: false,
          paths: {
            jquery: 'empty:',
          },
          wrapShim: true,
          name: `${productRoot}/expand_collapse.js`,
          exclude: ['jquery'],
          out: `${productRoot}/dist/expand_collapse_compiled.js`,
          optimize: 'none',
        },
      },
    },
    babel: {
      options: {
        sourceMap: true,
        presets: ['env'],
      },
      dist: {
        files: {
          './src/collective/expandcollapse/tile/browser/static/dist/expand_collapse_compiled.js':
            './src/collective/expandcollapse/tile/browser/static/dist/expand_collapse_compiled.js',
        },
      },
    },

    uglify: {
      'expand-collapse-tile': {
        options: {
          sourceMap: true,
          sourceMapName: `./${productRoot}/dist/expand_collapse_compiled.js.map`,
          sourceMapIncludeSources: false,
        },
        files: {
          './src/collective/expandcollapse/tile/browser/static/dist/expand_collapse_compiled.min.js': [
            './src/collective/expandcollapse/tile/browser/static/dist/expand_collapse_compiled.js',
          ],
        },
      },
    },
    postcss: {
      options: {
        map: {
          inline: false,
        },
        processors: [
          require('autoprefixer')({
            grid: true,
            browsers: ['last 2 versions', 'ie >= 11', 'iOS >= 9'],
          }),
          require('postcss-flexbugs-fixes')(),
        ],
      },
      dist: {
        src: [`${productRoot}/dist/styles.css`],
      },
    },
    watch: {
      scripts: {
        files: [`${productRoot}/expand_collapse.js`],
        tasks: ['requirejs', 'babel', 'uglify'],
        options: {
          livereload: true,
        },
      },
      css: {
        files: `${productRoot}/styles.scss`,
        tasks: ['sass', 'postcss'],
        options: {
          livereload: true,
        },
      },
    },
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('compile', [
    'sass',
    'postcss',
    'requirejs',
    // 'babel',
    'uglify',
  ]);
};
