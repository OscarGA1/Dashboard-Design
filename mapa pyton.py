Mapa_Nidec_HTML =
VAR _DataPoints =
    CONCATENATEX(
        'General Information',
        VAR _lat         = 'General Information'[Latitude]
        VAR _lon         = 'General Information'[Longitude]
        VAR _type        = 'General Information'[Type]
        VAR _site        = 'General Information'[Site]
        VAR _locname     = 'General Information'[Location name]
        VAR _invCost     = FORMAT(CALCULATE([Total Inventory Cost], 'General Information'[Location name] = _locname), "$#,##0")
        VAR _sales       = FORMAT(CALCULATE([Total Sales], 'General Information'[Location name] = _locname), "$#,##0")
        VAR _iconType    = IF(_type = "WH", "WH", "Plant")
        VAR _locnameLow  = LOWER(_locname)
        VAR _siteLow     = LOWER(_site)
        RETURN
        "(function(){
            var m = L.marker([" & _lat & "," & _lon & "], {icon: makeIcon('" & _iconType & "')}).addTo(map);
            m.bindPopup(`<div class='pc'><div class='pc-header pc-" & LOWER(_iconType) & "'><div class='pc-badge'>" & _iconType & "</div><div class='pc-site'>" & _site & "</div><div class='pc-name'>" & _locname & "</div></div><div class='pc-body'><div class='pc-kpi'><div class='pc-kpi-block'><span class='pc-kpi-label'>💰 Inventory Cost</span><span class='pc-kpi-val'>" & _invCost & "</span></div><div class='pc-divider'></div><div class='pc-kpi-block'><span class='pc-kpi-label'>📈 Total Sales</span><span class='pc-kpi-val kpi-green'>" & _sales & "</span></div></div></div></div>`, {maxWidth:260,minWidth:240});
            m.on('mouseover', function(){ this.openPopup(); });
            markers.push(m);
            allMarkers.push({marker:m, name:'" & _locnameLow & "', site:'" & _siteLow & "', type:'" & _iconType & "', displayName:'" & _locname & "', displaySite:'" & _site & "'});
        })();",
        " "
    )

VAR _HTML =
"data:text/html;charset=utf-8,<!DOCTYPE html><html><head>
<meta charset='UTF-8'>
<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>
<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',system-ui,sans-serif;}
#map{height:100vh;width:100vw;}

