Mapa_Nidec_HTML =
VAR _DataPoints =
    CONCATENATEX(
        'General Information',
        "L.marker([" & 'General Information'[Latitude] & ", " & 'General Information'[Longitude] & "], {icon: " &
        IF('General Information'[Type] = "WH", "iconWH", "iconPlant") &
        "}).addTo(map).bindPopup(`
            <div class='popup-card'>
                <div class='popup-header " & IF('General Information'[Type] = "WH", "popup-wh", "popup-plant") & "'>
                    <span class='popup-icon'>" & IF('General Information'[Type] = "WH", "🏬", "🏭") & "</span>
                    <span class='popup-type'>" & 'General Information'[Type] & "</span>
                </div>
                <div class='popup-body'>
                    <div class='popup-name'>" & 'General Information'[Location name] & "</div>
                    <div class='popup-coords'>
                        <span>📍 " & 'General Information'[Latitude] & ", " & 'General Information'[Longitude] & "</span>
                    </div>
                </div>
            </div>
        `);",
        " "
    )

VAR _HTML =
"data:text/html;charset=utf-8,<!DOCTYPE html><html><head>
<meta charset='UTF-8'>
<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>
<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family: 'Segoe UI', sans-serif; }
    #map { height:100vh; width:100vw; }

    /* ── Iconos ── */
    .icon-wrap {
        display:flex; align-items:center; justify-content:center;
        width:38px; height:38px; border-radius:50%;
        box-shadow: 0 3px 10px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor:pointer;
    }
    .icon-wrap:hover {
        transform: scale(1.2) translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }
    .icon-plant { background: linear-gradient(135deg, #1E3A5F, #2D5A8E); }
    .icon-wh    { background: linear-gradient(135deg, #1A4731, #2D7A50); }
    .icon-wrap svg { width:20px; height:20px; fill:white; }

    /* ── Pulse ring ── */
    .pulse-ring {
        position:absolute; width:38px; height:38px;
        border-radius:50%; animation: pulse 2s infinite;
    }
    .pulse-plant { border: 2px solid #2D5A8E; }
    .pulse-wh    { border: 2px solid #2D7A50; }
    @keyframes pulse {
        0%   { transform:scale(1);   opacity:0.8; }
        70%  { transform:scale(1.6); opacity:0;   }
        100% { transform:scale(1);   opacity:0;   }
    }

    /* ── Popup ── */
    .leaflet-popup-content-wrapper {
        padding:0; border-radius:12px;
        overflow:hidden; border:none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        min-width:200px;
    }
    .leaflet-popup-content { margin:0; }
    .leaflet-popup-tip-container { display:none; }

    .popup-card { font-family:'Segoe UI',sans-serif; }
    .popup-header {
        display:flex; align-items:center; gap:8px;
        padding:10px 14px;
    }
    .popup-plant { background: linear-gradient(135deg, #1E3A5F, #2D5A8E); }
    .popup-wh    { background: linear-gradient(135deg, #1A4731, #2D7A50); }
    .popup-icon  { font-size:18px; }
    .popup-type  {
        color:white; font-size:11px; font-weight:600;
        letter-spacing:1.5px; text-transform:uppercase;
        opacity:0.9;
    }
    .popup-body  { padding:12px 14px; background:white; }
    .popup-name  {
        font-size:14px; font-weight:700;
        color:#1a1a1a; margin-bottom:6px;
    }
    .popup-coords {
        font-size:11px; color:#888;
        display:flex; align-items:center; gap:4px;
    }

    /* ── Legend ── */
    .legend {
        position:absolute; bottom:28px; right:12px; z-index:999;
        background:white; border-radius:10px;
        padding:12px 16px;
        box-shadow:0 4px 16px rgba(0,0,0,0.12);
        font-family:'Segoe UI',sans-serif;
    }
    .legend-title {
        font-size:10px; font-weight:700; color:#888;
        letter-spacing:1.2px; text-transform:uppercase;
        margin-bottom:8px;
    }
    .legend-item {
        display:flex; align-items:center;
        gap:8px; font-size:12px; color:#333;
        margin-bottom:6px;
    }
    .legend-dot {
        width:12px; height:12px; border-radius:50%;
    }
    .dot-plant { background: linear-gradient(135deg, #1E3A5F, #2D5A8E); }
    .dot-wh    { background: linear-gradient(135deg, #1A4731, #2D7A50); }
</style>
</head><body>
<div id='map'></div>
<div class='legend'>
    <div class='legend-title'>Locations</div>
    <div class='legend-item'><div class='legend-dot dot-plant'></div> Plant</div>
    <div class='legend-item'><div class='legend-dot dot-wh'></div> Warehouse</div>
</div>
<script>
    var map = L.map('map', { zoomControl:false }).setView([25.7, -100.3], 4);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© Nidec Operations'
    }).addTo(map);

    L.control.zoom({ position:'topleft' }).addTo(map);

    function makeIcon(type) {
        var cls   = type === 'WH' ? 'icon-wh'    : 'icon-plant';
        var pulse = type === 'WH' ? 'pulse-wh'   : 'pulse-plant';
        var svg   = type === 'WH'
            ? '<svg viewBox=""0 0 24 24""><path d=""M10 20v-6h4v6h5v-8l-7-5-7 5v8z""/></svg>'
            : '<svg viewBox=""0 0 24 24""><path d=""M10 20h4V4h-4v16zm-6 0h4v-8H4v8zm12-12v12h4V8h-4z""/></svg>';
        return L.divIcon({
            html: '<div class=""pulse-ring ' + pulse + '""></div><div class=""icon-wrap ' + cls + '"">' + svg + '</div>',
            className: '',
            iconSize:   [38, 38],
            iconAnchor: [19, 19],
            popupAnchor:[0, -22]
        });
    }

    var iconWH    = makeIcon('WH');
    var iconPlant = makeIcon('Plant');

    var markers = [];
    " & _DataPoints & "

    var group = L.featureGroup(markers);
    if(group.getLayers().length > 0) {
        map.fitBounds(group.getBounds().pad(0.15));
    }
</script>
</body></html>"

RETURN _HTML