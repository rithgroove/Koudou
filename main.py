from src.model.map.osm_handler import OSMHandler
from os.path import join 

osm_file = join("osm_files","TX-To-TU.osm")

handler = OSMHandler()
handler.apply_file(osm_file)

print(temp)

