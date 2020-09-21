let CRS = L.CRS.EPSG4326
let optimalTileSize = L.point(430, 280)

var map = L.map('map', {
    zoom: 10,
    fullscreenControl: true,
    zoomControl: false,
});

var sidebar = L.control.sidebar({
    autopan: false,       // whether to maintain the centered map point when opening the sidebar
    closeButton: true,    // whether t add a close button to the panes
    container: 'sidebar', // the DOM container or #ID of a predefined sidebar container that should be used
    position: 'left',     // left or right
}).addTo(map);

sidebar.open('home');

L.control.zoom({
    position: 'bottomleft'
}).addTo(map);

var timeDimension = new L.TimeDimension({
    timeInterval: `${year}-01-01/${year}-12-31`,
    period: "P1D",
});

map.timeDimension = timeDimension;

var player = new L.TimeDimension.Player({
    transitionTime: 100,
    loop: false,
    startOver: true
}, timeDimension);

var timeDimensionControlOptions = {
    player: player,
    timeDimension: timeDimension,
    position: 'topleft',
    autoPlay: false,
    minSpeed: 1,
    speedStep: 0.5,
    maxSpeed: 15,
    timeSliderDragUpdate: true,
    playButton: false,
    speedSlider: false
};

var timeDimensionControl = new L.Control.TimeDimension(timeDimensionControlOptions);
map.addControl(timeDimensionControl);

var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

OpenStreetMap_Mapnik.addTo(map);

let asrc_attribution = '<a href="https://asrc.gc.cuny.edu/environment/">CUNY ASRC ESI</a>'

var wmsUrl = "http://10.16.12.61:9999/geoserver/news/wms"
var wmsDischarge = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    tileSize: optimalTileSize,
    crs: CRS,
    layers: `news:${slug}_Discharge_Daily_${year}`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution
});

// Create and add a TimeDimension Layer to the map
var tdWmsDischarge = L.timeDimension.layer.wms(wmsDischarge);

var wmsRunoff = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    crs: CRS,
    tileSize: optimalTileSize,
    layers: `news:${slug}_Runoff_Daily_${year}`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution
});

// Create and add a TimeDimension Layer to the map
var tdWmsRunoff = L.timeDimension.layer.wms(wmsRunoff);

var wmsWatertemp = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    crs: CRS,
    tileSize: optimalTileSize,
    layers: `news:${slug}_qxt_watertemp_Daily_${year}`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution
});

// Create and add a TimeDimension Layer to the map
var tdWmsWatertemp = L.timeDimension.layer.wms(wmsWatertemp);

// Default layer
tdWmsDischarge.addTo(map);

var baseMaps = {
    "Discharge": tdWmsDischarge,
    "Runoff": tdWmsRunoff,
    "QxT_Watertemp": tdWmsWatertemp
};

L.control.layers(baseMaps, null, {collapsed: false}).setPosition('topleft').addTo(map);

// Annotation

var info = L.control({position: 'topright'});

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
info.update = function (props) {
    this._div.innerHTML = `<h4>${slug}</h4>`
};

info.addTo(map);

// Legend

var dischargeLegend = L.control({position: 'bottomright'});
var watertempLegend = L.control({position: 'bottomright'});
var runoffLegend = L.control({position: 'bottomright'});

dischargeLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        `<img src=${discharge_png} alt="legend">`;
    return div;
};

watertempLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        `<img src=${watertemp_png} alt="legend">`;
    return div;
};

runoffLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        `<img src=${runoff_png} alt="legend">`;
    return div;
};

dischargeLegend.addTo(map);

map.on('baselayerchange', function (eventLayer) {
    if (eventLayer.name === 'Discharge') {
        this.removeControl(watertempLegend);
        this.removeControl(runoffLegend);
        dischargeLegend.addTo(this);
    } else if (eventLayer.name === 'QxT_Watertemp') {
        this.removeControl(dischargeLegend);
        this.removeControl(runoffLegend)
        watertempLegend.addTo(this);
    } else {
        this.removeControl(dischargeLegend);
        this.removeControl(watertempLegend)
        runoffLegend.addTo(this);
    }
});

// Bounds

var maxBounds = L.latLngBounds(
    L.latLng(5.5, -143), //Southwest
    L.latLng(65, -50)  //Northeast
);
map.fitBounds(maxBounds);
map.setMaxBounds(maxBounds);

map.options.minZoom = 4;
map.options.maxZoom = 10;

let bnds = map.getBounds();

// form behavior

let lat_start = document.getElementById("lat_start");
lat_start.readOnly = true;
lat_start.value = bnds.getSouth().toFixed(5);

let lat_end = document.getElementById("lat_end");
lat_end.readOnly = true;
lat_end.value = bnds.getNorth().toFixed(5);

let lon_start = document.getElementById("lon_start");
lon_start.readOnly = true;
lon_start.value = bnds.getWest().toFixed(5);

let lon_end  = document.getElementById("lon_end");
lon_end.readOnly = true;
lon_end.value = bnds.getEast().toFixed(5);

let spatial_subset = document.getElementById("id_spatial_subset");

// update form when map moves/zooms
function onExtentChange(e) {
    let bnds = map.getBounds();

    lat_start.value = bnds.getSouth().toFixed(5);
    lat_end.value = bnds.getNorth().toFixed(5);
    lon_start.value = bnds.getWest().toFixed(5);
    lon_end.value = bnds.getEast().toFixed(5);
}
map.on('move', onExtentChange);

// enable/disable extent controls when form option checked
function on_spatial_subset_set(e){
    let val = spatial_subset.checked;
    lat_start.readOnly = !val;
    lat_end.readOnly = !val;
    lon_start.readOnly = !val;
    lon_end.readOnly = !val;
}
spatial_subset.onchange = on_spatial_subset_set;

// update start_date / end_date form inputs when timedimension changes
let start_date = document.getElementById("id_start_date")
start_date.value = new Date(timeDimension.getCurrentTime() + 86400000).toLocaleDateString('en-US');

let end_date = document.getElementById("id_end_date")
end_date.value = new Date(timeDimension.getCurrentTime() + 86400000).toLocaleDateString('en-US');

function update_dateselect(e){
    let d = new Date(timeDimension.getCurrentTime() + 86400000).toLocaleDateString('en-US');
    start_date.value = d;
    end_date.value = d;
}

timeDimension.on('timeloading',update_dateselect);