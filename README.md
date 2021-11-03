# A Pickler for the Knowing Ones

A translator and generator to produce text in the form of [A Pickle for the Knowing Ones](https://www.gutenberg.org/cache/epub/43453/pg43453-images.html) (1802)
by noted eccentric [Timothy Dexter](https://en.wikipedia.org/wiki/Timothy_Dexter). The final output will be an entry in National Novel Generation Month 2021.

This repo contains the following utilities:

[] A dictionary generator, to iterate through the source of _A Pickle for the Knowing Ones_ and generate a map of Dexter's spellings to standard English. The program should suggest words, skip known words, and store the dictionary.
[] A script, `pickler.py`, to take an input text and turn it into a Dexter-style rendering. (To be started on or after November 1.)
[] A programmatic downloader for the source data, `filings.py` to be SEC quarterly earnings reports from Telsa, Inc.

## Dictionary generator

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

Any words added replace the `spellchecked_word` value in the dictionary, and flip the `is_spellchecked` bit. Re-running the program will resume at the last-checked word. On control-C (or at completion), the dictionary is saved.

## `pickler.py`

This takes an input text, as a list of strings, remaps all words according to the dictionary generated above, and removes all puncutation. The puncutation is then appended to the end, as Dexter did.

A test suite generates the process on a few samples:

**Source:**

```
It is a truth universally acknowledged, that a single man (??) loves punctuation!!
```

**Output:**

```
Itt is a trouth universally acknowledged that a single man leovs punctuation ,(??)!!
```

## `filings.py`

This downloads recent quarterly earnings reports (10-Q filings) from the [EDGAR database](https://www.sec.gov/edgar/searchedgar/companysearch.html) provided by the US Securities and Exchange Commission using [sec-edgar-downloader](https://github.com/jadchaar/sec-edgar-downloader), parses the reports, then passes the output through the pickler.

EDGAR reports are in a bespoke SGML format with wrapped HTML; this extracts the HTML blob, passes the text nodes to `pickler.py`, updates them in replace, then writes out the transformed HTML.

Using the HTML-to-text capability of [w3m](http://w3m.sourceforge.net/) then produces nicely-formatted plain text.
