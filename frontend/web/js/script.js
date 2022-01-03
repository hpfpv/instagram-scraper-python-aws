const apiEndpoint = 'https://iscacd5zck.execute-api.us-east-1.amazonaws.com/dev/';
let stories;
let workumber = 0;

const story_container = document.querySelector('.display_all')
const nextButton = document.querySelector('#next')
const backButton = document.querySelector('#back')

function Storyfier(storiesArray, rootEl) {
this.stories = storiesArray
this.root = rootEl
this.times = rootEl.querySelector('#times')
this.currentTime = 0
this.currentIndex = 0

// create breakpoints for when the slides should change
this.intervals = this.stories.map((story, index) => {
// TODO change so that it just uses the previous value + current time
let sum = 0
for (let i = 0; i < index; i++){
  sum += this.stories[i].time
}
return sum
})

// necessary to make sure the last slide plays to completion
this.maxTime = this.intervals[this.intervals.length - 1] + this.stories[this.stories.length - 1].time

// render progress bars
this.progressBars = this.stories.map(() => {
const el = document.createElement('div')
el.classList.add('time-item')
el.innerHTML = '<div style="width: 0%"></div>'
return el
})

this.progressBars.forEach((el) => {
this.times.appendChild(el)
})

// methods
this.render = () => {
const story = this.stories[this.currentIndex]
var is_video = story.is_video;
if (is_video){
  // this.root.style.background = ''
  this.root.querySelector('#story_image').classList.add("d-none")
  this.root.querySelector('#story_video').classList.remove("d-none")
  this.root.querySelector('#story_video').src = "media/" + story.media + ".mp4"
  this.root.querySelector('#story_image').poster = "media/" + story.media + ".jpg"
  this.root.querySelector('#story_video').autoplay = true
}
else {
  this.root.querySelector('#story_video').classList.add("d-none")
  this.root.querySelector('#story_image').classList.remove("d-none")
  this.root.querySelector('#story_image').src = "media/" + story.media + ".jpg"
}
this.root.querySelector('#story_avatar').style.backgroundImage = `url(profile/${story.user}.jpg)`
this.root.querySelector('#story_avatar_big').src = "profile/" + story.user + ".jpg"
this.root.querySelector('#story_time').innerHTML = story.story_time
this.root.querySelector('#story_user').innerHTML = story.user
}

this.updateProgress = () => {
this.progressBars.map((bar, index) => {
  // Fill already passed bars
  if (this.currentIndex > index) {
    bar.querySelector('div').style.width = '100%'
    return
  }

  if (this.currentIndex < index) {
    bar.querySelector('div').style.width = '0%'
    return
  }

  // update progress of current bar
  if (this.currentIndex == index) {
    const timeStart = this.intervals[this.currentIndex]

    let timeEnd;
    if (this.currentIndex == this.stories.length - 1){
      timeEnd = this.maxTime
    } else {
      timeEnd = this.intervals[this.currentIndex + 1]
    }

    const animatable = bar.querySelector('div')
    animatable.style.width = `${((this.currentTime - timeStart)/(timeEnd - timeStart))*100}%`


  }
})
}
}

Storyfier.prototype.start = function(){
// Render initial state
this.render()

// START INTERVAL
const test = setInterval(() => {
this.currentTime += 10
this.updateProgress()

if (this.currentIndex >= this.stories.length - 1 && (this.currentTime > this.maxTime)){
  clearInterval(test)
  return
}

const lastIndex = this.currentIndex
if (this.currentTime >= this.intervals[this.currentIndex + 1]){
  this.currentIndex += 1
}

if (this.currentIndex != lastIndex) {
  this.render()
}
}, 10)
}

Storyfier.prototype.next = function(){
const next = this.currentIndex + 1
if (next > this.stories.length - 1){
return
}

this.currentIndex = next
this.currentTime = this.intervals[this.currentIndex]
this.render()
}

Storyfier.prototype.back = function(){
if ((this.currentTime > (this.intervals[this.currentIndex] + 350)) || this.currentIndex === 0){
this.currentTime = this.intervals[this.currentIndex]
return
}

this.currentIndex -= 1
this.currentTime = this.intervals[this.currentIndex]
this.render()
}

const setup = async () => {
  is_video = true;
  const loadVideos = stories.map(({ media }) => {
  return new Promise((resolve, reject) => {
    var video = document.getElementById('story_video');
    // video.autoplay = true;
    // video.muted = true;
    video.playsInline = true;
    video.src = "media/" + media + ".mp4"
    // video.controls = true;
    video.load();

    video.addEventListener('canplaythrough', function(){
      resolve(video);
      console.log(is_video)
    });
    video.addEventListener('error', function(){
      reject(video);
      is_video = false;
      // console.log(is_video)
    })
  })
  })
  if (is_video == true) {
  // await Promise.all(loadVideos);
  } else {
  is_video = false
  const loadImages = stories.map(({ media }) => {
    return new Promise((resolve, reject) => {
      let img = document.getElementById('story_image');
      img.onload = () => {
        resolve(media)
      }
      img.src = "media/" + media + ".jpg" 
    })
  })
  // await Promise.all(loadImages)
  }

  const s = new Storyfier(stories, story_container);
  s.start()

  nextButton.addEventListener('click', () => {
  s.next()
  })

  backButton.addEventListener('click', () => {
  s.back()
  })
}

function work_in_progress() {
  document.getElementById('option_init_work_in_progress').classList.remove('d-none')
  document.getElementById('option_init_form').classList.add('d-none');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function stop(){
  sessionStorage.clear();
  window.location = './index.html';
}

function initStories() {
  if (sessionStorage.getItem('account_to_mention')==null){
    var account_to_mention = document.getElementById('account_to_mention').value;
    sessionStorage.setItem('account_to_mention', account_to_mention)
  }else {
    var account_to_mention = sessionStorage.getItem('account_to_mention')
  }
  console.log("Account to mention", account_to_mention);
  
  var initStoriesApi = apiEndpoint + account_to_mention + '/stories';

  $.ajax({
  url : initStoriesApi,
  type : 'GET',
  success : function(response) {
      // if (response.statusCode == '202'){
      requestId = response.requestId;
      console.log("requestId", requestId);
      if (workumber = 0){
        work_in_progress();
        workumber +=1;
      }
      sleep(60000).then(() => {
        retrieveStories(requestId);
      });
      
      // } else {
      //   window.location = './nothing.html';
      // }
  },
  error : function(response) {
      // window.location = './error.html';
      console.log("An error occured while initiating the request");
  }
  });
}


function retrieveStories(requestId) {
  var retrieveStoriesApi = apiEndpoint + requestId;
  $.ajax({
  url : retrieveStoriesApi,
  type : 'GET',
  success : function(response) {
      if (response.stories == '[]'){
        window.location = './nothing.html';
      } else {
        stories = response.stories;
        console.log(stories);
        window.location = './stories.html';
        setup();
      }
  },
  error : function(response) {
      // window.location = './error.html';
      console.log("An error occured while retriving stories");
  }
  });
}

