Configuring the run
===================
You can configure the run using `configs/` files:

- world: `config_create_world.yaml` for social environments
- example: `config_example.yaml` (see the number of days etc.)
- geography: call:
  ```
  Geography.from_file({"super_area": ["E02003282", "E02001720", "E00088544", "E02002560", "E02002559", "E02004314",]})
  ```
  the `E` stuff are coordinates for areas and superareas (in `data/input/geography/area_coordinates.csv` and `data/input/geography/super_area_coordinates.csv`) - that one above has: World length 46784; adding say "E02004900" increases it to 54947; my current test run:
  ```
  geography = Geography.from_file({"super_area": ["E02003282", "E02001720", "E00088544", "E02002560", "E02002559", "E02004314", "E02004900", "E02005758"]})
  ```
  which is 63277.
