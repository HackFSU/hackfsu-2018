var webpack = require('webpack');

module.exports = [{
    entry: './public/js/register/index.js',
    plugins: [
        new webpack.EnvironmentPlugin({
            API_HOST: 'https://api.hackfsu.com'
        })
    ],
    output: {
        filename: './public/js/register.js'
    }
}];
