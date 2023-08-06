.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: SPUD
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Proximity.present
            tos.types.Motivation.acting
            tos.mixins.types.Significance.emphasis

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name


News
====

Ignorant
--------

.. condition:: SPUD.state tos.mixins.types.Awareness.ignorant

Spud is standing backstage.

He's about ten years old, slightly chubby, with a pale face and sandy hair.

He looks cold in his tatty green bomber jacket.
His blue denim jeans are too long for him, and turn up excessively at the ankle.
He is wearing black school shoes.


.. property:: SPUD.state tos.mixins.types.Awareness.discover

Danny
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Danny

[PLAYER]_

    Spud, I've got a message from Edward. Is there any way you could fill in and play the Officer in Act One please?

[SPUD]_

    So where's Danny?

[PLAYER]_

    Danny's gone to the football.

    Have you got a script?

[SPUD]_

    I don't think I'll need the script. I can remember.

    Can I still be the dog as well?

[PLAYER]_

    Yes of course you can.

    Thank you!

.. property:: SPUD.state tos.mixins.types.Significance.elevated

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[PLAYER]_

    Spud, what a mess.

[SPUD]_

    What's up?

[PLAYER]_

    Spud, I've just come from Ed.

    Do you think you might be able to quickly learn the lines for Bluntschli?

[SPUD]_

    What's happened to Michael?

[PLAYER]_

    He's gone with his Dad to the football.

[SPUD]_

    I sort of know most of it anyway.

    But won't I also have to be the Officer?

[PLAYER]_

    Edward thinks it will work if you do a costume change on the balcony.

    He'll come and talk you through it later on.

[SPUD]_

    All right.

.. property:: SPUD.state tos.mixins.types.Significance.elevated

Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[PLAYER]_

    We've just heard; a bit of a shock. Hayley's not coming in tonight.

    So we need someone to play Louka.

[SPUD]_

    Is she at the...

[PLAYER]_

    The football, yes.

    Spud, you can say no if you don't want to do it.

[SPUD]_

    Doesn't she have to kiss Sergius?

[PLAYER]_

    Yes, I think she does.

[SPUD]_

    That's okay.

[PLAYER]_

    Good lad.

.. property:: SPUD.state tos.mixins.types.Significance.elevated

