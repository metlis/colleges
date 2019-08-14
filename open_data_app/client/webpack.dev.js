const path = require('path');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-source-map',
  output: {
    filename: 'dev.bundle.js',
    path: path.resolve(__dirname, '../static/open_data_app/js/build'),
  },
});