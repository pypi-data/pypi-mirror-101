.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing
            tos.map.Map.Location.office

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.leader

.. entity:: PHONE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.office

.. entity:: FATHER
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.father

.. entity:: MOTHER
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.mother

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.bookmark.drama.scenery
.. |PHONE| property:: PHONE.name

Office
======

{0}

.. property:: STORY.prompt ?

Ignorant
--------

.. condition:: STORY.bookmark.tally[office] 0

The Box Office is a tiny room.

Behind |PLAYER| is the door back to the Foyer.
On the left is a split aluminium window facing the Foyer entrance.

There is a desk and a chair, and a rotary telephone fixed to the wall on the right.

There is nothing else here. Everything of value is locked away.


.. property:: EDWARD.state tos.mixins.types.Mode.default

Indicate
--------

.. condition:: PHONE.state tos.mixins.types.Significance.indicate

|PLAYER| notices the |PHONE|.


Discover
--------

.. condition:: PHONE.state tos.mixins.types.Awareness.discover

|PLAYER| studies the |PHONE|.

Familiar
--------

.. condition:: PHONE.state tos.mixins.types.Awareness.familiar

|PLAYER| wonders what to do about the |PHONE|.

Approach
--------

.. condition:: EDWARD.state tos.mixins.types.Proximity.outside

|PLAYER| hears someone coming.

Hint
----

.. condition:: DRAMA.history[0].args[0] hint

I wonder if there's anyone around?

