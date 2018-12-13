// Where is the circle
var x, y;
var pVector=[];
//var pVector2=[];
var particles = [];
var historyPoints=[];
var count = 0;
var timePrev;
var once = true;
var playMS;
var playTime;
var totalMS;
var percentageTime = 0;
var startPlay= false;
var begin;
var end;

function setup() {
  // createCanvas(400, 400);
  var canvas = createCanvas(700, 540);
  bg = loadImage("static/points/bbcourt1.png");
  canvas.parent('sketch-holder')
  prepareData();
  //createData();
  //creates tags
  console.log("tagDS:" + JSON.stringify(tagDS))


  for(var a = 0; a <tagDS.length; a++)
  {
    var tag = tagDS[a];
    var p1 = new Particle(tag[4],tag[3],a,tag[2] );//tagID
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
  for(var i = 0; i < pVector.length; i++){
    console.log("point tagID:"+pVector[i].tagID);
    for(var j = 0; j<particles.length;j++)
    {
      console.log("particle tagID:"+particles[j].tagID);
      if(particles[j].tagID ==pVector[i].tagID){
      //get tag and push point into the x=f(time)    
      //also need to do mapping for the coordinates
      console.log("pushing data into function x= f(time), index: "+i);
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
  noLoop();
  totalMS = pVector[pVector.length-1].point.z;
  console.log("totalMS:" +totalMS);
  console.log("functionX Array of time: ");
  console.log(p1.interpolateFunctionX._x)

  //play();
}
function play(){
//check the percentage of the seek bar * total time -> playMS
//set as zero for now
console.log("percentageTime: "+ percentageTime);
console.log("totalMS: "+ totalMS);
playMS = totalMS * percentageTime;
playTime = new Date();
console.log("before play starts");
begin = new Date();
loop();
}
function pause(){
  noLoop()  
  }


function update(){
  var currentTime = new Date();
  var currentMS = (currentTime - playTime)+playMS;
  //console.clear();
  console.log("playMS: "+playMS);
  console.log("currentMS:" + currentMS);
  
    for(var a = 0; a<particles.length;a++)
    { 
      var xPoint = particles[a].interpolateFunctionX._f(currentMS);
     // console.log("xPoint: "+ xPoint);
      var yPoint = particles[a].interpolateFunctionY._f(currentMS);
      //console.log("xPoint: "+ yPoint);
      var lerpPoint = createVector(xPoint,yPoint);
      if(currentMS<=totalMS || startPlay == false){
      particles[a].update(lerpPoint)//which will add to history etc
      }else{
        end = new Date();
        console.log("Total Time taken:"+(end-begin));
        noLoop();
      }
      particles[a].show();	
    }
}

function draw() {
  // background(bg);
  background(bg);
  //if(startPlay)
  //{
    update();
  //}
}

function prepareData(){
  //tagId,timestamp,coordinates_x,coordinates_y
  // var p1 = new Particle(1);
  // var p2 = new Particle(2);
  var startTime = pointsDS[0][1];
for(var i = 0; i< pointsDS.length; i++){

    var x = pointsDS[i][2];
    var y = pointsDS[i][3];
    var elapsed = (pointsDS[i][1] - startTime) * 1000; // to make it Miliseconds
    var point = createVector(x, y, elapsed);
    pVector.push({'point': point, 'tagID': pointsDS[i][0]});
 
}
}




function createData(){
  x = width / 2;
  y = height/ 2;
  console.log("height and width of first point:");
  console.log(x);
  console.log(y);
  var x1 = createVector(x, y, 0);
  var x2 = createVector(x + 10, y + 10, 200);
  var x3 = createVector(x - 20, y + 5, 500);
  var x4 = createVector(x - 30, y - 30, 800);
  var x5 = createVector(x + 20, y + 5, 900);
  var x6 = createVector(x + 25, y - 15, 1100);
  var x7 = createVector(x - 30, y - 30, 1600);
  var x8 = createVector(x - 20, y - 30, 2100);
  var x9 = createVector(x - 20, y - 30, 2300);
  var x10 = createVector(x - 20, y - 30, 2500);
  var x11 = createVector(x - 20, y - 30, 2700);
  var x12 = createVector(x - 20, y - 30, 2780);
  var x13 = createVector(x - 20, y - 30, 2860);
  var x14 = createVector(x - 20, y - 30, 2960);
  var x15 = createVector(x - 20, y - 30, 3200);
  var x16 = createVector(x - 20, y - 30, 3300);
  var x17 = createVector(x - 20, y - 30, 3650);
  var x18 = createVector(x - 20, y - 30, 3800);
  var x19 = createVector(x - 20, y - 30, 3900);
  var x20 = createVector(x + 200, y + 200, 24000);

  pVector.push({'point': x1, 'tagID': 1});
  pVector.push({'point': x2, 'tagID': 1});
  pVector.push({'point': x3, 'tagID': 1});
  pVector.push({'point': x4, 'tagID': 1});
  pVector.push({'point': x5, 'tagID': 1});
  pVector.push({'point': x6, 'tagID': 1});
  pVector.push({'point': x7, 'tagID': 1});
  pVector.push({'point': x8, 'tagID': 1});
  pVector.push({'point': x9, 'tagID': 1});
  pVector.push({'point': x10, 'tagID': 1});
  pVector.push({'point': x12, 'tagID': 1});
  pVector.push({'point': x13, 'tagID': 1});
  pVector.push({'point': x14, 'tagID': 1});
  pVector.push({'point': x15, 'tagID': 1});
  pVector.push({'point': x16, 'tagID': 1});
  pVector.push({'point': x17, 'tagID': 1});
  pVector.push({'point': x18, 'tagID': 1});
  pVector.push({'point': x19, 'tagID': 1});
  pVector.push({'point': x20, 'tagID': 1});


  var sx = width / 3;
  var sy = height /3;
  var x1 = createVector(sx, sy, 0);
  var x2 = createVector(sx + 10, sy + 10, 400);
  var x3 = createVector(sx - 20, sy + 5, 900);
  var x4 = createVector(sx - 30, sy - 30, 1300);
  var x5 = createVector(sx + 20, sy + 5, 1500);
  var x6 = createVector(sx + 25, sy - 15, 1700);
  var x7 = createVector(sx - 30, sy - 30, 1800);
  var x8 = createVector(sx - 20, sy - 30, 2000);
  var x9 = createVector(sx - 20, sy - 30, 2500);
  var x10 = createVector(sx - 20, sy - 30, 2600);
  var x11 = createVector(sx - 20, sy - 30, 2700);
  var x12 = createVector(sx - 20, sy - 30, 2780);
  var x13 = createVector(sx - 20, sy - 30, 2860);
  var x14 = createVector(sx - 20, sy - 30, 2960);
  var x15 = createVector(sx - 20, sy - 30, 3200);
  var x16 = createVector(sx - 20, sy - 30, 3300);
  var x17 = createVector(sx - 20, sy - 30, 3650);
  var x18 = createVector(sx - 20, sy - 30, 3800);
  var x19 = createVector(sx - 20, sy - 30, 3900);
  var x20 = createVector(sx + 200, sy + 200, 24000);
  pVector.push({'point': x1, 'tagID': 2});
  pVector.push({'point': x2, 'tagID': 2});
  pVector.push({'point': x3, 'tagID': 2});
  pVector.push({'point': x4, 'tagID': 2});
  pVector.push({'point': x5, 'tagID': 2});
  pVector.push({'point': x6, 'tagID': 2});
  pVector.push({'point': x7, 'tagID': 2});
  pVector.push({'point': x8, 'tagID': 2});
  pVector.push({'point': x9, 'tagID': 2});
  pVector.push({'point': x10, 'tagID': 2});
  pVector.push({'point': x12, 'tagID': 2});
  pVector.push({'point': x13, 'tagID': 2});
  pVector.push({'point': x14, 'tagID': 2});
  pVector.push({'point': x15, 'tagID': 2});
  pVector.push({'point': x16, 'tagID': 2});
  pVector.push({'point': x17, 'tagID': 2});
  pVector.push({'point': x18, 'tagID': 2});
  pVector.push({'point': x19, 'tagID': 2});
  pVector.push({'point': x20, 'tagID': 2});
  print(pVector);

  // console.log('Start x: '+lerp(pVector[count].x, pVector[count+1].x, 0.002));
  // console.log('Start y: '+lerp(pVector[count].y, pVector[count+1].y, 0.002));

}

