// Async ajax library for accessing the Hotspot API

var api = {
    version: 'v2',
    devices: [],
    base_url: "/api/",
    hotspots: []
}

api.getHotspots = function(func) {
    request = $.ajax({
        url: api.base_url+"/v2/hotspots",
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(func);
}

api.getHotspotsByRadius = function(lat, lng, rad, func) {
    request = $.ajax({
        url: api.base_url+"search?lat="+lat+"&lng="+lng+"&distance="+rad,
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(function(data){
        if (data.status == "SUCCESS") {
            func(data.results);
        }
        else {
            console.log("Not called due to ajax error: ", func);
            console.log(data);
        }
    });
}

api.setCheckIn = function(hotspot_id, func) {
    if (typeof(func)==='undefined') func = function(x) {console.log(x);};
    request = $.ajax({
        url: api.base_url+"scan?id="+hotspot_id,
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(function(data){
        if (data.status == "SUCCESS") {
            func(data.scan_id);
        }
        else {
            console.log("Not called due to ajax error: ", func);
            console.log(data);
        }
    });
}

api.setCheckIn(13);

//api.getHotspots(function(x) {console.log(x)});
api.getHotspotsByRadius(45, -122, 100,function(x) {console.log(x)});


// function getHotspotsByRadius()

// function getHotspotDetails()

// function setCheckedIn()

// function 
