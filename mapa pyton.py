Mapa_Nidec_HTML = 
VAR _Tabla =
    FILTER (
        'General Information',
        NOT ISBLANK ( 'General Information'[Latitude] ) &&
        NOT ISBLANK ( 'General Information'[Longitude] ) &&
        'General Information'[Latitude] <> 0 &&
        'General Information'[Longitude] <> 0 &&
        'General Information'[Type] <> "Virtual"
    )

VAR _TablaVirtual =
    FILTER (
        'General Information',
        'General Information'[Type] = "Virtual"
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
        VAR _itype    = _type
        VAR _itypeLow = LOWER ( _itype )
        VAR _nameLow  = LOWER ( _locname )
        VAR _siteLow  = LOWER ( _site )
        RETURN
            "(function(){" &
                "var m=L.marker([" & _lat & "," & _lon & "],{icon:makeIcon('" & _itype & "')}).addTo(mcg);" &
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
                "m.on('mouseover',function(){this.openPopup();});" &
                "markers.push(m);" &
                "allMarkers.push({marker:m,name:'" & _nameLow & "',site:'" & _siteLow & "',type:'" & _itype & "',displayName:'" & _locname & "',displaySite:'" & _site & "'});" &
            "})();",
        " "
    )

VAR _VirtualCards =
    CONCATENATEX (
        _TablaVirtual,
        VAR _site    = 'General Information'[Site]
        VAR _locname = 'General Information'[Location name]
        VAR _cost    = FORMAT ( CALCULATE ( [Total Inventory Cost], 'General Information'[Location name] = _locname ), "$#,##0" )
        VAR _sales   = FORMAT ( CALCULATE ( [Total Sales],          'General Information'[Location name] = _locname ), "$#,##0" )
        RETURN
            "virtualData.push({site:'" & _site & "',name:'" & _locname & "',cost:'" & _cost & "',sales:'" & _sales & "'});",
        " "
    )

