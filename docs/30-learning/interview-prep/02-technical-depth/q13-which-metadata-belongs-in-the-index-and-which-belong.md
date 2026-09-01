# Q13 · Which metadata belongs in the index, and which belongs in the prompt?

In the index: anything you filter or scope on — source, publication date, tenant, ACL,
document type, language. A field you did not index is a filter you cannot apply, and the
failure looks like poor recall rather than like a schema bug.

In the prompt: anything the model must reason about — the title, the source, and especially
the publication date, because a temporal question is unanswerable if dates live only in the
index.

Dates go in **both**, and that is the part most candidates miss.
