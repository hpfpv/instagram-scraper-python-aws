const apiEndpoint = 'https://iscacd5zck.execute-api.us-east-1.amazonaws.com/dev/';
// let stories;

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
  this.root.querySelector('#story_video').src = "data/media/" + story.media + ".mp4"
  this.root.querySelector('#story_image').poster = "data/media/" + story.media + ".jpg"
  this.root.querySelector('#story_video').autoplay = true
}
else {
  this.root.querySelector('#story_video').classList.add("d-none")
  this.root.querySelector('#story_image').classList.remove("d-none")
  this.root.querySelector('#story_image').src = "data/media/" + story.media + ".jpg"
}
this.root.querySelector('#story_avatar').style.backgroundImage = `url(data/profile/${story.user}.jpg)`
this.root.querySelector('#story_avatar_big').src = "data/profile/" + story.user + ".jpg"
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
    video.src = "data/media/" + media + ".mp4"
    // video.controls = true;
    video.load();

    video.addEventListener('canplaythrough', function(){
      resolve(video);
    });
    video.addEventListener('error', function(){
      reject(video);
      is_video = false;
    })
  })
  })
  if (is_video == true) {
  await Promise.all(loadVideos);
  } else {
  is_video = false;
  const loadImages = stories.map(({ media }) => {
    return new Promise((resolve, reject) => {
      let img = document.getElementById('story_image');
      img.onload = () => {
        resolve(media)
      }
      img.src = "data/media/" + media + ".jpg" 
    })
  })
  await Promise.all(loadImages);
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
  document.getElementById('work_in_progress').classList.remove('d-none')
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function stop(){
  clearStorage();
  window.location = './index.html';
}

function clearStorage(){
  sessionStorage.clear();
  localStorage.clear();
  worknumber = 0;
}

function reload (){
  sleep(600000).then(() => {
    initStories();
  });
}

function initStories() {
  work_in_progress();
  if (sessionStorage.getItem('account_to_mention')==null){
    var account_to_mention = document.getElementById('account_to_mention').value;
    sessionStorage.setItem('account_to_mention', account_to_mention)
  }else {
    var account_to_mention = sessionStorage.getItem('account_to_mention')
  }
  console.log("Account to mention", account_to_mention);

  // Use this section for testing purposes only
  // sleep(3000).then(() => {
  //   const stor = [
  //     {
  //         "story_id": "2744057125774454818",
  //         "story_time": "16h",
  //         "user": "hpfpv",
  //         "is_video": true,
  //         "story_media_url": "https://scontent-iad3-2.cdninstagram.com/v/t50.12441-16/271439537_757098821916710_8192934091010385844_n.mp4?_nc_ht=scontent-iad3-2.cdninstagram.com&_nc_cat=102&_nc_ohc=PPyhCLQvkBkAX8g5Ryu&edm=AHlfZHwBAAAA&ccb=7-4&oe=61D85ACC&oh=00_AT93zNDzQ9amy4E8rrLACx4lVphiwkiBXtWaILbic47OUg&_nc_sid=21929d",
  //         "media": "2744057125774454818",
  //         "time": 10400
  //     },
  //     {
  //         "story_id": "2744019491559617567",
  //         "story_time": "17h",
  //         "user": "hpfpv",
  //         "is_video": true,
  //         "story_media_url": "https://scontent-iad3-2.cdninstagram.com/v/t50.12441-16/271212401_2995249320727073_3365759509281053303_n.mp4?_nc_ht=scontent-iad3-2.cdninstagram.com&_nc_cat=105&_nc_ohc=ldPeFVY2ER0AX86wsIn&edm=AHlfZHwBAAAA&ccb=7-4&oe=61D7E466&oh=00_AT9M6tSvdjnvka8Bk-UEk_m71M38aGV1Exuyto9KxlVD_A&_nc_sid=21929d",
  //         "media": "2744019491559617567",
  //         "time": 10333
  //     }
  //   ]
  //   const stor_str = JSON.stringify(stor)
  //   sessionStorage.setItem('stories', stor_str)
  //   window.location = './stories.html';
  // });
  var initStoriesApi = apiEndpoint + account_to_mention + '/stories';

  $.ajax({
  url : initStoriesApi,
  type : 'GET',
  success : function(response) {
      requestId = response.requestId;
      console.log("requestId", requestId);
      sleep(100000).then(() => {
        retrieveStories(requestId);
      });
  },
  error : function(response) {
      console.log("An error occured while initiating the request");
      window.location = './error.html';
      sessionStorage.setItem("options_error_text", "An error occured while initiating the request. Please try again later.");
      sessionStorage.setItem("options_error_retry", "initStories();")
  }
  });
}

function retrieveStories(requestId) {
  var retrieveStoriesApi = apiEndpoint + requestId;
  $.ajax({
    url : retrieveStoriesApi,
    async: true,
    type : 'GET',
    success : function(response) {
      if (response.completed == true){
        console.log("stories retrieved successfully from backend")
        if (response.stories == '[]'){
          console.log("no new stories found")
          window.location = './nothing.html';
        } else {
          sessionStorage.setItem('stories', response.stories)
          window.location = './stories.html';
        }
      }else{
        console.log("stories still being proccessed by backend");
        sleep(60000).then(() => {
          retrieveStories(requestId);
        });
      }
    },
    error : function(response) {
      sleep(60000).then(() => {
        retrieveStories(requestId);
      });
      window.location = './error.html';
      sessionStorage.setItem("options_error_text", "An error occured while retrieving stories. Please try again later.");
      sessionStorage.setItem("options_error_retry", "retrieveStories(requestId)")
    }
    });
}

