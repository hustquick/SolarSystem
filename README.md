# SolarSystem
Use Python to write the code for solar system

- `TroughCollector.py` describes a trough collector that has a vacuum tube.
- `DishCollector.py` describes a dish collector that has a receiver with an absorber.
- `PowerTower.py` describes a power tower with heliostats.
- `Stream.py` describes the properties of a stream. For a stream, properties of fluid, temperature, pressure, quality 
can be set. Properties of h, s, u, cp are dependent. They can be automatically obtained when `temperature`, 
`pressure`, and `quality` are properly set. They can not be set. Temperature, pressure, quality are interrelated. 
A flag `pressure_dependent` is set to identify whether the stream is pressure-dependent or temperature-dependent.
