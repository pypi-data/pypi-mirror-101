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
   :states: tos.types.Motivation.leader
            tos.mixins.types.Proximity.present

.. entity:: SPUD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.acting

.. entity:: PHONE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.office
            tos.mixins.types.Significance.suppress

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name


Message
=======

{0}

Danny
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Danny

[EDWARD]_

    |PLAYER|, was that the telephone ringing earlier?

[PLAYER]_

    That was Danny's mother. They want him to go to the football tonight instead.

[EDWARD]_

    Hmm. Oh well.

    We'll need someone to stand in for the Officer.

    That's fine. It's only a few lines.

[PLAYER]_

    What about Spud? He's already here.

[EDWARD]_

    Yes, why not? Would you go and let him know please |PLAYER|?

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[EDWARD]_

    Ah, |PLAYER|, what now?

[PLAYER]_

    It's Mikey. He's going to the football as well.

[EDWARD]_

    That's disappointing. Very disappointing.

    Of all the people to lose. Bluntschli.

[PLAYER]_

    Should we call it off do you think?

[EDWARD]_

    Never. Where's Spud?

[PLAYER]_

    Bluntschli and the Officer. It's a lot to ask.

[EDWARD]_

    But, as 'tis, we cannot miss him.
    He serves in offices that profit us.

    Go now, |PLAYER| and tell him to get ready.

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[EDWARD]_

    Ah, |PLAYER|, what now?

[PLAYER]_

    I know don't how how to say this, but...

[EDWARD]_

    Which one is it?

[PLAYER]_

    Hayley.

[EDWARD]_

    Aaah! How they mock me! But I will not be defeated.

    Go and warn Spud he has more lines to learn.

[PLAYER]_

    Are you sure this will work?.

[EDWARD]_

    It will have to work.

    *Aside*

    These three have robbed me.

    And this demi-devil; for he's a bastard one,
    has plotted with them to take my life.

.. property:: SPUD.state tos.mixins.types.Significance.indicate

