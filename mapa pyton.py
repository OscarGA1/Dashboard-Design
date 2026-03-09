import pandas as pd
import plotly.express as px

df = dataset[["Latitude", "Longitude", "Location Name", "Type"]].dropna()

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Type",
    hover_name="Location Name",
    hover_data={
        "Type": True,
        "Latitude": False,
        "Longitude": False
    },
    color_discrete_map={
        "Plant": "#1E3A5F",
        "WH":    "#2D7A50"
    },
    size_max=14,
    zoom=3,
    mapbox_style="carto-positron"
)

fig.update_traces(marker=dict(size=12))
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        bgcolor="white",
        bordercolor="#ccc",
        borderwidth=1,
        font=dict(size=11)
    )
)

fig.show()
```

---

### Cómo pegarlo en Power BI paso a paso

1. En tu reporte ve a **Insertar → Visual de Python**
2. En el panel de campos arrastra desde `General Information`:
   - `Latitude`
   - `Longitude`
   - `Location Name`
   - `Type`
3. Pega el código en el editor que aparece abajo
4. Dale al botón **▶ Ejecutar**

---

### Antes de correrlo verifica esto en tu PC

Abre **CMD** y ejecuta:
```
pip install plotly pandas