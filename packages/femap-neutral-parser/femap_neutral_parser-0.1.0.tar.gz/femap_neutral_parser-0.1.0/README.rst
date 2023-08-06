====================
FEMAP neutral Parser
====================


FEMAP neutral file parser


* Free software: MIT license


Features and limitations
------------------------

Parse and render FEMAP neutral files. For now, three blocks are interpreted:

* Block 100 "Neutral File Header"
* Block 450 "Output Sets"
* Block 451 "Output Data Vectors"

Additionally, MYSTRAN outputs (which makes use of different titles than FEMAP) are harmonized: Access to total translation using the same title as FEMAP ("Total Translation" *vs* "RSS translations").

