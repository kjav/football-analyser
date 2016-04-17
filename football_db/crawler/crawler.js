var page = require('webpage').create();
var everton_match_url = 'http://www.whoscored.com/Matches/614052/Live';
var google_url = 'http://www.google.com';
console.log("crawler.js starting.....");

var fs = require('fs');
var special_script = fs.read('prettydecoded.js');


page.open(google_url, function(status) {
	page.evaluateJavascript(special_script);
	console.log('evaluated the javascript....');
	page.render('everton.png');
	phantom.exit();
});

