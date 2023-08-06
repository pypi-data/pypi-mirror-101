.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-03
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.leader
            tos.mixins.types.Proximity.present

.. entity:: PUZZLE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.foyer

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name

Lionheart
=========

{0}

Ignorant
--------

.. condition:: EDWARD.state tos.mixins.types.Awareness.ignorant

|EDWARD| is here.

He is a tall man with grey hair swept back in an elaborate quiff.
He contemplates |PLAYER| with narrowed eyes.

[EDWARD]_

    Good evening |PLAYER|, are you well?

[PLAYER]_

    Hello Edward; yes. A bit nervous.

[EDWARD]_

    First night, yes.

    What fear I a moon battle? Let infamy flee the dawn; on the bones of dread fortune will we set our throne!

|EDWARD|'s eyebrows arch dramatically. The glow of a green exit sign catches the side of his ruddy, aquiline nose.

.. property:: EDWARD.state tos.mixins.types.Awareness.discover

Lights
------

.. condition:: PUZZLE.state tos.mixins.types.Significance.notknown

[EDWARD]_

    That mob of hoodlums is hanging around outside.
    Would you make sure to keep the security lights switched on?
    We don't want any more damage to the cars.

.. property:: PUZZLE.state tos.mixins.types.Significance.indicate

Reminder
--------

.. condition:: PUZZLE.state tos.mixins.types.Significance.emphasis

[EDWARD]_

    Don't forget those lights, |PLAYER|.

