module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  assetsDir: 'static',
  devServer: {
    disableHostCheck: true
  },
  css: {
    loaderOptions: {
      scss: {
        prependData: "@import '@/styles/variables.scss';"
      }
    }
  },
  configureWebpack: {
    module: {
      rules: [
        // SCSS has different line endings than SASS
        // and needs a semicolon after the import.
        {
          test: /\.scss$/,
          use: [
            'vue-style-loader',
            'css-loader',
            {
              loader: 'sass-loader',
              // Requires sass-loader@^8.0.0
              options: {
                // This is the path to your variables
                prependData: "@import '@/styles/variables.scss';"
              },
            },
          ],
        },
      ],
    },
  }
}