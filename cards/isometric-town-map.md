# Isometric town map

Source: https://github.com/mapeditor/tiled — GPL-2.0 or later. About 12.9k stars. Release 1.12.2, 27 May 2026. The map orientations are documented at https://doc.mapeditor.org/manual/maps/.

Rule. A big top-down isometric town is a Tiled map. Set the orientation to Isometric, or to Isometric (Staggered) when the map should stay rectangular. Make the map larger than one screen. The picture on screen is a render of that map. Do not paint the town as one generated image.

Tiled does not ship the tiles. The tileset is original art, or a pack with its own license. The editor being GPL does not make the map file GPL.

Leave. Do not vendor Tiled. Do not copy another game's tiles into the map.

These do not do this job:

- https://github.com/deepnight/ldtk — MIT, about 4.3k stars. Isometric tiles were refused in issue 944.
- https://github.com/markusmoenig/Eldiron — MIT, about 824 stars, docs current as of October 2026. It builds 3D geometry and looks at it with an isometric camera. Its author says that is not an isometric tile map. Use it for a 3D town, not for this map.
- One-shot image generators, and diffusion tile tools such as https://github.com/charmed-ai/tilemapgen, paint a poster. They are how the last village plates failed.