VAR _HTML =
    "data:text/html;charset=utf-8," &
    "<!DOCTYPE html><html><head><meta charset='UTF-8'>" &
    "<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>" &
    "<link rel='stylesheet' href='https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css'/>" &
    "<link rel='stylesheet' href='https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css'/>" &
    "<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>" &
    "<script src='https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js'></script>" &
    "<style>" &
    "*{margin:0;padding:0;box-sizing:border-box;}" &
    "body{font-family:Segoe UI,sans-serif;}" &
    "#map{height:100vh;width:100vw;}" &

    "/* ── Cluster overrides ── */" &
    ".marker-cluster{background:rgba(30,58,95,0.15)!important;}" &
    ".marker-cluster div{background:rgba(30,58,95,0.88)!important;color:#fff!important;font-family:Segoe UI,sans-serif;font-size:12px;font-weight:700;}" &
    ".marker-cluster-small div{background:rgba(45,90,142,0.88)!important;}" &
    ".marker-cluster-medium div{background:rgba(30,58,95,0.88)!important;}" &
    ".marker-cluster-large div{background:rgba(15,30,60,0.92)!important;}" &

    "/* ── Icons ── */" &
    ".icon-wrap{width:40px;height:40px;position:relative;display:flex;align-items:center;justify-content:center;}" &
    ".pulse-ring{position:absolute;inset:0;border-radius:50%;animation:pulse 2.4s ease-out infinite;pointer-events:none;}" &
    ".pulse-Plant{border:2px solid rgba(58,123,213,0.8);}" &
    ".pulse-WH{border:2px solid rgba(39,174,96,0.8);}" &
    ".pulse-3PL{border:2px solid rgba(230,126,34,0.8);}" &
    ".pulse-Office{border:2px solid rgba(142,68,173,0.8);}" &
    "@keyframes pulse{0%{transform:scale(0.9);opacity:1;}70%{transform:scale(1.8);opacity:0;}100%{transform:scale(0.9);opacity:0;}}" &
    ".icon-core{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.32);transition:transform 0.2s,box-shadow 0.2s;}" &
    ".icon-Plant{background:linear-gradient(145deg,#1E3A5F,#3a7bd5);}" &
    ".icon-WH{background:linear-gradient(145deg,#1A4731,#27ae60);}" &
    ".icon-3PL{background:linear-gradient(145deg,#7d3c00,#e67e22);}" &
    ".icon-Office{background:linear-gradient(145deg,#4a235a,#8e44ad);}" &
    ".icon-core svg{width:17px;height:17px;fill:white;display:block;}" &

    "/* ── Popup ── */" &
    ".leaflet-popup-content-wrapper{padding:0;border-radius:14px;border:none;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.2);}" &
    ".leaflet-popup-content{margin:0!important;}" &
    ".leaflet-popup-tip-container{display:none;}" &
    ".leaflet-popup-close-button{color:rgba(255,255,255,0.85)!important;font-size:17px!important;top:7px!important;right:9px!important;}" &
    ".pc{width:240px;font-family:Segoe UI,sans-serif;}" &
    ".pc-header{padding:14px 16px;}" &
    ".pc-plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
    ".pc-wh{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
    ".pc-3pl{background:linear-gradient(135deg,#7d3c00,#e67e22);}" &
    ".pc-office{background:linear-gradient(135deg,#4a235a,#8e44ad);}" &
    ".pc-badge{display:inline-block;background:rgba(255,255,255,0.2);color:white;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:2px 8px;border-radius:20px;margin-bottom:6px;}" &
    ".pc-site{color:rgba(255,255,255,0.7);font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px;}" &
    ".pc-name{color:white;font-size:15px;font-weight:700;line-height:1.2;}" &
    ".pc-body{background:white;padding:12px 16px;}" &
    ".pc-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;}" &
    ".pc-sep{height:1px;background:#f0f0f0;margin:2px 0;}" &
    ".pc-label{font-size:11px;color:#999;font-weight:500;}" &
    ".pc-val{font-size:13px;font-weight:700;color:#1a1a1a;}" &
    ".kpi-green{color:#1A7A40;}" &

    "/* ── Search ── */" &
    "#searchWrap{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:1000;width:300px;}" &
    "#searchIcon{position:absolute;left:13px;top:50%;transform:translateY(-50%);font-size:13px;pointer-events:none;}" &
    "#searchBox{width:100%;padding:10px 16px 10px 38px;border:none;border-radius:24px;background:rgba(255,255,255,0.97);box-shadow:0 4px 20px rgba(0,0,0,0.22);font-size:13px;color:#1a1a1a;outline:none;}" &
    "#searchResults{margin-top:6px;background:white;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.18);display:none;}" &
    ".sr-item{padding:10px 14px;cursor:pointer;border-bottom:1px solid #f0f0f0;display:flex;align-items:center;gap:8px;transition:background 0.15s;}" &
    ".sr-item:hover{background:#f5f9ff;}" &
    ".sr-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}" &
    ".sr-dot-Plant{background:#3a7bd5;}" &
    ".sr-dot-WH{background:#27ae60;}" &
    ".sr-dot-3PL{background:#e67e22;}" &
    ".sr-dot-Office{background:#8e44ad;}" &
    ".sr-dot-Virtual{background:#95a5a6;}" &
    ".sr-name{font-size:13px;font-weight:600;color:#1a1a1a;}" &
    ".sr-site{font-size:11px;color:#aaa;}" &

    "/* ── Toggle buttons ── */" &
    "#toggleWrap{position:absolute;top:16px;right:16px;z-index:1000;display:flex;gap:6px;flex-wrap:wrap;max-width:280px;justify-content:flex-end;}" &
    ".tbtn{padding:7px 12px;border:none;border-radius:20px;font-size:11px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:all 0.2s;letter-spacing:0.3px;}" &
    ".tbtn-on-Plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);color:white;}" &
    ".tbtn-on-WH{background:linear-gradient(135deg,#1A4731,#27ae60);color:white;}" &
    ".tbtn-on-3PL{background:linear-gradient(135deg,#7d3c00,#e67e22);color:white;}" &
    ".tbtn-on-Office{background:linear-gradient(135deg,#4a235a,#8e44ad);color:white;}" &
    ".tbtn-on-Virtual{background:linear-gradient(135deg,#555,#95a5a6);color:white;}" &
    ".tbtn-off{background:rgba(255,255,255,0.75);color:#bbb;box-shadow:none;}" &

    "/* ── Legend ── */" &
    ".legend{position:absolute;bottom:24px;right:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:12px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);}" &
    ".legend-title{font-size:9px;font-weight:700;color:#bbb;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}" &
    ".li{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:500;color:#444;margin-bottom:5px;}" &
    ".li:last-child{margin-bottom:0;}" &
    ".ld{width:10px;height:10px;border-radius:3px;}" &
    ".ld-Plant{background:linear-gradient(135deg,#1E3A5F,#3a7bd5);}" &
    ".ld-WH{background:linear-gradient(135deg,#1A4731,#27ae60);}" &
    ".ld-3PL{background:linear-gradient(135deg,#7d3c00,#e67e22);}" &
    ".ld-Office{background:linear-gradient(135deg,#4a235a,#8e44ad);}" &

    "/* ── Counter ── */" &
    "#counter{position:absolute;bottom:24px;left:16px;z-index:999;background:rgba(255,255,255,0.97);border-radius:12px;padding:10px 16px;box-shadow:0 4px 20px rgba(0,0,0,0.13);font-size:12px;color:#777;}" &
    "#counter b{font-size:15px;color:#1E3A5F;}" &

    "/* ── Virtual Panel ── */" &
    "#virtualPanel{position:absolute;top:0;right:0;height:100%;width:320px;background:rgba(255,255,255,0.97);box-shadow:-6px 0 30px rgba(0,0,0,0.15);z-index:1001;display:none;flex-direction:column;}" &
    "#virtualHeader{padding:18px 20px 14px;background:linear-gradient(135deg,#555,#95a5a6);}" &
    "#virtualHeader h3{color:white;font-size:14px;font-weight:700;margin-bottom:2px;}" &
    "#virtualHeader p{color:rgba(255,255,255,0.75);font-size:11px;}" &
    "#virtualClose{position:absolute;top:14px;right:16px;background:none;border:none;color:white;font-size:20px;cursor:pointer;line-height:1;}" &
    "#virtualList{overflow-y:auto;flex:1;padding:12px;}" &
    ".vc{background:white;border-radius:10px;margin-bottom:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.08);border:1px solid #f0f0f0;}" &
    ".vc-top{padding:10px 14px;background:linear-gradient(135deg,#f8f9fa,#eee);}" &
    ".vc-site{font-size:9px;font-weight:700;color:#999;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:2px;}" &
    ".vc-name{font-size:13px;font-weight:700;color:#1a1a1a;}" &
    ".vc-body{padding:10px 14px;display:flex;gap:0;}" &
    ".vc-kpi{flex:1;}" &
    ".vc-label{font-size:10px;color:#aaa;font-weight:500;}" &
    ".vc-val{font-size:13px;font-weight:700;color:#1a1a1a;}" &
    ".vc-val-green{font-size:13px;font-weight:700;color:#1A7A40;}" &
    ".vc-div{width:1px;background:#f0f0f0;margin:0 10px;}" &
    "</style></head><body>" &
    "<div id='map'></div>" &

    "<div id='searchWrap'><span id='searchIcon'>🔍</span><input id='searchBox' type='text' placeholder='Search location or site...' autocomplete='off'/><div id='searchResults'></div></div>" &

    "<div id='toggleWrap'>" &
    "<button id='btnWH'      class='tbtn tbtn-on-WH'      onclick='toggleType(""WH"")'>🏬 WH</button>" &
    "<button id='btn3PL'     class='tbtn tbtn-on-3PL'     onclick='toggleType(""3PL"")'>🚚 3PL</button>" &
    "<button id='btnOffice'  class='tbtn tbtn-on-Office'  onclick='toggleType(""Office"")'>🏢 Office</button>" &
    "<button id='btnPlant'   class='tbtn tbtn-on-Plant'   onclick='toggleType(""Plant"")'>🏭 Plant</button>" &
    "<button id='btnVirtual' class='tbtn tbtn-on-Virtual' onclick='toggleVirtual()'>🌐 Virtual</button>" &
    "</div>" &

    "<div class='legend'>" &
    "<div class='legend-title'>Location Type</div>" &
    "<div class='li'><div class='ld ld-WH'></div>Warehouse</div>" &
    "<div class='li'><div class='ld ld-3PL'></div>3PL Logistic</div>" &
    "<div class='li'><div class='ld ld-Office'></div>Office</div>" &
    "<div class='li'><div class='ld ld-Plant'></div>Plant</div>" &
    "</div>" &
    "<div id='counter'>Showing <b id='cnt'>0</b> locations</div>" &

    "<div id='virtualPanel'>" &
    "<div id='virtualHeader'>" &
    "<h3>🌐 Virtual Locations</h3>" &
    "<p>No physical coordinates</p>" &
    "<button id='virtualClose' onclick='toggleVirtual()'>×</button>" &
    "</div>" &
    "<div id='virtualList'></div>" &
    "</div>" &

    "<script>" &
    "var map=L.map('map',{zoomControl:false}).setView([25.7,-100.3],4);" &
    "L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'© Nidec'}).addTo(map);" &
    "L.control.zoom({position:'bottomleft'}).addTo(map);" &

    "function makeIcon(t){" &
    "var ic='icon-'+t;" &
    "var pc='pulse-'+t;" &
    "var svgs={" &
    "WH:'<svg viewBox=""0 0 24 24""><path d=""M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z""/></svg>'," &
    "Plant:'<svg viewBox=""0 0 24 24""><path d=""M10 20h4V4h-4v16zm-6 0h4v-8H4v8zm12-12v12h4V8h-4z""/></svg>'," &
    "Office:'<svg viewBox=""0 0 24 24""><path d=""M17 11V3H7v4H3v14h8v-4h2v4h8V11h-4zm-8 4H7v-2h2v2zm0-4H7V9h2v2zm0-4H7V5h2v2zm4 8h-2v-2h2v2zm0-4h-2V9h2v2zm0-4h-2V5h2v2zm4 8h-2v-2h2v2zm0-4h-2V9h2v2z""/></svg>'," &
    "3PL:'<svg viewBox=""0 0 24 24""><path d=""M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm13.5-9l1.96 2.5H17V9.5h2.5zm-1.5 9c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z""/></svg>'" &
    "};" &
    "var sv=svgs[t]||svgs['Plant'];" &
    "return L.divIcon({" &
    "html:'<div class=""icon-wrap""><div class=""pulse-ring '+pc+'""></div><div class=""icon-core '+ic+'"">'+sv+'</div></div>'," &
    "className:''," &
    "iconSize:[40,40]," &
    "iconAnchor:[20,20]," &
    "popupAnchor:[0,-24]" &
    "});}" &

    "var mcg=L.markerClusterGroup({" &
    "showCoverageOnHover:false," &
    "maxClusterRadius:60," &
    "spiderfyOnMaxZoom:true," &
    "disableClusteringAtZoom:10," &
    "iconCreateFunction:function(c){" &
    "var n=c.getChildCount();" &
    "return L.divIcon({html:'<div style=""background:rgba(30,58,95,0.88);color:white;border-radius:50%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;box-shadow:0 3px 10px rgba(0,0,0,0.3);border:2px solid rgba(255,255,255,0.4)"">'+n+'</div>'," &
    "className:'',iconSize:[36,36]});}" &
    "}).addTo(map);" &

    "var markers=[];var allMarkers=[];var typeOn={WH:true,Plant:true,Office:true,'3PL':true};" &
    "var virtualData=[];var virtualVisible=false;" &

    _DataPoints &
    _VirtualCards &

    "document.getElementById('cnt').textContent=markers.length;" &
    "var grp=L.featureGroup(markers);" &
    "if(grp.getLayers().length>0){map.fitBounds(grp.getBounds().pad(0.15));}" &

    "function updateCnt(){document.getElementById('cnt').textContent=allMarkers.filter(function(x){return mcg.hasLayer(x.marker);}).length;}" &

    "function toggleType(t){" &
    "typeOn[t]=!typeOn[t];" &
    "document.getElementById('btn'+t).className=typeOn[t]?'tbtn tbtn-on-'+t:'tbtn tbtn-off';" &
    "allMarkers.forEach(function(x){" &
    "if(x.type===t){typeOn[t]?mcg.addLayer(x.marker):mcg.removeLayer(x.marker);}" &
    "});updateCnt();}" &

    "function toggleVirtual(){" &
    "virtualVisible=!virtualVisible;" &
    "var panel=document.getElementById('virtualPanel');" &
    "var btn=document.getElementById('btnVirtual');" &
    "if(virtualVisible){" &
    "panel.style.display='flex';" &
    "btn.className='tbtn tbtn-on-Virtual';" &
    "var list=document.getElementById('virtualList');" &
    "list.innerHTML='';" &
    "if(virtualData.length===0){list.innerHTML='<p style=""padding:20px;color:#aaa;text-align:center;font-size:13px;"">No virtual locations found</p>';return;}" &
    "virtualData.forEach(function(v){" &
    "var card=document.createElement('div');" &
    "card.className='vc';" &
    "card.innerHTML='<div class=""vc-top""><div class=""vc-site"">'+v.site+'</div><div class=""vc-name"">'+v.name+'</div></div><div class=""vc-body""><div class=""vc-kpi""><div class=""vc-label"">💰 Inventory Cost</div><div class=""vc-val"">'+v.cost+'</div></div><div class=""vc-div""></div><div class=""vc-kpi""><div class=""vc-label"">📈 Total Sales</div><div class=""vc-val-green"">'+v.sales+'</div></div></div>';" &
    "list.appendChild(card);});" &
    "}else{" &
    "panel.style.display='none';" &
    "btn.className='tbtn tbtn-off';" &
    "}}" &

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
    "d.onclick=function(){" &
    "mcg.zoomToShowLayer(x.marker,function(){x.marker.openPopup();});" &
    "sb.value=x.displayName;sr.style.display='none';" &
    "};sr.appendChild(d);});" &
    "sr.style.display='block';});" &
    "document.addEventListener('click',function(e){" &
    "if(!document.getElementById('searchWrap').contains(e.target)){sr.style.display='none';}});" &
    "</script></body></html>"

RETURN _HTML