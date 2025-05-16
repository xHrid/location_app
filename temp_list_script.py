from pathlib import Path

tiles = Path('tiles')
urls = []

for p in tiles.rglob("*.png"):
    urls.append('/' + str(p).replace("\\", "/"))  # For Windows compatibility

with open("tile_urls.txt", "w") as f:
    f.writelines(f"  '{url}',\n" for url in urls)
