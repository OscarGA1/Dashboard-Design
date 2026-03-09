Mapa_Nidec_HTML = 
VAR _DataPoints =
    CONCATENATEX (
        'General Information',
        VAR _lat      = 'General Information'[Latitude]
        VAR _lon      = 'General Information'[Longitude]
        VAR _type     = 'General Information'[Type]
        VAR _site     = 'General Information'[Site]
        VAR _locname  = 'General Information'[Location name]
        VAR _cost     = FORMAT ( CALCULATE ( [Total Inventory Cost], 'General Information'[Location name] = _locname ), "$#,##0" )
        VAR _sales    = FORMAT ( CALCULATE ( [Total Sales],          'General Information'[Location name] = _locname ), "$#,##0" )
        VAR _itype    = IF ( _type = "WH", "WH", "Plant" )
        VAR _itypeLow = LOWER ( _itype )
        VAR _nameLow  = LOWER ( _locname )
        VAR _siteLow  = LOWER ( _site )
        RETURN
            "(function(){" &
                "var m=L.marker([" & _lat & "," & _lon & "],{icon:makeIcon('" & _itype & "')}).addTo(map);" &
                "m.bindPopup(" &
                    "'<div class=""pc"">" &
                        "<div class=""pc-header pc-" & _itypeLow & """>" &
                            "<span class=""pc-badge"">" & _itype & "</span>" &
                            "<div class=""pc-site"">" & _site & "</div>" &
                            "<div class=""pc-name"">" & _locname & "</div>" &
                        "</div>" &
                        "<div class=""pc-body"">" &
                            "<div class=""pc-row""><span class=""pc-label"">💰 Inventory Cost</span><span class=""pc-val"">" & _cost & "</span></div>" &
                            "<div class=""pc-sep""></div>" &
                            "<div class=""pc-row""><span class=""pc-label"">📈 Total Sales</span><span class=""pc-val kpi-green"">" & _sales & "</span></div>" &
                        "</div>" &
                    "</div>'," &
                    "{maxWidth:260,minWidth:220}" &
                ");" &
                "m.on(""mouseover"",function(){this.openPopup();});" &
                "markers.push(m);" &
                "allMarkers.push({marker:m,name:""" & _nameLow & """,site:""" & _siteLow & """,type:""" & _itype & """,displayName:""" & _locname & """,displaySite:""" & _site & """});" &
            "})();",
        " "
    )

VAR _HTML = "data:text/html;charset=utf-8," &
"<!DOCTYPE html><html><head><meta charset='UTF-8'>" &
"<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>" &
"<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>" &
"<style>" &
"*{margin:0;padding:0;box-sizing:border-box;}" &
"body{font-family:Segoe UI,sans-serif;}" &
"#map{height:100vh;width:100vw;}" &
"#searchWrap{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:1000;width:300px;}" &
"#searchIcon{position:absolute;left:13px;top:50%;transform:translateY(-50%);font-size:13px;pointer-events:none;}" &
"#searchBox{width:100%;padding:10px 16px 10px 38px;border:none;border-radius:24px;background:rgba(255,255,255,0.97);box-shadow:0 4px 20px rgba(0,0,0,0.22);font-size:13px;color:#1a1a1a;outline:none;}" &
"#searchResults{margin-top:6px;background:white;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.18);display:none;}" &
".sr-item{padding:10px 14px;cursor:pointer;border-bottom:1px solid #f0f0f0;display:flex;align-items:center;gap:8px;transition:background 0.15s;}" &
".sr-item:hover{background:#f5f9ff;}" &
".sr-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}" &
".sr-dot-Plant{background:#2D5A8E;}" &
".sr-dot-WH{background:#2D7A50;}" &
".sr-name{font-size:13px;font-weight:600;color:#1a1a1a;}" &
".sr-site{font-size:11px;color:#aaa;}" &
".icon-outer{position:relative;width:40px;height:40px;display:flex;align-items:center;justify-content:center;}" &
".pulse-ring{position:absolute;width:40px;height:40px;border-radius:50%;animation:pulse 2.4s ease-out infinite;}" &
".pulse-Plant{border:2px solid rgba(58,123,213,0.7);}" &
".pulse-WH{border:2px solid rgba(39,174,96,0.7);}" &
"@keyframes pulse{0%{transform:scale(0.95);opacity:1;}70%{transform:scale(1.75);opacity:0;}100%{transform:scale(0.95);opacity:0;}}" &
".icon-core{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.28);transition:transform 0.2s,box-shadow 0.2s;cursor:pointer;}" &
".icon-core:hover{transform:scale(1.18) translateY(-2px);box-shadow:0 8px 22px rgba(0,0,0,0.38);}" &
".icon-Plant{background:linear-gradient(145deg,#1E3A5F,#3a7bd5);}" &
".icon-WH{background:linear-gradient(145deg,#1A4731,#27ae60);}" &
".icon-core svg{width:17px;height:17px;fill:white;}" &
".leaflet-popup-content-wrapper{padding:0;border-radius:14px;border:none;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.2);}" &
".leaflet-popup-content{margin:0!important;}" &
".leaflet-popup-tip-container{display:none;}" &
".leaflet-popup-close-button{color:rgba(255,255,255,0.85)!important;font-size:17px!important;top:7px!important;right:9px!important;}" &
".pc{width:240px;font-family:Segoe UI,sans-serif;}" &
".pc-header{padding:14px 16px;}" &
".pc-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
".pc-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
".pc-badge{display:inline-block;background:rgba(255,255,255,0.2);color:white;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:2px 8px;border-radius:20px;margin-bottom:6px;}" &
".pc-site{color:rgba(255,255,255,0.7);font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;}" &
".pc-name{color:white;font-size:15px;font-weight:700;line-height:1.2;}" &
".pc-body{background:white;padding:12px 16px;}" &
".pc-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;}" &
".pc-sep{height:1px;background:#f0f0f0;margin:2px 0;}" &
".pc-label{font-size:11px;color:#999;font-weight:500;}" &
".pc-val{font-size:13px;font-weight:700;color:#1a1a1a;}" &
".kpi-green{color:#1A7A40;}" &
"#toggleWrap{position:absolute;top:16px;right:16px;z-index:1000;display:flex;gap:8px;}" &
".tbtn{padding:8px 14px;border:none;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:all 0.2s;}" &
".tbtn-on-Plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);color:white;}" &
".tbtn-on-WH{background:linear-gradient(135deg,#1A4731,#27ae60);color:white;}" &
".tbtn-off{background:rgba(255,255,255,0.75);color:#bbb;box-shadow:none;}" &
".legend{position:absolute;bottom:24px;right:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:12px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);}" &
".legend-title{font-size:9px;font-weight:700;color:#bbb;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}" &
".li{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:500;color:#444;margin-bottom:5px;}" &
".li:last-child{margin-bottom:0;}" &
".ld{width:10px;height:10px;border-radius:3px;}" &
".ld-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
".ld-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
"#counter{position:absolute;bottom:24px;left:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:10px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);font-size:12px;color:#777;}" &
"#counter b{font-size:15px;color:#1E3A5F;}" &
"</style></head><body>" &
"<div id='map'></div>" &
"<div id='searchWrap'>" &
"<span id='searchIcon'>🔍</span>" &
"<input id='searchBox' type='text' placeholder='Search location or site...' autocomplete='off'/>" &
"<div id='searchResults'></div>" &
"</div>" &
"<div id='toggleWrap'>" &
"<button id='btnPlant' class='tbtn tbtn-on-Plant' onclick='toggleType(""Plant"")'>🏭 Plant</button>" &
"<button id='btnWH' class='tbtn tbtn-on-WH' onclick='toggleType(""WH"")'>🏬 Warehouse</button>" &
"</div>" &
"<div class='legend'>" &
"<div class='legend-title'>Location Type</div>" &
"<div class='li'><div class='ld ld-plant'></div>Manufacturing Plant</div>" &
"<div class='li'><div class='ld ld-wh'></div>Warehouse</div>" &
"</div>" &
"<div id='counter'>Showing <b id='cnt'>0</b> locations</div>" &
"<script>" &
"var map=L.map('map',{zoomControl:false}).setView([25.7,-100.3],4);" &
"L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'© Nidec'}).addTo(map);" &
"L.control.zoom({position:'bottomleft'}).addTo(map);" &
"function makeIcon(t){" &
"var ic=t==='WH'?'icon-WH':'icon-Plant';" &
"var pc=t==='WH'?'pulse-WH':'pulse-Plant';" &
"var sv=t==='WH'" &
"?'<svg viewBox=""0 0 24 24""><path d=""M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z""/></svg>'" &
":'<svg viewBox=""0 0 24 24""><path d=""M10 20h4V4h-4v16zm-6 0h4v-8H4v8zm12-12v12h4V8h-4z""/></svg>';" &
"return L.divIcon({html:'<div class=""icon-outer""><div class=""pulse-ring '+pc+'""></div><div class=""icon-core '+ic+'"">'+sv+'</div></div>',className:'',iconSize:[40,40],iconAnchor:[20,20],popupAnchor:[0,-24]});}" &
"var markers=[];var allMarkers=[];var typeOn={Plant:true,WH:true};" &
 _DataPoints &
"var grp=L.featureGroup(markers);" &
"if(grp.getLayers().length>0){map.fitBounds(grp.getBounds().pad(0.15));}" &
"document.getElementById('cnt').textContent=markers.length;" &
"function updateCnt(){document.getElementById('cnt').textContent=allMarkers.filter(function(x){return map.hasLayer(x.marker);}).length;}" &
"function toggleType(t){" &
"typeOn[t]=!typeOn[t];" &
"var btn=document.getElementById('btn'+t);" &
"btn.className=typeOn[t]?'tbtn tbtn-on-'+t:'tbtn tbtn-off';" &
"allMarkers.forEach(function(x){if(x.type===t){typeOn[t]?map.addLayer(x.marker):map.removeLayer(x.marker);}});" &
"updateCnt();}" &
"var sb=document.getElementById('searchBox');" &
"var sr=document.getElementById('searchResults');" &
"sb.addEventListener('input',function(){" &
"var q=this.value.toLowerCase().trim();" &
"sr.innerHTML='';" &
"if(q.length<2){sr.style.display='none';return;}" &
"var hits=allMarkers.filter(function(x){return x.name.includes(q)||x.site.includes(q);}).slice(0,6);" &
"if(!hits.length){sr.style.display='none';return;}" &
"hits.forEach(function(x){" &
"var d=document.createElement('div');" &
"d.className='sr-item';" &
"d.innerHTML='<div class=""sr-dot sr-dot-'+x.type+'""></div><div><div class=""sr-name"">'+x.displayName+'</div><div class=""sr-site"">'+x.displaySite+'</div></div>';" &
"d.onclick=function(){map.setView(x.marker.getLatLng(),10,{animate:true});setTimeout(function(){x.marker.openPopup();},400);sb.value=x.displayName;sr.style.display='none';};" &
"sr.appendChild(d);});" &
"sr.style.display='block';});" &
"document.addEventListener('click',function(e){if(!document.getElementById('searchWrap').contains(e.target)){sr.style.display='none';}});" &
"</script></body></html>"

RETURN _HTML
