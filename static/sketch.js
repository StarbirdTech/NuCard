
//creates date/time as empty strings
let currentDate = ""
let currentTime = ""

//defines post request, dosent do anything to the server
let url = '/checkin';
let lastName = '';

let d,h,m;

let pollTime = 100
let swipeTimeout = 5000

class Student{
  constructor(name){
    this.name = name
    this.hasArrived = false
    this.late = false
    this.early = false
  }
}

let students = []
//loads attendance file, we should have a seperate file for each day
function preload() {  
  attd = loadJSON('/static/Attendance.json', initStudents);
}

function initStudents()
{
   for(i = 0; i < attd['students'].length;i++)
  {
    students.push(new Student(attd['students'][i]['student']))
  }
  print(students)
}

function setup() {
  lastName = '';

  createCanvas(1200, 1500);
  background(242,93,146);

  //IdentityTheft = loadSound('Its Not a Joke.mp3')
    
  setTimeout(refreshJson,pollTime)
};

function draw() {

}

//reloads json file and preforms callback to updateattd function

function refreshJson()
{
  url = getURL()
  try{
    attd = loadJSON('static/Attendance.json', updateAttd)
    httpGet(url + "/checkin", "text", checkIn)
  }
  catch(error)
  {
    console.log(error)
  }
  
  setTimeout(refreshJson,pollTime)
  
}

let tempName=''

//this is basically our draw loop
function updateAttd(){
  background(242,93,146)
  fill(0);
  strokeWeight(4);
  textSize(24);
  
  offset = 40
  for(i = 0; i < students.length;i++)
  {
   text(students[i].name,40, 50 + i * offset)
   
   if(students[i].hasArrived)
    {
    fill(0,255,0)
    }
   else{
    fill(255,0,0)
    }
    
   rectMode(CENTER)
   rect(400, 40 + i * offset,300,20)
   fill(0)

    if(lastName == students[i].name){
      tempName = students[i].name
    }
    if(tempName !=''){
      text('Welcome, ' + tempName, 700,200)
    }

   //text(attd['students'][i]['time'],270, 50 + i * offset)

  }
  
}

let checkInTimeout = false;
function checkIn(data)
{
    //called once, when the idcard tapped is a new id card
    
    lastName = data

    //check current time compared to day start time
    time()
    
    for(i = 0; i<students.length ;i++)
    {
        if (lastName == students[i].name)
        {
          if(!checkInTimeout)
          {
            checkInTimeout=true
            students[i].hasArrived = !students[i].hasArrived //toggle
            setTimeout(changeBox, swipeTimeout)
          }
        }
    }
    
    if(h<9){
      //early
    }
    else{
      //late
    }
    
    //console.log(lastName)
    //console.log(h + ":" + m)

}

function changeBox()
{
  checkInTimeout=false
  tempName = ''
}

var idScan = 0
let Identitytheft
var sound = 0

function time(){
  d = day();
  h = hour();
  m = minute();

}

