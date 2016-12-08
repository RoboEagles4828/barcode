var attendance = {};

var getAttendance = function() {
	var attendanceContainer = document.getElementById("attendanceContainer");
	attendanceContainer.innerHTML = "<div class=\"loader\"></div>";

// uncomment to delay GET by 1 second
//setTimeout(function() {

	$.get("attendance.php", function(data) {
		if (data != null && data.length > 10) {
			attendance = JSON.parse(data);
			openList();
		} else {
			attendanceContainer.innerHTML = "<p>No Attendance Records Were Found</p>";
		}
	});

// uncomment to delay GET by 1 second
//}, 1000);

}

var openList = function() {
	document.getElementById("leftbutton").style.visibility = "hidden";
	document.getElementById("rightbutton").onclick = getAttendance;
	document.getElementById("rightbutton").innerHTML = "Refresh";

	var view = '<div class="col-xs-0 col-lg-1"></div>'
	view += '<div class="col-xs-12 col-lg-10">'
	view += '<div class="container-fluid">'
	for (date in attendance) {
		view += '<div class="col-sm-6 col-md-4">'
		view += '<div class="button" onclick="openFile(' + "'"+ date + "'" + ')"><div>'
		view += date;
		view += '</div></div></div>'
	}
	view += '</div></div>'
	view += '<div class="col-xs-0 col-lg-1"></div>'

	attendanceContainer.innerHTML = view;
}

var openFile = function(i) {
	document.getElementById("leftbutton").style.visibility = "";
	document.getElementById("rightbutton").onclick = function() { download(makeCsv(i), i + ".csv", "text/csv"); };
	document.getElementById("rightbutton").innerHTML = "Download";

	var view = "<p>" + makeCsv(i).replace(/\n/g,"</p><p>") + "</p>";
	attendanceContainer.innerHTML = view;
}

var makeCsv = function(i) {
	var file = attendance[i];
	var csv = "";
	for (ID in file) {
		csv += ID + ",";
		csv += file[ID]["name"] + ",";
		csv += file[ID]["times"]["total"];
		csv += "\n"
	}

	return csv
}