#searchWrap{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:1000;width:320px;}
#searchIcon{position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:14px;pointer-events:none;}
#searchBox{width:100%;padding:10px 16px 10px 40px;border:none;border-radius:24px;background:rgba(255,255,255,0.97);box-shadow:0 4px 20px rgba(0,0,0,0.25);font-size:13px;color:#1a1a1a;outline:none;transition:box-shadow 0.2s;}
#searchBox:focus{box-shadow:0 4px 28px rgba(0,0,0,0.4);}
#searchResults{margin-top:6px;background:white;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.2);display:none;}
.sr-item{padding:10px 16px;font-size:13px;cursor:pointer;border-bottom:1px solid #f0f0f0;transition:background 0.15s;display:flex;align-items:center;gap:8px;}
.sr-item:hover{background:#f5f9ff;}
.sr-item:last-child{border-bottom:none;}
.sr-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.sr-dot-plant{background:#2D5A8E;}
.sr-dot-wh{background:#2D7A50;}
.sr-text{display:flex;flex-direction:column;}
.sr-name{font-weight:600;color:#1a1a1a;}
.sr-site{font-size:11px;color:#999;}

.icon-outer{position:relative;width:40px;height:40px;display:flex;align-items:center;justify-content:center;}
.pulse-ring{position:absolute;width:40px;height:40px;border-radius:50%;animation:pulse 2.4s ease-out infinite;}
.pulse-plant{border:2px solid rgba(74,144,217,0.7);}
.pulse-wh{border:2px solid rgba(45,122,80,0.7);}
@keyframes pulse{0%{transform:scale(0.95);opacity:1;}70%{transform:scale(1.7);opacity:0;}100%{transform:scale(0.95);opacity:0;}}
.icon-core{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.3);transition:transform 0.2s ease,box-shadow 0.2s ease;cursor:pointer;}
.icon-core:hover{transform:scale(1.15) translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,0.4);}
.icon-plant{background:linear-gradient(145deg,#1E3A5F,#3a7bd5);}
.icon-wh{background:linear-gradient(145deg,#1A4731,#27ae60);}
.icon-core svg{width:18px;height:18px;fill:white;}

.leaflet-popup-content-wrapper{padding:0;border-radius:14px;border:none;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.22);}
.leaflet-popup-content{margin:0;width:auto !important;}
.leaflet-popup-tip-container{display:none;}
.leaflet-popup-close-button{color:rgba(255,255,255,0.8) !important;font-size:18px !important;top:8px !important;right:10px !important;z-index:10;}

.pc{font-family:'Segoe UI',sans-serif;width:240px;}
.pc-header{padding:14px 16px 12px;position:relative;}
.pc-plant{background:linear-gradient(135deg,#1E3A5F 0%,#3a7bd5 100%);}
.pc-wh{background:linear-gradient(135deg,#1A4731 0%,#27ae60 100%);}
.pc-badge{display:inline-block;background:rgba(255,255,255,0.2);color:white;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;border-radius:20px;margin-bottom:6px;}
.pc-site{color:rgba(255,255,255,0.75);font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:2px;}
.pc-name{color:white;font-size:15px;font-weight:700;line-height:1.2;}
.pc-body{background:white;padding:12px 16px;}
.pc-kpi{display:flex;align-items:stretch;}
.pc-kpi-block{flex:1;display:flex;flex-direction:column;gap:3px;padding:6px 8px;}
.pc-divider{width:1px;background:#eee;margin:4px 0;}
.pc-kpi-label{font-size:10px;color:#999;font-weight:500;text-transform:uppercase;letter-spacing:0.5px;}
.pc-kpi-val{font-size:15px;font-weight:700;color:#1a1a1a;}
.kpi-green{color:#1A7A40;}

.legend{position:absolute;bottom:24px;right:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:12px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.15);}
.legend-title{font-size:9px;font-weight:700;color:#aaa;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}
.legend-item{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:500;color:#333;margin-bottom:5px;}
.legend-item:last-child{margin-bottom:0;}
.l-dot{width:10px;height:10px;border-radius:3px;}
.l-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}
.l-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}

#counter{position:absolute;bottom:24px;left:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:10px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.15);font-size:12px;color:#555;}
#counter span{font-weight:700;color:#1E3A5F;font-size:15px;}

#toggleWrap{position:absolute;top:16px;right:16px;z-index:1000;display:flex;gap:8px;}
.toggle-btn{padding:8px 16px;border:none;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:all 0.2s;letter-spacing:0.5px;}
.toggle-btn.active{color:white;transform:translateY(-1px);box-shadow:0 6px 16px rgba(0,0,0,0.25);}
.toggle-btn.inactive{background:rgba(255,255,255,0.7);color:#999;}
.btn-plant.active{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}
.btn-wh.active{background:linear-gradient(135deg,#1A4731,#27ae60);}
</style>
</head><body>
<div id='map'></div>

<div id='searchWrap'>
    <div id='searchIcon'>🔍</div>
    <input id='searchBox' type='text' placeholder='Search location or site...' autocomplete='off'/>
    <div id='searchResults'></div>
</div>

<div id='toggleWrap'>
    <button class='toggle-btn btn-plant active' onclick='toggleType(""Plant"",this)'>🏭 Plant</button>
    <button class='toggle-btn btn-wh active' onclick='toggleType(""WH"",this)'>🏬 Warehouse</button>
</div>

<div class='legend'>
    <div class='legend-title'>Location Type</div>
    <div class='legend-item'><div class='l-dot l-plant'></div> Manufacturing Plant</div>
    <div class='legend-item'><div class='l-dot l-wh'></div> Warehouse</div>
</div>

<div id='counter'>Showing <span id='visibleCount'>0</span> locations</div>

<script>
var map = L.map('map',{zoomControl:false}).setView([25.7,-100.3],4);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'© Nidec'}).addTo(map);
L.control.zoom({position:'bottomleft'}).addTo(map);

function makeIcon(type){
    var isCls = type==='WH'?'icon-wh':'icon-plant';
    var pCls  = type==='WH'?'pulse-wh':'pulse-plant';
    var svg   = type==='WH'
        ? '<svg viewBox=""0 0 24 24""><path d=""M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z""/></svg>'
        : '<svg viewBox=""0 0 24 24""><path d=""M10 20h4V4h-4v16zm-6 0h4v-8H4v8zm12-12v12h4V8h-4z""/></svg>';
    return L.divIcon({
        html:'<div class=""icon-outer""><div class=""pulse-ring '+pCls+'""></div><div class=""icon-core '+isCls+'"">'+svg+'</div></div>',
        className:'',iconSize:[40,40],iconAnchor:[20,20],popupAnchor:[0,-24]
    });
}

var markers    = [];
var allMarkers = [];
var typeState  = {Plant:true, WH:true};

" & _DataPoints & "

var group = L.featureGroup(markers);
if(group.getLayers().length>0){ map.fitBounds(group.getBounds().pad(0.15)); }
document.getElementById('visibleCount').textContent = markers.length;

function updateCounter(){
    var v = allMarkers.filter(function(m){ return map.hasLayer(m.marker); }).length;
    document.getElementById('visibleCount').textContent = v;
}

function toggleType(type, btn){
    typeState[type] = !typeState[type];
    btn.classList.toggle('active', typeState[type]);
    btn.classList.toggle('inactive', !typeState[type]);
    allMarkers.forEach(function(m){
        if(m.type === type){
            if(typeState[type]){ map.addLayer(m.marker); }
            else { map.removeLayer(m.marker); }
        }
    });
    updateCounter();
}

var searchBox     = document.getElementById('searchBox');
var searchResults = document.getElementById('searchResults');

searchBox.addEventListener('input', function(){
    var q = this.value.toLowerCase().trim();
    searchResults.innerHTML='';
    if(q.length<2){searchResults.style.display='none';return;}
    var matches = allMarkers.filter(function(m){
        return m.name.includes(q)||m.site.includes(q);
    }).slice(0,6);
    if(matches.length===0){searchResults.style.display='none';return;}
    matches.forEach(function(m){
        var div=document.createElement('div');
        div.className='sr-item';
        div.innerHTML='<div class=""sr-dot '+(m.type==='WH'?'sr-dot-wh':'sr-dot-plant')+'"""></div><div class=""sr-text""><span class=""sr-name"">'+m.displayName+'</span><span class=""sr-site"">'+m.displaySite+'</span></div>';
        div.addEventListener('click',function(){
            map.setView(m.marker.getLatLng(),10,{animate:true});
            setTimeout(function(){m.marker.openPopup();},400);
            searchBox.value=m.displayName;
            searchResults.style.display='none';
        });
        searchResults.appendChild(div);
    });
    searchResults.style.display='block';
});

document.addEventListener('click',function(e){
    if(!document.getElementById('searchWrap').contains(e.target)){
        searchResults.style.display='none';
    }
});
</script>
</body></html>"

RETURN _HTML