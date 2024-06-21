from ..common import WARSAW
import folium
import pandas as pd
import plotly.express as px


def createPopupHtml(row: pd.Series) -> str:
    html = ""
    html += f"<b>Line:</b> {row.Lines}<br>"
    html += f"<b>Vehicle:</b> {row.VehicleNumber}<br>"
    html += f"<b>Time:</b> {row.Time}<br>"
    html += f"<b>Speed:</b> {row.v:.0f} km/h<br>"

    return html.replace(" ", "&nbsp;")


def getColor(speed: float):
    if speed < 10:
        color = "lightblue"
    elif 10 <= speed < 20:
        color = "blue"
    elif 20 <= speed < 30:
        color = "darkblue"
    elif 30 <= speed < 40:
        color = "lightgreen"
    elif 40 <= speed < 50:
        color = "green"
    elif 50 <= speed < 60:
        color = "darkgreen"
    elif 60 <= speed < 70:
        color = "orange"
    elif 70 <= speed < 80:
        color = "red"
    elif 80 <= speed <= 90:
        color = "darkred"
    elif 90 < speed:
        color = "black"

    return color


def createSpeedingsMap(locations: pd.DataFrame, filename) -> None:
    map = folium.Map(location=WARSAW, zoom_start=12)

    for row in locations.itertuples():
        folium.Marker(
            location=[row.Lat, row.Lon],
            popup=folium.Popup(createPopupHtml(row)),
            icon=folium.Icon(color=getColor(row.v), icon="bus", prefix="fa"),
        ).add_to(map)

    map.save(filename)
    print(f"Map saved: {filename}")


def createSpeedsDistribution(speeds: pd.DataFrame, filename) -> None:
    fig = px.histogram(speeds, x="v", title="Speeds Distribution")
    fig.write_html(filename)
    print(f"Speeds chart saved: {filename}")


def createLateDistribution(lateBuses: pd.DataFrame, filename) -> None:
    fig = px.histogram(lateBuses, x="LateMins", title="Late Buses Distribution")
    fig.write_html(filename)
    print(f"Late buses chart saved: {filename}")

def createNearbyLinesPieChart(lines, placename, filename) -> None:
    fig = px.pie(lines, names=lines.index, values=lines.values, title=f"Lines near {placename}")
    fig.write_html(filename)
    print(f"Nearby lines pie chart for {placename} saved: {filename}")

def createLateLinesBarChart(mll, filename) -> None:
    fig = px.bar(mll, x=mll.index, y=mll.values, title="Most Late Lines")
    fig.update_layout(yaxis_title="Number of late buses")
    fig.write_html(filename)
    print(f"Most late lines bar chart saved: {filename}")
