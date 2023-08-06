.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-27
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.bookmark.drama.location

In a room
=========

{0}

Auditorium
----------

.. condition:: PLAYER.state tos.map.Map.Location.auditorium

The Auditorium has seats for about 150 people in two blocks.

Steps lead up to the rear exit.

The curtains to the stage are drawn closed.

Backstage
---------

.. condition:: PLAYER.state tos.map.Map.Location.backstage

|PLAYER| stands in a long corridor of breeze block, painted white.

There are a couple of dressing rooms here, and a small toilet.

Balcony
-------

.. condition:: PLAYER.state tos.map.Map.Location.balcony

|PLAYER| is standing on the narrow Balcony behind the Auditorium.

Through a door is the Lighting Box. Downstairs is the Bar.

Bar
---

.. condition:: PLAYER.state tos.map.Map.Location.bar

|PLAYER| contemplates the Bar.

It's an L-shaped space around the Kitchen counter.

A window looks out over the Car Park to the lane beyond.

Car Park
--------

.. condition:: PLAYER.state tos.map.Map.Location.car_park

|PLAYER| is outside in the Car Park. There is an exit on to a lane which meets the main road.

Foyer
-----

.. condition:: PLAYER.state tos.map.Map.Location.foyer

In the Foyer again, it is chilly.

Cloaks
------

.. condition:: PLAYER.state tos.map.Map.Location.cloaks

The Cloakroom is an oddly elongated space with an open counter on to the Foyer.

Corridor
--------

.. condition:: PLAYER.state tos.map.Map.Location.corridor

The Corridor is draughty, and the carpet worn.

It runs the length of the Auditorium and ends in a door to Backstage.

Costume
-------

.. condition:: PLAYER.state tos.map.Map.Location.costume

The Costume Room is chilly, and slightly damp.

Racks of clothing take up some of the space. The rest is given over to lighting equipment and crates of props.

Kitchen
-------

.. condition:: PLAYER.state tos.map.Map.Location.kitchen

The Kitchen is simply equipped.

There are two or three cupboards, a fridge, and a sink with a water boiler above it.

Under the counter are cups, plates and glasses.

Lighting
--------

.. condition:: PLAYER.state tos.map.Map.Location.lighting

The Lighting Box has room for two people. 

The control panel is roughly framed. It has a patch bay and a mixer for sound.

There are variac controls for the lighting.
There is a fuse box on the far wall.

There is a glass panel looking out over the Auditorium to the Stage.

A couple of tall stools are the only furniture.

Passage
-------

.. condition:: PLAYER.state tos.map.Map.Location.passage

The Passage is draughty, and the carpet worn.

It runs the length of the Auditorium and ends in a door to Backstage.

Stage
-----

.. condition:: PLAYER.state tos.map.Map.Location.stage

The Stage is quite dark, lit only by pale round working lights.

The scene is set for a bedroom and balcony. There is a Central European feel to the blankets and drapery.

Stairs
------

.. condition:: PLAYER.state tos.map.Map.Location.stairs

A zig-zag stairway between the Bar and the Balcony.

It runs the length of the Auditorium and ends in a door to Backstage.

Wings
-----

.. condition:: PLAYER.state tos.map.Map.Location.wings

Either side of the Stage is framed by black wooden panels. They are angled to allow three ways on and off.

The walls are of black painted brick.

Overhead is the lighting gantry.
