# Q12 · How would you design a RAG pipeline for documents that change daily?

Two paths, and mixing them is the classic outage.

The **incremental path** runs in minutes and is triggered by content. Change capture emits
document *ids*, not documents. A content-hash diff decides what actually needs re-chunking —
metadata-only edits skip embedding entirely. Chunk-level upsert on stable ids derived from
doc id + ordinal + content hash, so unchanged chunks keep their id and need no new vector.
Orphaned chunks are tombstoned rather than deleted, and stay filterable until the next
compaction so in-flight queries stay consistent.

The **rebuild path** runs in hours and is triggered by a *model* change — an embedding model,
a chunker, an analyzer — never by content. Build v(n+1) alongside v(n), both queryable, one
routed to. Shadow-evaluate the new one on the frozen eval slice and on replayed production
queries. Then an atomic alias swap, keeping the old index warm so rollback is a pointer change
rather than a rebuild.

The thing to say out loud: **never write new-model embeddings into an index that still holds
old-model vectors.** Nothing will error. Cosine similarity will return well-formed numbers for
vectors that mean nothing to each other. A model-version tag on every row plus a check in the
release gate is the entire defence.
