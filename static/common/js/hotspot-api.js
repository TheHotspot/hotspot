// Async ajax library for accessing the Hotspot API

var api = {
    version: '2',
    base_url: "/api/",
}
api.getHotspots = function(func) {
    if (typeof(func)==='undefined') func = function(x) {console.log(x);};
    request = $.ajax({
        url: api.base_url+"v2/hotspots",
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(func);
}

api.getCurrentHotspot = function(lat, lng, func) {
    if (typeof(func)==='undefined') func = function(x) {console.log(x);};
    request = $.ajax({
        url: api.base_url+"v2/locate?lat="+lat+"&lng="+lng,
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(function(data){
        if (data.status == "SUCCESS") {
            func(data.hotspot);
        }
        else {
            console.log("Not called due to ajax error: ", func);
            console.log(data);
        }
    });
}

api.getHotspotsByRadius = function(lat, lng, rad, func) {
    if (typeof(func)==='undefined') func = function(x) {console.log(x);};
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

api.getHotspotDetails = function(hotspot_id, func) {
    if (typeof(func)==='undefined') func = function(x) {console.log(x);};
    request = $.ajax({
        url: api.base_url+"hotspot?id="+hotspot_id,
        beforeSend: function(xhr) {
            xhr.overrideMimeType("application/json");
        }
    });
    request.done(function(data){
        if (data.status == "SUCCESS") {
            func(data.hotspot);
        }
        else {
            console.log("Not called due to ajax error: ", func);
            console.log(data);
        }
    });
}


// Examples
//
//print = function(x) {console.log(x)}
//
//api.setCheckIn(13, print);
//api.getHotspotsByRadius(45, -122, 100, print);
//api.getHotspotDetails(13, print);
