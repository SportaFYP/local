// Where is the circle
var x, y;
var pVector = [];
//var pVector2=[];
var particles = [];
var historyPoints = [];
var count = 0;
var timePrev;
var once = true;
var playMS;
var playTime;
var currentMS;
var totalMS;
var percentageTime = 0;
var startPlay = false;
var begin;
var end;
var distanceDataPoints = [];
var overlayTimeGraphs = [];
var playerTimeInOverlayGraphs = [];
var canvasWidth, canvasHeight;
var pozyxWidth = 7770;
var pozyxHeight = 6000;

function setup() {
  // createCanvas(400, 400);
  var canvas = createCanvas($('#sketch-holder').width(), ($('#sketch-holder').width() / 16 * 9));
  bg = loadImage("static/points/bbcourt.png");
  canvas.parent('sketch-holder')
  prepareData();
  //creates tags
  console.log("tagDS:" + JSON.stringify(tagDS))


  for (var a = 0; a < tagDS.length; a++) {
    var tag = tagDS[a];
    var p1 = new Particle(tag[7], tag[5], tag[6], tag[3]);//tagID
    p1.interpolateFunctionX.interp1d([], []);
    p1.interpolateFunctionY.interp1d([], []);
    particles.push(p1);
  }
  // var p1 = new Particle(28261);
  // p1.interpolateFunctionX.interp1d([], []);
  // p1.interpolateFunctionY.interp1d([], []);
  // particles.push(p1);


  //particles.push(p2);
  console.log(percentageTime);
  //set up
  for (var i = 0; i < pVector.length; i++) {
    console.log("point tagID:" + pVector[i].tagID);
    for (var j = 0; j < particles.length; j++) {
      console.log("particle tagID:" + particles[j].tagID);
      if (particles[j].tagID == pVector[i].tagID) {
        //get tag and push point into the x=f(time)    
        //also need to do mapping for the coordinates
        console.log("pushing data into function x= f(time), index: " + i);
        //x=f(time) -- where _x is time, _y is datapoint
        particles[j].interpolateFunctionX._x.push(pVector[i].point.z);
        particles[j].interpolateFunctionX._y.push(pVector[i].point.x);
        console.log("pushing data into function y= f(time)");
        //y=f(time) -- where _x is time, _y is datapoint
        particles[j].interpolateFunctionY._x.push(pVector[i].point.z);
        particles[j].interpolateFunctionY._y.push(pVector[i].point.y);
      }
    }
  }
  totalMS = pVector[pVector.length - 1].point.z;

  for (var i = 0; i < overlayJSON.length; i++) {
    overlays.push(new Overlay(overlayJSON[i].name, overlayJSON[i].xorig, overlayJSON[i].yorig, overlayJSON[i].width, overlayJSON[i].height, overlayJSON[i].color))
  }

  for (var i = 0; i < overlays.length; i++) {
    row = "<td><input type=\"checkbox\" onchange=\"overlays[" + i + "].isVisible = this.checked\" checked>" + overlays[i].name + "</td>"
    $('.overlayRow:nth-child(' + (Math.floor(i / 5) + 1) + ')').append(row)

    if ((i % 4) == 0 && i != 0) {
      $('#overlayList').append('<tr class="overlayRow"></tr>')
    }
  }

  for (var i = 0; i < 14; i++) {
    for (var j = 0; j < tagDS.length; j++) {
      if ((i + 1) == tagDS[j][6]) {
        $('#player' + (i + 1)).append(tagDS[j][5])
        break
      }
    }
  }

  for (var k = 0; k < particles.length; k++) {

    if (particles[k].playerNumber >= 0 && particles[k].playerNumber < 8) {
      distanceDataPoints.push({ label: particles[k].playerNumber + " - " + particles[k].name, y: (particles[k].getTotalDistanceWalked() / 1000), color: "#0000ff" })
    }
    if (particles[k].playerNumber >= 8 && particles[k].playerNumber < 15) {
      distanceDataPoints.push({ label: particles[k].playerNumber + " - " + particles[k].name, y: (particles[k].getTotalDistanceWalked() / 1000), color: "#663300" })
    }

    var timeDataPoints = [];
    secondsNotInOverlay = totalMS

    for (var l = 0; l < overlays.length; l++) {
      counter = 0;
      for (var m = 0; m < totalMS; m++) {
        if (overlays[l].isPlayerInOverlay(particles[k].interpolateFunctionX._f(m), particles[k].interpolateFunctionY._f(m), pozyxWidth, pozyxHeight)) {
          counter++;
        }
      }
      if (counter != 0) {
        secondsNotInOverlay -= counter;
        timeDataPoints.push({ label: overlays[l].name, y: (counter / 1000), color: rgbToHex(overlays[l].color) });
        if (particles[k].playerNumber >= 0 && particles[k].playerNumber < 8) {
          overlays[l].addPlayerIntoOverlayArray(particles[k], counter, "#0000ff")
        }
        if (particles[k].playerNumber >= 8 && particles[k].playerNumber < 15) {
          overlays[l].addPlayerIntoOverlayArray(particles[k], counter, "#663300")
        }
      }
    }

    timeDataPoints.push({ label: "Not in any overlay", y: (secondsNotInOverlay / 1000), color: "#888888" });

    var playerTime = {
      theme: "light2",
      animationEnabled: true,
      title: {
        text: "Time spent in overlay for " + particles[k].name
      },
      data: [
        {
          type: "doughnut",
          startAngle: 0,
          showInLegend: true,
          toolTipContent: "{label} - {y}(#percent %)",
          yValueFormatString: "######0.###s",
          legendText: "{label}",
          indexLabel: "{label} - {y}",
          dataPoints: timeDataPoints
        }
      ]
    };

    overlayTimeGraphs.push(playerTime);

    option = document.createElement("option");
    option.text = particles[k].name;

    document.getElementById("selectPlayer").add(option);
  }

  var distance = {
    animationEnabled: true,

    title: {
      text: "Distance walked by players",
      fontFamily: "Arial"
    },
    axisX: {
      interval: 1
    },
    axisY2: {
      interlacedColor: "rgba(1,77,101,.2)",
      gridColor: "rgba(1,77,101,.1)",
      title: "Distance walked (m)"
    },
    data: [{
      type: "bar",
      name: "players",
      axisYType: "secondary",
      dataPoints: distanceDataPoints
    }]
  };

  for (var l = 0; l < overlays.length; l++) {
    if (overlays[l].playerTimeInOverlay.length != 0) {
      var playerTimeInOverlay = {
        animationEnabled: true,

        title: {
          text: "Total time players spent in " + overlays[l].name,
          fontFamily: "Arial"
        },
        axisX: {
          interval: 1
        },
        axisY2: {
          interlacedColor: "rgba(1,77,101,.2)",
          gridColor: "rgba(1,77,101,.1)",
          title: "Distance walked (m)"
        },
        data: [{
          type: "bar",
          name: "players",
          axisYType: "secondary",
          yValueFormatString: "######0.###s",
          dataPoints: overlays[l].playerTimeInOverlay
        }]
      };


      playerTimeInOverlayGraphs.push(playerTimeInOverlay)

      option = document.createElement("option");
      option.text = overlays[l].name;

      document.getElementById("selectOverlay").add(option);
    }
  }

  if (document.getElementById('selectOverlay').length == 0) {
    option = document.createElement("option");
    option.text = "There is no overlays drawn for this match";

    document.getElementById("selectOverlay").add(option);
  }

  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    if ($(e.target).attr("href") == "#statistics") {
      distanceGraph = new CanvasJS.Chart("distanceGraph", distance);
      particleTimeGraph = new CanvasJS.Chart("particleTimeGraph", overlayTimeGraphs[document.getElementById("selectPlayer").selectedIndex]);
      playerTimeInOverlayGraph = new CanvasJS.Chart("playerTimeInOverlayGraph", playerTimeInOverlayGraphs[document.getElementById("selectOverlay").selectedIndex]);
      distanceGraph.render();
      particleTimeGraph.render();
      playerTimeInOverlayGraph.render();
      $("#court").css("top", particleTimeGraph.height)
      //$("#selectOverlay").css("top", particleTimeGraph.height)
      //$("#playerTimeInOverlayGraph").css("top", selectOverlay.height)
    } else {
      distanceGraph.destroy();
      particleTimeGraph.destroy();
      playerTimeInOverlayGraph.render();
    }
  });
}
function play() {
  //check the percentage of the seek bar * total time -> playMS
  //set as zero for now
  console.log("percentageTime: " + percentageTime);
  console.log("totalMS: " + totalMS);
  playMS = totalMS * percentageTime;
  playTime = new Date();
  console.log("before play starts");
  begin = new Date();
  loop();
}
function pause() {
  noLoop()
}


