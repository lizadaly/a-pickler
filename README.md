# A Pickler for the Knowing Ones

A translator and generator to produce text in the form of [A Pickle for the Knowing Ones](https://www.gutenberg.org/cache/epub/43453/pg43453-images.html) (1802)
by noted eccentric [Timothy Dexter](https://en.wikipedia.org/wiki/Timothy_Dexter). The final output will be an entry in National Novel Generation Month 2021.

This repo will contain three utilities:

- A concordance generator, to iterate through the source of _A Pickle for the Knowing Ones_ and generate a map of Dexter's spellings to standard English. The program should suggest words, skip known words, and store the condordance.
- A script, `pickler.py`, to take an input text and turn it into a Dexter-style rendering. (To be started on or after November 1.)
- A script, `unpickler.py`, which reverses the process and turns a Dexter-style document into plain-ish English. (To be started on or after November 1.)

The pickler/depickler process will necessarily be lossy, but it should also be funny.
