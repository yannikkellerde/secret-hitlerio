const fs = require('fs');
const path = require('path');
const http = require('http');

const options = {
	method: 'POST',
	hostname: 'localhost',
	port: '8080',
	path: '/account/signup',
	headers: {
		'content-type': 'application/json; charset=UTF-8'
	}
};

const createUser = function(username) {
	const req = http.request(options, function(res) {
		const chunks = [];

		res.on('data', function(chunk) {
			chunks.push(chunk);
		});

		res.on('end', function() {
			if (res.statusCode == 200) {
				console.log(`Successfully created ${username}`);
			} else if (res.statusCode == 401) {
				console.warn(`${username} already exists`);
			} else {
				console.error(`${username} returned error code ${res.statusCode}`);
			}
		});
	});
	let pass = username == "yannik" ? "Did_sh_beat_everyone" : "snipsnap";
	req.write(`{\"username\":\"${username}\",\"password\":\"${pass}\",\"password2\":\"${pass}\",\"isPrivate\":false,\"bypassKey\":\"igotthebypass\"}`);
	req.end();
};

const filePath = path.join(__dirname, '..', 'src', 'frontend-scripts', 'components', 'section-main', 'Defaultmid.jsx');
const fileString = fs.readFileSync(filePath, 'utf8');

const nameRegex = /data-name="([A-z]+)" className="loginquick">/g;

console.log('Creating accounts in MongoDB.  May give errors for repeated runs.');

let m;

usernames = ["Rexxar", "Malfurion", "Jaina", "Uther", "Anduin", "Valeera", "Thrall", "Guldan", "Garrosh", "aaa", "bbb", "ccc", "ddd", "eee", "fff", "yannik", "thomas", "levin", "tobias", "chaewon"]

for (let i = 0; i < usernames.length; i++) {
	createUser(usernames[i]);
}