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
		path: path.resolve(__dirname, '../public/scripts')
	},
	devtool: 'inline-source-map',
	cache: false,
	devServer: {
		contentBase: ['./src', './public'], // Old version uses `contentBase`
		inline: true,
		hot: true, // Enable Hot Module Replacement (HMR)
		port: 3000,
		host: '0.0.0.0', // Required for Docker compatibility
		historyApiFallback: true, // Fix React Router issues (if needed)
		watchContentBase: true, // Ensures static files are watched
		watchOptions: {
			poll: 1000, // Fix file watching issues inside Docker
			ignored: /node_modules/,
		},
		headers: {
			'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
			'Pragma': 'no-cache',
			'Expires': '0'
		},
	clientLogLevel: 'info', // Log more info to the browser console

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
