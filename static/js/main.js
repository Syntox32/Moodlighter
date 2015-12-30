
var socket = io.connect("http://" + document.domain + ":" + location.port + "/socket");

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var globalColor = {
	r: 0,
	b: 0,
	g: 0
};

// drawCanvas();

socket.on("sync", function(msg) {
	setColorSettings(msg.color);
});

socket.on("on_connect", function(msg) {
	var e = document.getElementById("status");
	e.innerHTML = msg.data;
	// console.log(msg.color);
	setColorSettings(msg.color);
});

function setColorSettings(msg) {
	var c = msg.split(":");
	
	globalColor.r = c[1];
	globalColor.g = c[3];
	globalColor.b = c[5];
	
	document.getElementById("red-number").value = globalColor.r;
	document.getElementById("red-slider").value = globalColor.r;
	document.getElementById("grn-number").value = globalColor.g;
	document.getElementById("grn-slider").value = globalColor.g;
	document.getElementById("blu-number").value = globalColor.b;
	document.getElementById("blu-slider").value = globalColor.b;
	
	drawCanvas();
}


function sliderChanged(event, color) {
	var val = event.target.value;
	document.getElementById(color + "-number").value = val;
	socket.emit("color change", { data: color + ":" + val.toString() });

	switch(color) {
		case "red": globalColor.r = val; break;
		case "grn": globalColor.g = val; break;
		case "blu": globalColor.b = val; break;
	}

	drawCanvas();
}

function numberChanged(event, color) {
	var val = event.target.value;
	document.getElementById(color + "-slider").value = val;
	socket.emit("color change", { data: color + ":" + val.toString() });

	switch(color) {
		case "red": globalColor.r = val; break;
		case "grn": globalColor.g = val; break;
		case "blu": globalColor.b = val; break;
	}

	drawCanvas();
}

function drawCanvas() {
	var colorStr = "rgb(" 
		+ globalColor.r.toString() + ","
		+ globalColor.g.toString() + ","
		+ globalColor.b.toString() + ")";
	ctx.fillStyle = colorStr;
	var wi = parseInt(canvas.offsetWidth);
	var hi = parseInt(canvas.offsetHeight);
	// ctx.clearRect(0,0, wi, hi);
	ctx.fillRect(0, 0, wi, hi);
}
