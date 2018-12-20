var particles = [];
var img;  
var tags = [];
var canvas;

function preload() {
  // load image
  img = loadImage("https://preview.ibb.co/m7fWyo/bb_court.png");
  tags = loadImage("https://image.ibb.co/f1cy39/1.png");
  

} 

function setup() {
    canvas = createCanvas(650, 400);
    canvas.parent('sketch-holder');
    //particle = new Particle(300, 300);   
    transformData();
   
}

// function mousePressed() {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
//     particles.push(new Particle(mouseX, mouseY, tags));
//     //var b = new Tagsa(mouseX, mouseY, tags);
//    // particles.push(b);
// }
  
function draw() {
  background(255);
   // Displays the image at its actual size at point (0,0)
   image(img, 0, 0); 
  
   tags.resize(0, 20);

   for (var i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].show();
    
}
   //image(tag4, 0, 0);
 
   //particle.update();
   //particle.show();
  
//     for (var i = 0; i < particles.length; i++) {
   
//        particles[i].update();
//        particles[i].show();
       
//    }
}
//data creation method
function transformData(){
  console.log("dataset:" + a);
  console.log("source: "+ source);
	var pointDataX = source[0][2];
  var pointDataY = source[0][3];
  console.log(source.length);
  console.log("Its just below emppty");
  console.log("x =" + pointDataX);
  console.log("y =" + pointDataY);
  var startTime = 0;//original timestamp to miliseconds)
  var dataset	= [];

  //see/check array of "source"
// var totalArray= source.length;
// for(i=0; i<totalArray; i++){
//   console.log(source[i]);
// }

  //dataset='{{item[0]}}';
  //var someJavaScriptVar = {{item[0]}}';
  
  var tagID =1;
	var previousTS=0;
  //timeD = time difference
  var timeD = 0;
  //var dataset = {{ results|tojson }};
  //var dataset=0;
  
  
  
  for(var y = 0; y<source.length; y++) //rows.length
  {         
    timeD = startTime - previousTS;
    //round(random) is so that no decimal points is added, only whole numbers)
    pointDataX += round(random(-50,100));
    //mapping to smaller canvas
    pointDataX= map(pointDataX, 0,4500, 0,600);
    pointDataY += round(random(-50,100));
    //mapping to smaller canvas
    pointDataY= map(pointDataY, 0,4500, 0,600);
   	var vectorPoint= createVector(pointDataX,pointDataY)
    //for each data point, crea)te a object with timestamp, and x+y)
    var point = {
    'points' : vectorPoint,
    'startTime': startTime,
    'timeD' : timeD,
    'tagID' : tagID
    }
    dataset.push(point);
      
    previousTS= startTime;
    
    //add a random amount of miliseconds that "passed" since last movement
    startTime += round(random(0,50));
    //update the tagID randomly, 1 of 10 tags
    tagID += round(random(0,10));
  }

console.log();
}

  // display image (img, x, y)