function update() {
  var currentTime = new Date();
  currentMS = (currentTime - playTime) + playMS;

  if (isNaN(currentMS))
    currentMS = 0;

  //console.log("playMS: " + playMS);
  //console.log("currentMS:" + currentMS);

  for (var a = 0; a < particles.length; a++) {
    var xPoint = particles[a].interpolateFunctionX._f(currentMS);
    // console.log("xPoint: "+ xPoint);
    var yPoint = particles[a].interpolateFunctionY._f(currentMS);
    //console.log("xPoint: "+ yPoint);
    var lerpPoint = createVector(xPoint, yPoint);
    if (currentMS <= totalMS || startPlay == false) {
      if (!(xPoint == 0 && yPoint == 0)) {
        particles[a].update(lerpPoint, currentMS)//which will add to history etc
      }
    } else {
      end = new Date();
      console.log("Total Time taken:" + (end - begin));
      noLoop();
    }
    if (particles[a].history.length != 0) {
      particles[a].show();
    }
  }
}

function draw() {
  // background(bg);
  background(bg);
  //if(startPlay)
  //{

  for (var i = 0; i < overlays.length; i++) {
    if (overlays[i].isVisible) {
      overlays[i].draw(canvasWidth, canvasHeight);
    }
  }

  update();
  //}
}

function prepareData() {
  //tagId,timestamp,coordinates_x,coordinates_y
  // var p1 = new Particle(1);
  // var p2 = new Particle(2);
  var startTime = pointsDS[0][1];
  for (var i = 0; i < pointsDS.length; i++) {

    var x = pointsDS[i][2];
    var y = pointsDS[i][3];
    var elapsed = (pointsDS[i][1] - startTime) * 1000; // to make it Miliseconds
    var point = createVector(x, y, elapsed);
    pVector.push({ 'point': point, 'tagID': pointsDS[i][0] });

  }
}

function clearHistory() {
  for (var i = 0; i < particles.length; i++) {
    particles[i].clearHistory();
  }
}