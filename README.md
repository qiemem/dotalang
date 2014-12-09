DOTA Message Extractor
===

Run as follows:

    python messages.py replay.dem [replay2.dem replay3.dem ...]

Message data will be printed as JSON to stdout. You can then just pipe the output into a file:

    python messages.py replay.dem > messages.json

Dependencies
---

[smoke](https://github.com/skadistats/smoke), which does the actual parsing. See its page for installation instructions.

