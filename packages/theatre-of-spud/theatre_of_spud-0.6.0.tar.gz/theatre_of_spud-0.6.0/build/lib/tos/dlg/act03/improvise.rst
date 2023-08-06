.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Proximity.present
            tos.types.Motivation.leader

.. entity:: SPUD
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Proximity.present
            tos.types.Motivation.acting
            tos.mixins.types.Significance.elevated

.. entity:: PHONE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.office

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name


Improvise
=========

Danny
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Danny

[EDWARD]_

    You won't be needing the dog suit tonight, Spud.


.. property:: PHONE.state tos.mixins.types.Significance.accepted
.. property:: SPUD.state tos.mixins.types.Significance.diminish

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[EDWARD]_

    I'll pity thee. Take pains to make thee speak.
    Teach thee each hour one thing or other.


.. property:: PHONE.state tos.mixins.types.Significance.accepted
.. property:: SPUD.state tos.mixins.types.Significance.diminish

Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[PLAYER]_

    OK, so don't forget. In Act Three when you're Bluntschli, Nicola will take Louka's line about the post arriving.

Spud looks confused.

[EDWARD]_

    What, ho! Slave. Caliban!
    Thou earth, thou. Speak!

[SPUD]_

    You mean Nicola who plays Catherine?

[PLAYER]_

    No, Adam who plays Nicola.

[SPUD]_

    Got it.

[PLAYER]_

    I think. Err.

    Anyway, one of them will do it.

.. property:: PHONE.state tos.mixins.types.Significance.accepted
.. property:: SPUD.state tos.mixins.types.Significance.diminish

