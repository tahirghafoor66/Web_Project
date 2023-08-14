function testFunc(orderID, itemID, reqUser, action) {
	console.log('inside testFunc')
	console.log('orderID: ' + orderID)
	console.log('itemID: ' + itemID)
	console.log('action: ' + action)
	console.log('reqUser: ' + reqUser)
}

var end = 600 // change this to stop the counter at a higher value
var refresh = 1000; // Refresh rate in milli seconds

console.log('scripts.js file loaded....')

function diff_minutes(dt2, dt1) {

	var diff = (dt2.getTime() - dt1.getTime()) / 1000;
	diff /= 60;
	return Math.abs(Math.round(diff));

}

dt1 = new Date(2014, 10, 2);
dt2 = new Date(2014, 10, 3);
console.log('time difference is ' + diff_minutes(dt1, dt2));


function displayTime(start) {
	window.start = parseFloat(start);

	if (window.start >= end) {
		mytime = setTimeout('calculateDiff()', refresh)
	}
	else { alert("Order Completed "); }
}

function calculateDiff() {
	// Calculate the number of days left
	var days = Math.floor(window.start / 86400);

	// After deducting the days calculate the number of hours left
	var hours = Math.floor((window.start - (days * 86400)) / 3600);

	// After days and hours , how many minutes are left 
	var minutes = Math.floor((window.start - (days * 86400) - (hours * 3600)) / 60);

	// Finally how many seconds left after removing days, hours and minutes. 
	var secs = Math.floor((window.start - (days * 86400) - (hours * 3600) - (minutes * 60)));

	var timeleft = days + " Days " + hours + " Hours " + minutes + " Minutes and " + secs + " Secondes " + "are remaing to Complete the Order";
	


	document.getElementById('showtime').innerHTML = timeleft;

	window.start = window.start - 1;

	dt = displayTime(window.start);
}