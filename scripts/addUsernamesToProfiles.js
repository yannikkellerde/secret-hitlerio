const mongoose = require('mongoose');
const Profile = require('../models/profile');

mongoose.Promise = global.Promise;
mongoose.connect(process.env.MONGO_URL + `secret-hitler-app`);

Profile.find({})
	.cursor()
	.eachAsync(profile => {
		profile.username = profile._id;
		profile.save();
	})
	.then(() => {
		console.log('profile updates complete');
	});
