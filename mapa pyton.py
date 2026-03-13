2Mapa_Nidec_HTML = 
VAR _Tabla =
    FILTER (
        'General Information',
        NOT ISBLANK ( 'General Information'[Latitude] ) &&
        NOT ISBLANK ( 'General Information'[Longitude] ) &&
        'General Information'[Latitude] <> 0 &&
        'General Information'[Longitude] <> 0
    )

VAR _DataPoints =
    CONCATENATEX (
        _Tabla,
        VAR _lat      = 'General Information'[Latitude]
        VAR _lon      = 'General Information'[Longitude]
        VAR _type     = 'General Information'[Type]
        VAR _site     = 'General Information'[Site]
        VAR _locname  = 'General Information'[Location name]
        VAR _cost     = FORMAT ( CALCULATE ( [Total Inventory Cost], 'General Information'[Location name] = _locname ), "$#,##0" )
        VAR _sales    = FORMAT ( CALCULATE ( [Total Sales],          'General Information'[Location name] = _locname ), "$#,##0" )
        VAR _itype    = IF ( _type = "WH", "WH", IF ( _type = "Office", "Office", IF ( _type = "3PL", "3PL", IF ( _type = "Virtual", "Virtual", "Plant" ) ) ) )
        VAR _itypeLow = LOWER ( _itype )
        VAR _nameLow  = LOWER ( _locname )
        VAR _siteLow  = LOWER ( _site )
        RETURN
            "(function(){" &
                "var m=L.marker([" & _lat & "," & _lon & "],{icon:makeIcon('" & _itype & "')});" &
                "m.bindPopup(" &
                    "'<div class=""pc"">" &
                        "<div class=""pc-header pc-" & _itypeLow & """>" &
                            "<span class=""pc-badge"">" & _itype & "</span>" &
                            "<div class=""pc-site"">" & _site & "</div>" &
                            "<div class=""pc-name"">" & _locname & "</div>" &
                        "</div>" &
                        "<div class=""pc-body"">" &
                            "<div class=""pc-row""><span class=""pc-label"">💰 Current Inventory Cost</span><span class=""pc-val"">" & _cost & "</span></div>" &
                            "<div class=""pc-sep""></div>" &
                            "<div class=""pc-row""><span class=""pc-label"">📈 Total Sales of Current Month</span><span class=""pc-val kpi-green"">" & _sales & "</span></div>" &
                        "</div>" &
                    "</div>'," &
                    "{maxWidth:260,minWidth:220}" &
                ");" &
                "m.on('mouseover',function(){this.openPopup();});" &
                "allMarkers.push({marker:m,name:'" & _nameLow & "',site:'" & _siteLow & "',type:'" & _itype & "',displayName:'" & _locname & "',displaySite:'" & _site & "'});" &
            "})();",
        " "
    )

VAR _HTML =
    "data:text/html;charset=utf-8," &
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>" &
    "<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>" &
    "<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>" &
    "<style>" &
    "*{margin:0;padding:0;box-sizing:border-box;}" &
    "body{font-family:Segoe UI,sans-serif;}" &
    "#map{height:100vh;width:100vw;}" &

    "/* Icon wraps */" &
    ".icon-wrap{width:40px;height:40px;position:relative;display:flex;align-items:center;justify-content:center;}" &
    ".pulse-ring{position:absolute;inset:0;border-radius:50%;animation:pulse 2.4s ease-out infinite;pointer-events:none;}" &
    ".pulse-Plant{border:2px solid rgba(58,123,213,0.8);}" &
    ".pulse-WH{border:2px solid rgba(39,174,96,0.8);}" &
    ".pulse-Office{border:2px solid rgba(155,89,182,0.8);}" &
    ".pulse-3PL{border:2px solid rgba(230,126,34,0.8);}" &
    ".pulse-Virtual{border:2px solid rgba(149,165,166,0.8);}" &
    "@keyframes pulse{0%{transform:scale(0.9);opacity:1;}70%{transform:scale(1.8);opacity:0;}100%{transform:scale(0.9);opacity:0;}}" &

    "/* Icon cores */" &
    ".icon-core{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.32);transition:transform 0.2s,box-shadow 0.2s;}" &
    ".icon-Plant{background:linear-gradient(145deg,#1E3A5F,#3a7bd5);}" &
    ".icon-WH{background:linear-gradient(145deg,#1A4731,#27ae60);}" &
    ".icon-Office{background:linear-gradient(145deg,#4A1A6B,#9b59b6);}" &
    ".icon-3PL{background:linear-gradient(145deg,#7A3A1A,#e67e22);}" &
    ".icon-Virtual{background:linear-gradient(145deg,#2A2A3A,#95a5a6);}" &
    ".icon-core svg{width:17px;height:17px;fill:white;display:block;}" &

    "/* Popups */" &
    ".leaflet-popup-content-wrapper{padding:0;border-radius:14px;border:none;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.2);}" &
    ".leaflet-popup-content{margin:0!important;}" &
    ".leaflet-popup-tip-container{display:none;}" &
    ".leaflet-popup-close-button{color:rgba(255,255,255,0.85)!important;font-size:17px!important;top:7px!important;right:9px!important;}" &
    ".pc{width:240px;font-family:Segoe UI,sans-serif;}" &
    ".pc-header{padding:14px 16px;}" &
    ".pc-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
    ".pc-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
    ".pc-office{background:linear-gradient(135deg,#4A1A6B,#9b59b6);}" &
    ".pc-3pl{background:linear-gradient(135deg,#7A3A1A,#e67e22);}" &
    ".pc-virtual{background:linear-gradient(135deg,#2A2A3A,#95a5a6);}" &
    ".pc-badge{display:inline-block;background:rgba(255,255,255,0.2);color:white;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:2px 8px;border-radius:20px;margin-bottom:6px;}" &
    ".pc-site{color:rgba(255,255,255,0.7);font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;}" &
    ".pc-name{color:white;font-size:15px;font-weight:700;line-height:1.2;}" &
    ".pc-body{background:white;padding:12px 16px;}" &
    ".pc-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;}" &
    ".pc-sep{height:1px;background:#f0f0f0;margin:2px 0;}" &
    ".pc-label{font-size:11px;color:#999;font-weight:500;}" &
    ".pc-val{font-size:13px;font-weight:700;color:#1a1a1a;}" &
    ".kpi-green{color:#1A7A40;}" &

    "/* Search */" &
    "#searchWrap{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:1000;width:300px;}" &
    "#searchIcon{position:absolute;left:13px;top:50%;transform:translateY(-50%);font-size:13px;pointer-events:none;}" &
    "#searchBox{width:100%;padding:10px 16px 10px 38px;border:none;border-radius:24px;background:rgba(255,255,255,0.97);box-shadow:0 4px 20px rgba(0,0,0,0.22);font-size:13px;color:#1a1a1a;outline:none;}" &
    "#searchResults{margin-top:6px;background:white;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.18);display:none;}" &
    ".sr-item{padding:10px 14px;cursor:pointer;border-bottom:1px solid #f0f0f0;display:flex;align-items:center;gap:8px;transition:background 0.15s;}" &
    ".sr-item:hover{background:#f5f9ff;}" &
    ".sr-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}" &
    ".sr-dot-Plant{background:#2D5A8E;}" &
    ".sr-dot-WH{background:#2D7A50;}" &
    ".sr-dot-Office{background:#7D3A9B;}" &
    ".sr-dot-3PL{background:#C0621A;}" &
    ".sr-dot-Virtual{background:#707B7C;}" &
    ".sr-name{font-size:13px;font-weight:600;color:#1a1a1a;}" &
    ".sr-site{font-size:11px;color:#aaa;}" &

    "/* Toggle buttons */" &
    "#toggleWrap{position:absolute;top:16px;right:16px;z-index:1000;display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;max-width:340px;}" &
    ".tbtn{padding:8px 14px;border:none;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:all 0.2s;}" &
    ".tbtn-on-Plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);color:white;}" &
    ".tbtn-on-WH{background:linear-gradient(135deg,#1A4731,#27ae60);color:white;}" &
    ".tbtn-on-Office{background:linear-gradient(135deg,#4A1A6B,#9b59b6);color:white;}" &
    ".tbtn-on-3PL{background:linear-gradient(135deg,#7A3A1A,#e67e22);color:white;}" &
    ".tbtn-on-Virtual{background:linear-gradient(135deg,#2A2A3A,#95a5a6);color:white;}" &
    ".tbtn-off{background:rgba(255,255,255,0.75);color:#bbb;box-shadow:none;}" &

    "/* Legend */" &
    ".legend{position:absolute;bottom:24px;right:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:12px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);}" &
    ".legend-title{font-size:9px;font-weight:700;color:#bbb;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}" &
    ".li{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:500;color:#444;margin-bottom:5px;}" &
    ".li:last-child{margin-bottom:0;}" &
    ".ld{width:10px;height:10px;border-radius:3px;}" &
    ".ld-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
    ".ld-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
    ".ld-office{background:linear-gradient(135deg,#4A1A6B,#9b59b6);}" &
    ".ld-3pl{background:linear-gradient(135deg,#7A3A1A,#e67e22);}" &
    ".ld-virtual{background:linear-gradient(135deg,#2A2A3A,#95a5a6);}" &

    "/* Counter */" &
    "#counter{position:absolute;bottom:24px;left:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:10px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);font-size:12px;color:#777;}" &
    "#counter b{font-size:15px;color:#1E3A5F;}" &
    "</style></head><body>" &

    "<div id='map'></div>" &
    "<div id='searchWrap'><span id='searchIcon'>🔍</span><input id='searchBox' type='text' placeholder='Search location or site...' autocomplete='off'/><div id='searchResults'></div></div>" &

    "<div id='toggleWrap'>" &
    "<button id='btnPlant'   class='tbtn tbtn-on-Plant'   onclick='toggleType(""Plant"")'>🏭 Plant</button>" &
    "<button id='btnWH'      class='tbtn tbtn-on-WH'      onclick='toggleType(""WH"")'>🏬 Warehouse</button>" &
    "<button id='btnOffice'  class='tbtn tbtn-on-Office'  onclick='toggleType(""Office"")'>🏢 Office</button>" &
    "<button id='btn3PL'     class='tbtn tbtn-on-3PL'     onclick='toggleType(""3PL"")'>📦 3PL</button>" &
    "<button id='btnVirtual' class='tbtn tbtn-on-Virtual' onclick='toggleType(""Virtual"")'>🌐 Virtual</button>" &
    "</div>" &

    "<div class='legend'>" &
    "<div class='legend-title'>Location Type</div>" &
    "<div class='li'><div class='ld ld-plant'></div>Manufacturing Plant</div>" &
    "<div class='li'><div class='ld ld-wh'></div>Warehouse</div>" &
    "<div class='li'><div class='ld ld-office'></div>Office</div>" &
    "<div class='li'><div class='ld ld-3pl'></div>3PL</div>" &
    "<div class='li'><div class='ld ld-virtual'></div>Virtual</div>" &
    "</div>" &

    "<div id='counter'>Showing <b id='cnt'>0</b> locations</div>" &

    "<script>" &
    "var map=L.map('map',{zoomControl:false}).setView([25.7,-100.3],4);" &
    "L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'© Nidec'}).addTo(map);" &
    "L.control.zoom({position:'bottomleft'}).addTo(map);" &

    "function makeIcon(t){" &
    "var ic='icon-'+t;var pc='pulse-'+t;var sv;" &
    "if(t==='WH'){" &
    "sv='<svg viewBox=""0 0 24 24""><path d=""M1 21V8l11-6 11 6v13H1zm2-2h18V9.25L12 4.15 3 9.25V19zm4-1h10v-5H7v5zm0-7h2V9H7v2zm4 0h2V9h-2v2zm4 0h2V9h-2v2zm-8 5h2v-3H7v3zm4 0h2v-3h-2v3zm4 0h2v-3h-2v3z""/></svg>';}" &
    "else if(t==='Office'){" &
    "sv='<svg viewBox=""0 0 24 24""><path d=""M5 3h14v18H5V3zm2 2v14h10V5H7zm2 2h2v2H9V7zm4 0h2v2h-2V7zm-4 4h2v2H9v-2zm4 0h2v2h-2v-2zm-4 4h2v2H9v-2zm4 0h2v2h-2v-2zM9 17h6v4H9v-4z""/></svg>';}" &
    "else if(t==='3PL'){" &
    "sv='<svg viewBox=""0 0 24 24""><path d=""M3 3h18v3H3V3zm0 4h18v1H3V7zm1 2h16v12H4V9zm2 2v8h12v-8H6zm1 1h4v3H7v-3zm6 0h4v3h-4v-3zm-6 4h4v3H7v-3zm6 0h4v3h-4v-3z""/></svg>';}" &
    "else if(t==='Virtual'){" &
    "sv='<svg viewBox=""0 0 24 24""><path d=""M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm-1 17.93V18c0-.55.45-1 1-1s1 .45 1 1v1.93A8.01 8.01 0 0 1 4.07 13H6c.55 0 1 .45 1 1s-.45 1-1 1H4.07zM4.07 11H6c.55 0 1-.45 1-1s-.45-1-1-1H4.07A8.01 8.01 0 0 1 11 4.07V6c0 .55.45 1 1 1s1-.45 1-1V4.07A8.01 8.01 0 0 1 19.93 11H18c-.55 0-1 .45-1 1s.45 1 1 1h1.93A8.01 8.01 0 0 1 13 19.93V18c0-.55-.45-1-1-1s-1 .45-1 1v1.93A8.01 8.01 0 0 1 4.07 11z""/></svg>';}" &
    "else{" &
    "sv='<svg viewBox=""0 0 24 24""><path d=""M2 20V8.5L12 2l10 6.5V20H2zm2-2h16V9.6L12 4.15 4 9.6V18zm3-1h2v-3H7v3zm4 0h2v-3h-2v3zm4 0h2v-3h-2v3zM7 13h2v-2H7v2zm4 0h2v-2h-2v2zm4 0h2v-2h-2v2z""/></svg>';}" &
    "return L.divIcon({html:'<div class=""icon-wrap""><div class=""pulse-ring '+pc+'""></div><div class=""icon-core '+ic+'"">'+sv+'</div></div>',className:'',iconSize:[40,40],iconAnchor:[20,20],popupAnchor:[0,-24]});}" &

    "function makeClusterIcon(count,types){" &
    "var colors={Plant:'#3a7bd5',WH:'#27ae60',Office:'#9b59b6','3PL':'#e67e22',Virtual:'#95a5a6'};" &
    "var dominant=Object.keys(types).reduce(function(a,b){return types[a]>types[b]?a:b;});" &
    "var col=colors[dominant]||'#3a7bd5';" &
    "var size=count<5?38:count<10?46:54;" &
    "var fs=count<5?13:count<10?15:17;" &
    "return L.divIcon({" &
    "html:'<div style=""width:'+size+'px;height:'+size+'px;border-radius:50%;background:'+col+';border:3px solid white;box-shadow:0 4px 16px rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:'+fs+'px;font-family:Segoe UI,sans-serif;"">'+count+'</div>'," &
    "className:''," &
    "iconSize:[size,size]," &
    "iconAnchor:[size/2,size/2]" &
    "});}" &

    "var allMarkers=[];var clusterMarkers=[];var typeOn={Plant:true,WH:true,Office:true,'3PL':true,Virtual:true};" &
    "var CLUSTER_RADIUS=60;var CLUSTER_MIN=3;var CLUSTER_MAX_ZOOM=6;" &

    _DataPoints &

    "function runClustering(){" &
    "clusterMarkers.forEach(function(c){map.removeLayer(c);});clusterMarkers=[];" &
    "allMarkers.forEach(function(x){map.removeLayer(x.marker);});" &
    "var active=allMarkers.filter(function(x){return typeOn[x.type];});" &
    "var currentZoom=map.getZoom();" &

    /* If zoom > threshold, show all individual markers, no clustering */
    "if(currentZoom>CLUSTER_MAX_ZOOM){" &
    "active.forEach(function(x){map.addLayer(x.marker);});" &
    "document.getElementById('cnt').textContent=active.length;" &
    "return;}" &

    "var assigned=new Array(active.length).fill(false);" &
    "var clusters=[];" &
    "for(var i=0;i<active.length;i++){" &
    "if(assigned[i])continue;" &
    "var group=[i];assigned[i]=true;" &
    "var pi=map.latLngToContainerPoint(active[i].marker.getLatLng());" &
    "for(var j=i+1;j<active.length;j++){" &
    "if(assigned[j])continue;" &
    "var pj=map.latLngToContainerPoint(active[j].marker.getLatLng());" &
    "var dx=pi.x-pj.x,dy=pi.y-pj.y;" &
    "if(Math.sqrt(dx*dx+dy*dy)<CLUSTER_RADIUS){group.push(j);assigned[j]=true;}" &
    "}clusters.push(group);}" &

    "var cnt=0;" &
    "clusters.forEach(function(group){" &

    /* Only cluster if group has >= CLUSTER_MIN markers */
    "if(group.length<CLUSTER_MIN){" &
    "group.forEach(function(idx){map.addLayer(active[idx].marker);});cnt+=group.length;" &
    "}else{" &
    "var sumLat=0,sumLng=0,types={};" &
    "group.forEach(function(idx){" &
    "var ll=active[idx].marker.getLatLng();" &
    "sumLat+=ll.lat;sumLng+=ll.lng;" &
    "types[active[idx].type]=(types[active[idx].type]||0)+1;" &
    "});" &
    "var cLat=sumLat/group.length,cLng=sumLng/group.length;" &
    "var cm=L.marker([cLat,cLng],{icon:makeClusterIcon(group.length,types)}).addTo(map);" &
    "(function(g){cm.on('click',function(){" &
    "var lats=g.map(function(i){return active[i].marker.getLatLng().lat;});" &
    "var lngs=g.map(function(i){return active[i].marker.getLatLng().lng;});" &
    "var minLat=Math.min.apply(null,lats),maxLat=Math.max.apply(null,lats);" &
    "var minLng=Math.min.apply(null,lngs),maxLng=Math.max.apply(null,lngs);" &
    /* If all points at same location, force zoom in by +3 levels */
    "if(maxLat-minLat<0.01&&maxLng-minLng<0.01){" &
    "map.setView([lats[0],lngs[0]],Math.min(map.getZoom()+3,18),{animate:true});" &
    "}else{" &
    "map.fitBounds([[minLat,minLng],[maxLat,maxLng]],{padding:[80,80],animate:true,maxZoom:14});" &
    "}" &
    "});})(group);" &
    "clusterMarkers.push(cm);cnt+=group.length;" &
    "}" &
    "});" &
    "document.getElementById('cnt').textContent=cnt;}" &

    "map.on('zoomend moveend',runClustering);" &

    "var grp=L.featureGroup(allMarkers.map(function(x){return x.marker;}));" &
    "if(grp.getLayers().length>0){map.fitBounds(grp.getBounds().pad(0.15),{animate:false});}" &
    "setTimeout(function(){runClustering();},100);" &

    "function toggleType(t){" &
    "typeOn[t]=!typeOn[t];" &
    "var btnId=t==='3PL'?'btn3PL':'btn'+t;" &
    "document.getElementById(btnId).className=typeOn[t]?'tbtn tbtn-on-'+t:'tbtn tbtn-off';" &
    "runClustering();}" &

    "var sb=document.getElementById('searchBox'),sr=document.getElementById('searchResults');" &
    "sb.addEventListener('input',function(){" &
    "var q=this.value.toLowerCase().trim();" &
    "sr.innerHTML='';" &
    "if(q.length<2){sr.style.display='none';return;}" &
    "var hits=allMarkers.filter(function(x){return x.name.includes(q)||x.site.includes(q);}).slice(0,6);" &
    "if(!hits.length){sr.style.display='none';return;}" &
    "hits.forEach(function(x){" &
    "var d=document.createElement('div');d.className='sr-item';" &
    "d.innerHTML='<div class=""sr-dot sr-dot-'+x.type+'""></div><div><div class=""sr-name"">'+x.displayName+'</div><div class=""sr-site"">'+x.displaySite+'</div></div>';" &
    "d.onclick=function(){map.setView(x.marker.getLatLng(),10,{animate:true});setTimeout(function(){runClustering();x.marker.openPopup();},600);sb.value=x.displayName;sr.style.display='none';};" &
    "sr.appendChild(d);});" &
    "sr.style.display='block';});" &
    "document.addEventListener('click',function(e){if(!document.getElementById('searchWrap').contains(e.target)){sr.style.display='none';}});" &
    "</script></body></html>"

RETURN _HTML
