const path = require('path');
// const Reload = require('webpack-livereload-plugin');
// const CleanWebpackPlugin = require('clean-webpack-plugin');
// const HtmlWebpackPlugin = require('html-webpack-plugin');

process.env.NODE_ENV = 'development';

module.exports = {
	entry: './src/frontend-scripts/game-app.js',
	plugins: [
		// new Reload(),
		// new CleanWebpackPlugin(['../public/scripts']),
		// new HtmlWebpackPlugin({
		// 	title: 'caching'
		// })
	],
	output: {
		filename: 'bundle.js',
		path: path.resolve(__dirname, '../public/scripts'),
		publicPath: '/'
	},
	devtool: 'inline-source-map',
	cache: false,
	devServer: {
		contentBase: ['./src', './public', './views'],
		hot: true,
		port: 3000,
		host: '0.0.0.0',
		historyApiFallback: true,
		watchContentBase: true,
		writeToDisk: true,
		watchOptions: {
		  poll: 1000,
		  ignored: /node_modules/,
		},
		headers: {
		  'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
		  'Pragma': 'no-cache',
		  'Expires': '0',
		},
		clientLogLevel: 'info',
	  },
	module: {
		rules: [
			{
				test: /\.(html)$/,
				use: {
					loader: 'html-loader',
					options: {
						attrs: [':data-src']
					}
				}
			},
			{
				test: /\.(png|svg|jpg|gif)$/,
				use: {
					loader: 'file-loader',
					options: {
						useRelativePath: true
					}
				}
			},
			{
				test: /\.(js|jsx)$/,
				use: {
					loader: 'babel-loader',
					query: {
						presets: ['react-app']
					}
				},
				exclude: /node_modules/
			},
			{
				test: /\.s?css$/,
				use: [
					{
						loader: 'style-loader'
					},
					{
						loader: 'css-loader',
						options: {
							sourceMap: true
						}
					},
					{
						loader: 'sass-loader',
						options: {
							sourceMap: true
						}
					}
				]
			}
		]
	}
};
