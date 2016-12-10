var attendance = {};
var analysis = {};
var attendanceContainer = document.getElementById("attendanceContainer");
var leftbutton = document.getElementById("leftbutton");
var rightbutton = document.getElementById("rightbutton");

var getAttendance = function() {
	attendanceContainer = document.getElementById("attendanceContainer");
	leftbutton = document.getElementById("leftbutton");
	rightbutton = document.getElementById("rightbutton");
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
	leftbutton.onclick = analyze;
	leftbutton.innerHTML = "Analyze";
	rightbutton.onclick = getAttendance;
	rightbutton.innerHTML = "Refresh";

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
	document.getElementById("leftbutton").onclick = openList;
	document.getElementById("leftbutton").innerHTML = "Back";
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
		csv += "\n";
	}

	return csv
}

var str = function(i) {
	ret = i.toString();
	if (i < 10) {
		return "0" + ret;
	}
	return ret
}

var time_to_seconds = function(time) {
	var t = time.split(":");
	return 3600 * parseInt(t[0]) + 60 * parseInt(t[1]) + parseInt(t[2])};

var seconds_to_time = function(s){
	var hr = Math.floor(s / 3600);
	s -= hr * 3600;
	var mn = Math.floor(s / 60);
	s -= mn * 60;
	return str(hr) + ":" + str(mn) + ":" + str(s);
}

var analyze = function() {
	var times = "";
	var view = "";

	leftbutton.onclick = openList;
	leftbutton.innerHTML = "Back";
	rightbutton.onclick = function() { download(times, "analysis.csv", "text/csv"); };;
	rightbutton.innerHTML = "Download";

	var people = {};
	var count = 0;
	for (file in attendance) {
		for (ID in attendance[file]) {
			if (!people.hasOwnProperty(ID)) {
				people[ID] = {"time": 0, "name": attendance[file][ID]["name"]};
			}

			count++;
			people[ID]["time"] += time_to_seconds(attendance[file][ID]["times"]["total"]);
		}
	}
	hrs = 0;
	for (person in people) {
		hrs += people[person]["time"];
	}

	hrs = Math.round(hrs / 360) / 10;

	view = "<p>" + count + " people worked for " + hrs + " hours</p>";
	for (person in people) {
		times += person + "," + people[person]["name"] + "," + seconds_to_time(people[person]["time"]) + "\n";
	}

	view += "<hr/>" + times.replace(/\n/g,"</p><p>") + "</p>";

	attendanceContainer.innerHTML = view;
}