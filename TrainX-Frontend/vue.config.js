module.exports = {
  devServer: {
    compress: true,
    disableHostCheck: true,
    port: 4200,
    host: '0.0.0.0',
    progress: false,
    watchOptions: {
      aggregateTimeout: 300,
      poll: 1000
    }
  },
}
