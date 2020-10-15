let optimalTileSize = L.point(430, 280);

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

L.control.scale().addTo(map)

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
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    noWrap: true
});

OpenStreetMap_Mapnik.addTo(map);

let asrc_attribution = '<a href="https://asrc.gc.cuny.edu/environment/">CUNY ASRC ESI</a>'

var wmsUrl = "http://10.16.12.61:9999/geoserver/newswbm/wms"
var wmsDischarge = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    tileSize: optimalTileSize,
    layers: `newswbm:multiscenario_${slug}_discharge_daily_${year}_nolakes`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution,
    noWrap: true
});

// Create and add a TimeDimension Layer to the map
var tdWmsDischarge = L.timeDimension.layer.wms(wmsDischarge);

var wmsWatertemp = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    tileSize: optimalTileSize,
    layers: `newswbm:multiscenario_${slug}_qxt_watertemp_daily_${year}_nolakes`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution,
    noWrap: true
});

// Create and add a TimeDimension Layer to the map
var tdWmsWatertemp = L.timeDimension.layer.wms(wmsWatertemp);

var wmsAirTemperature = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    tileSize: optimalTileSize,
    layers: `newswbm:multiscenario_${slug}_airtemperature_daily_${year}_nolakes`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution,
    noWrap: true
});

// Create and add a TimeDimension Layer to the map
var tdWmsAirTemperature = L.timeDimension.layer.wms(wmsAirTemperature);

var wmsWetBulbTemp = L.tileLayer.wms(wmsUrl, {
    tiled: true,
    tileSize: optimalTileSize,
    layers: `newswbm:multiscenario_${slug}_wetbulbtemp_daily_${year}_nolakes`,
    opacity: 0.5,
    format: 'image/png',
    transparent: true,
    attribution: asrc_attribution,
    noWrap: true
});

// Create and add a TimeDimension Layer to the map
var tdWmsWetBulbTemp = L.timeDimension.layer.wms(wmsWetBulbTemp);

// Default layer
tdWmsDischarge.addTo(map);

var baseMaps = {
    "Discharge": tdWmsDischarge,
    "QxT_Watertemp": tdWmsWatertemp,
    "Air Temperature": tdWmsAirTemperature,
    "Wet Bulb Temperature": tdWmsWetBulbTemp
};

let layer_control = L.control.layers(baseMaps, null, {collapsed: false}).setPosition('topleft').addTo(map);

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
// var runoffLegend = L.control({position: 'bottomright'});
var airtemperatureLegend = L.control({position: 'bottomright'});
var wetbulbtempLegend = L.control({position: 'bottomright'});


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

airtemperatureLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        `<img src=${airtemperature_png} alt="legend">`;
    return div;
};

wetbulbtempLegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        `<img src=${wetbulbtemp_png} alt="legend">`;
    return div;
};

dischargeLegend.addTo(map);

map.on('baselayerchange', function (eventLayer) {
    if (eventLayer.name === 'Discharge') {
        this.removeControl(watertempLegend);
        // this.removeControl(runoffLegend);
        this.removeControl(airtemperatureLegend);
        this.removeControl(wetbulbtempLegend);
        dischargeLegend.addTo(this);
    } else if (eventLayer.name === 'QxT_Watertemp') {
        this.removeControl(dischargeLegend);
        this.removeControl(airtemperatureLegend);
        this.removeControl(wetbulbtempLegend);
        // this.removeControl(runoffLegend)
        watertempLegend.addTo(this);
    } else if (eventLayer.name === 'Air Temperature') {
        this.removeControl(dischargeLegend);
        this.removeControl(watertempLegend);
        this.removeControl(wetbulbtempLegend);
        // this.removeControl(runoffLegend)
        airtemperatureLegend.addTo(this);
    } else if (eventLayer.name === 'Wet Bulb Temperature') {
        this.removeControl(dischargeLegend);
        this.removeControl(airtemperatureLegend);
        this.removeControl(watertempLegend);
        // this.removeControl(runoffLegend)
        wetbulbtempLegend.addTo(this);
    }
});

// Bounds
map.options.minZoom = 4;
map.options.maxZoom = 10;

var InitialBounds = L.latLngBounds(
    L.latLng(10, -180), //Southwest
    L.latLng(65, -14)  //Northeast
);
map.fitBounds(InitialBounds);

var maxBounds = L.latLngBounds(
    L.latLng(0, -180), //Southwest
    L.latLng(90, 0)  //Northeast
);
map.setMaxBounds(maxBounds);


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

let lon_end = document.getElementById("lon_end");
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
function on_spatial_subset_set(e) {
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

function update_dateselect(e) {
    let d = new Date(timeDimension.getCurrentTime() + 86400000).toLocaleDateString('en-US');
    start_date.value = d;
    end_date.value = d;
}

timeDimension.on('timeloading', update_dateselect);

// change download selection when layer changes
map.on('baselayerchange', function (e) {
    let var_select = document.getElementById("id_variable")
    if (map.hasLayer(tdWmsDischarge)) {
        var_select.value = "discharge"
    } else if (map.hasLayer(tdWmsWatertemp)) {
        var_select.value = "qxt_watertemp"
    } else if (map.hasLayer(tdWmsAirTemperature)) {
        var_select.value = "airtemperature"
    } else if (map.hasLayer(tdWmsWetBulbTemp)) {
        var_select.value = "wetbulbtemp"
    }
})


// Bounding Box Select tool

var drawnItems = new L.FeatureGroup();

var drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        circle: false,
        polygon: false,
        marker: false,
        rectangle: {
            repeatMode: true
        }
    },
    edit: {
     featureGroup: drawnItems,
     edit: false
    }
});

map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {

    drawnItems.getLayers().forEach(function (layer) {
        map.removeLayer(layer);
    })

    var type = e.layerType,
        layer = e.layer;
    if (type === 'rectangle') {
        // Do marker specific actions
        bnds = layer._bounds;
        lat_start.value = bnds.getSouth().toFixed(5);
        lat_end.value = bnds.getNorth().toFixed(5);
        lon_start.value = bnds.getWest().toFixed(5);
        lon_end.value = bnds.getEast().toFixed(5);
    }
    // Do whatever else you need to. (save to db; add to map etc)
    drawnItems.addLayer(layer);
    map.addLayer(drawnItems);
});

