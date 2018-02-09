

function request (url) {
  return new Promise(function (resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        resolve(xhr.response);
      } else {
        reject({
          status: this.status,
          statusText: xhr.statusText
        });
      }
    };
    xhr.onerror = function () {
      reject({
        status: this.status,
        statusText: xhr.statusText
      });
    };
    xhr.send();
  });
}

function search(){
    //Get query string from text input
    var query = document.getElementById("search-field").value;
    var url = "/search?q="+query;
    console.log('Search Query : '+query);
    //Run Asynchronous XHR
    Promise.resolve(request(url))
    .then(function (res) {
        json = JSON.parse(res);
        console.log(json);
        if (json.hashtags != undefined)
            wordcloud(json.hashtags, 15, 100, 10);
        if (json.places != undefined){
            draw_hist(json.places);
        }
    })
    .catch(function (err) {
        console.error('XHR ERROR : ', err);
    });
}

//Load svg world map
window.onload = function(){
    var url = "/static/world_map2.svg";
    console.log('load '+url);
    //Run Asynchronous XHR
    Promise.resolve(request(url))
    .then(function (res) {
        res.className += 'worldMap'
        map = document.getElementById('map');
        map.innerHTML = res;
    })
    .catch(function (err) {
        console.error('XHR LOAD ERROR : ', err);
    });
}
