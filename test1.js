var heatmap;
var points = [];
var running = true;
window.onload = async function() {
    var queryString = decodeURIComponent(window.location.search);
    queryString = queryString.substring(1);
    document.getElementById("myframe").setAttribute("src",queryString);
    var body = document.body;
    var hm = document.querySelector('.heatmap-wrapper');
    var config = {
      container: hm,
      radius: 10,
      maxOpacity: .5,
      minOpacity: 0,
      blur: .75
    };
    heatmap = h337.create(config)
    var trackData = false;

    setInterval(function() {
      trackData = true;
    }, 100);

    var idleTimeout, idleInterval;
    var lastX, lastY;
    var idleCount;
    webgazer.params.showVideoPreview =true;
    await webgazer.setRegression('ridge')
        .setGazeListener(function(data, clock) {
          if(data && trackData && running){
          points.push({
            x : data.x , 
            y : data.y
          });
          trackData = false;
        };
        }).begin();
        webgazer.showPredictionPoints(true);
  };

  function htmp_btn(){
    if(running){
    heatmap.addData(points);
    points = [];
    }
    takeshot();
  };
  function takeshot() { 
    let div = document.getElementById('maincanvas'); 
    const a = document.createElement("a");
    html2canvas(div).then( 
        function (canvas) { 
            document 
            .getElementById('output') 
            .appendChild(canvas);
            document.getElementById("saveBtn").download  = canvas;
        })
};
  function start(){
    running = true;
    webgazer.resume();
  };
  function stop(){
    running = false;
    webgazer.pause();
  };
  window.applyKalmanFilter = true;
  window.saveDataAcrossSessions = true;
