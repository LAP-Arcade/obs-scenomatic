# obs-scenomatic

Change OBS scenes automatically depending on the processes found on your
computer.

This is different than OBS built-in "Automatic Scene Switcher" as it does not
rely on window titles but on process names instead. Some games do not create
traditional windows so they are not detected by OBS.

Example `config.yml`:

```yml
# default values
# client:
#   host: localhost
#   port: 4455
#   password: ''

default_scene: some_scene
collection: some_collection
profile: some_profile

scenes:
  # keys = OBS scene names
  DDR:
    match: [ddr.exe]
    delay: 20 # in seconds
  ITG: [itgmania.exe, notitg.exe, stepmania.exe] # implicit argument match
```
