const path = require('path');

module.exports = {
  entry: './index.js',
  output: {
    filename: 'home.js',
    path: path.resolve(__dirname, 'dist')
  },
  resolve: {
      alias: {
          jquery: "jquery/src/jquery"
      }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};