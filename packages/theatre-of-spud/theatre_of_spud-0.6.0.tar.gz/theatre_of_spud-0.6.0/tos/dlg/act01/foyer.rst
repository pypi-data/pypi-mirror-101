.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing
            tos.map.Map.Location.foyer

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.leader

.. entity:: PUZZLE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.foyer

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |EDWARD| property:: EDWARD.name
.. |LOCALE| property:: STORY.bookmark.drama.scenery
.. |PUZZLE| property:: PUZZLE.name

Foyer
=====

{0}

.. property:: STORY.prompt ?

Ignorant
--------

.. condition:: STORY.bookmark.tally[foyer] 0

The Foyer is carpeted grey and gloomy.

The Box Office and Cloakroom are in darkness.

There are doors to a Corridor on the left.

Further on is the Bar area.


.. property:: EDWARD.state tos.mixins.types.Mode.default

Indicate
--------

.. condition:: PUZZLE.state tos.mixins.types.Significance.indicate

|PLAYER| notices the |PUZZLE|.

.. property:: PUZZLE.state tos.mixins.types.Significance.emphasis

Discover
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.discover

|PLAYER| studies the |PUZZLE|.

Familiar
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.familiar

|PLAYER| wonders what to do about the |PUZZLE|.

Approach
--------

.. condition:: EDWARD.state tos.mixins.types.Proximity.outside

|PLAYER| hears someone coming.

Leaving
-------

.. condition:: EDWARD.state tos.mixins.types.Proximity.outward

|EDWARD| leaves abruptly.

Hint
----

.. condition:: DRAMA.history[0].args[0] hint

I wonder if there's anyone around?

Complete
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.complete

There is the sound of conversation from the Bar.

[PLAYER]_

    I wonder who that could be?

.. property:: STORY.state 2
