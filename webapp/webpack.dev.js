var webpack = require('webpack');

module.exports = [{
    entry: './public/js/register/index.js',
    plugins: [
        new webpack.EnvironmentPlugin({
            API_HOST: 'http://localhost:8080'
        })
    ],
    output: {
        filename: './public/js/register.js'
    }
}];
