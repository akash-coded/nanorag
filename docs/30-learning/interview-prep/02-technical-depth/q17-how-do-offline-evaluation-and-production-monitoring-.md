# Q17 · How do offline evaluation and production monitoring complement each other?


Offline gates the release: deterministic, fast, runs on every change, and blocks a merge on a
regression. It cannot tell you about terminology your users started using last week.

Production has no labels but has reality: escalation rate, citation click-through, thumbs-down,
the questions people actually ask. Its job is to supply the failures that become next quarter's
regression cases.

The loop between them is the thing to name: **every production failure that gets a human
verdict becomes a new offline regression case.** Without that feed, your offline set slowly
becomes a mirror of your own retriever's blind spots, and it will keep passing while your users
suffer. I would also run the offline suite nightly on unchanged code, which is not redundant —
it is how you detect corpus drift, upstream model updates and judge drift, three things that
change your system without anyone committing anything.
