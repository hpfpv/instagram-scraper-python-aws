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
if (is_video == true){
  // this.root.style.background = ''
  // this.root.querySelector('#story_image').classList.add("d-none")
  // this.root.querySelector('#story_video').classList.remove("d-none")
  this.root.querySelector('#story_media').src = "data/media/" + story.media + ".mp4"
  this.root.querySelector('#story_media').poster = "data/media/" + story.media + ".jpg"
  this.root.querySelector('#story_media').autoplay = true
}
else {
  // this.root.querySelector('#story_video').classList.add("d-none")
  // this.root.querySelector('#story_media').classList.remove("d-none")
  this.root.querySelector('#story_media').poster = "data/media/" + story.media + ".jpg"
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
  const loadStories = stories.map((story) => {
    const response = []
    response["story_id"] = story.story_id
    response["story_time"] = story.story_time
    response["user"] = story.user
    response["is_video"] = story.is_video
    response["time"] = story.time
    var video = document.getElementById('story_media');
    if (story.is_video == true){
      response["media"] = new Promise((resolve, reject) => {
        // var video = document.getElementById('story_media');
        // video.autoplay = true;
        video.muted = true;
        video.playsInline = true;
        video.src = "data/media/" + story.media + ".mp4"
        video.controls = false;
        video.load();
        resolve(video);
        // video.addEventListener('canplaythrough', function(){
          
        // });
        // video.addEventListener('error', function(){
        //   reject(video);
        // })
      })
    }else{
      response["media"] = new Promise((resolve, reject) => {
        // let img = document.getElementById('story_media');
        // video.onload = () => {
        //   resolve(story.media)
        // }
        video.playsInline = true;
        video.controls = false;
        video.poster = "data/media/" + story.media + ".jpg" 
        resolve(video);
      })
    }
    return response
      
  })
  await Promise.all(loadStories);

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

  // Use this section for testing purposes only - static data received from backend
  // sleep(5).then(() => {
  //   const stor = [{"story_id": "2745752530074420522", "story_time": "2h", "user": "decouvre.bj", "is_video": false, "story_media_url": "https://scontent-lga3-1.cdninstagram.com/v/t51.2885-15/e35/271468002_6807092292696775_5230543882211352467_n.jpg?_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=QYDNgP6OgvAAX8xA2O1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-NjncxICcjtc6of0LEGMh0mAQ0DdmyDtCQl8CuUHKlLw&oe=61DA5A19&_nc_sid=21929d", "media": "2745752530074420522", "time": 5000}, {"story_id": "2745746206237102229", "story_time": "2h", "user": "decouvre.bj", "is_video": true, "story_media_url": "https://scontent-lga3-1.cdninstagram.com/v/t50.12441-16/271303537_618782479362080_6340909627538600528_n.mp4?_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=108&_nc_ohc=_aWdv1nXuPMAX87G_EP&tn=hCW8RFCdqdwz8MUd&edm=AHlfZHwBAAAA&ccb=7-4&oe=61DA4091&oh=00_AT8zBj-b012sjGfhHVMelqdcKwFySXQPwnhZR-bCJsNumQ&_nc_sid=21929d", "media": "2745746206237102229", "time": 8220.0}, {"story_id": "2745787120598851686", "story_time": "1h", "user": "uneantillaisequelquepart", "is_video": false, "story_media_url": "https://scontent-lga3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/271548749_623922062060156_6502586881374907532_n.jpg?_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=108&_nc_ohc=-B2hQqXrIpMAX_MDoru&tn=hCW8RFCdqdwz8MUd&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9nuXqhAFEdZ8UuuosD5pJeIV5NxnizRGy-zA6-hC89vw&oe=61DA718E&_nc_sid=21929d", "media": "2745787120598851686", "time": 5000}, {"story_id": "2745746518576306857", "story_time": "2h", "user": "sam_b_journey", "is_video": true, "story_media_url": "https://scontent-lga3-1.cdninstagram.com/v/t50.12441-16/271318316_650054186024136_3051851240130752546_n.mp4?_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=100&_nc_ohc=qIugGzRIHN8AX_FE1cf&tn=hCW8RFCdqdwz8MUd&edm=AHlfZHwBAAAA&ccb=7-4&oe=61DA28DA&oh=00_AT9c28romkQwwRq1edGSFhfG86nS2ci3tXGURk7XUKCOBw&_nc_sid=21929d", "media": "2745746518576306857", "time": 5000.0}, {"story_id": "2745763739452556401", "story_time": "2h", "user": "svint.vlexe", "is_video": false, "story_media_url": "https://scontent-lga3-1.cdninstagram.com/v/t51.2885-15/e35/271314811_343121794020321_2652971603330649226_n.webp.jpg?_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=109&_nc_ohc=k_pHLwGh_bwAX83LKa7&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_v6RoNGRD1qn-ePThQ6qYdXYPwEwvsGS509_X5LEG6Pw&oe=61DA3E85&_nc_sid=21929d", "media": "2745763739452556401", "time": 5000}]
  //   const stor_str = JSON.stringify(stor)
  //   sessionStorage.setItem('stories', stor_str)
  //   window.location = './stories.html';
  // });
  // End of test section. comment below lines when testing

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
        console.log("request still being proccessed by backend");
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

