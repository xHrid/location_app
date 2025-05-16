import os, math, requests
import geopandas as gpd

# === Load strata.geojson and get bounds ===
gdf = gpd.read_file('strata.geojson')
minx, miny, maxx, maxy = gdf.total_bounds

# === Lat/Lon → Tile coords ===
def deg2num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    return (
        int((lon + 180.0) / 360.0 * n),
        int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    )

# === Download function with headers & fallback ===
HEADERS = {
    'User-Agent': 'MyOfflineMapApp/1.0 (your.email@example.com)'
}
def fetch_tile(z, x, y):
    urls = [
        f"https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        f"https://{['a','b','c'][x%3]}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
    ]
    out_dir = f"tiles/{z}/{x}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{y}.png"

    if os.path.exists(out_path):
        return
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                with open(out_path, 'wb') as f:
                    f.write(r.content)
                print(f"Saved: {z}/{x}/{y}.png from {url}")
                return
        except Exception as e:
            pass
    print(f"Failed to fetch tile {z}/{x}/{y}")

# === Main download loop ===
for z in [17, 18]:
    x_min, y_max = deg2num(miny, minx, z)
    x_max, y_min = deg2num(maxy, maxx, z)
    print(f"Zoom {z}: x {x_min}→{x_max}, y {y_min}→{y_max}")
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            fetch_tile(z, x, y)
