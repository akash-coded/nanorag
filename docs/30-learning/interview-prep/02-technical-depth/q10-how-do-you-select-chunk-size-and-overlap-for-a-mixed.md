# Q10 · How do you select chunk size and overlap for a mixed-format corpus?


I would not answer with a number. The size is a consequence of two things: the shape of the
document and the shape of the question.

If the documents carry reliable structure — headings, sections, cells, functions — split on
their own boundaries and carry the heading path into every chunk. That is free, and it makes
chunks attributable. If answers span several paragraphs of continuous argument, embed small and
return the parent. If queries are short, factoid and identifier-heavy, smaller chunks plus a
lexical index, because precision matters more than surrounding narrative.

Then measure. Run the strategies against one eval set and put three columns next to recall:
storage multiplier, index cost, and the number of gold spans that no chunk of that strategy
contains — because a chunking choice can make a label unscoreable, which looks like a recall
problem and is not.

And one thing I would raise unprompted: **re-chunking silently re-tunes BM25.** The
length-normalisation term is relative to the average document length of the corpus you just
rebuilt, so lexical scores change even though no code did. Re-measure after every chunking
change.
