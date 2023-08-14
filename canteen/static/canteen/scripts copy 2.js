function testFunc(orderID, itemID, reqUser, action) {
	console.log('inside testFunc')
	console.log('orderID: ' + orderID)
	console.log('itemID: ' + itemID)
	console.log('action: ' + action)
	console.log('reqUser: ' + reqUser)
}

var end = 0 // change this to stop the counter at a higher value
var refresh = 1000; // Refresh rate in milli seconds

console.log('Inside scripts.js file')

function display_c(start) {
	window.start = parseFloat(start);

	if (window.start >= end) {
		mytime = setTimeout('display_ct()', refresh)
	}
	else { alert("Time Over "); }
}

function display_ct() {
	// Calculate the number of days left
	var days = Math.floor(window.start / 86400);

	// After deducting the days calculate the number of hours left
	var hours = Math.floor((window.start - (days * 86400)) / 3600);

	// After days and hours , how many minutes are left 
	var minutes = Math.floor((window.start - (days * 86400) - (hours * 3600)) / 60);

	// Finally how many seconds left after removing days, hours and minutes. 
	var secs = Math.floor((window.start - (days * 86400) - (hours * 3600) - (minutes * 60)));

	var x = window.start + "(" + days + " Days " + hours + " Hours " + minutes + " Minutes and " + secs + " Secondes " + ")";
	document.getElementById('showtime').innerHTML = x;

	window.start = window.start - 1;

	tt = display_c(window.start);
}