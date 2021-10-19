# A Pickler for the Knowing Ones

A translator and generator to produce text in the form of [A Pickle for the Knowing Ones](https://www.gutenberg.org/cache/epub/43453/pg43453-images.html) (1802)
by noted eccentric [Timothy Dexter](https://en.wikipedia.org/wiki/Timothy_Dexter). The final output will be an entry in National Novel Generation Month 2021.

This repo will contain three utilities:

- A concordance generator, to iterate through the source of _A Pickle for the Knowing Ones_ and generate a map of Dexter's spellings to standard English. The program should suggest words, skip known words, and store the concordance.
- A script, `pickler.py`, to take an input text and turn it into a Dexter-style rendering. (To be started on or after November 1.)
- A script, `unpickler.py`, which reverses the process and turns a Dexter-style document into plain-ish English. (To be started on or after November 1.)

The pickler/depickler process will necessarily be lossy, but it should also be funny.

## Concordance generator

This loops through the source text, breaking on word boundaries, and generates an ordered data structure like the following:

```
[original_word, spellchecked_word, is_spellchecked]
```

Initially the first two values are the same, and the last is false.

In the spellcheck pass, a text-based UI assists the transcriber by showing a window of context, with a selection
of spell-checked options (via autocomplete), or the transcriber can type in a new word:

```
╭────────────────────────────────────────────────────────────────────────────────╮
│ put in A Nuf here and thay may pepper and solt itt as they plese    ,, ,                                                                   │
╰────────────────────────────────────────────────────────────────────────────────╯
? [solt]: salt

```

Any words added replace the `spellchecked_word` value in the concordance, and flip the `is_spellchecked` bit. Re-running the program will resume at the last-checked word. On control-C (or at completion), the concordance is saved.
