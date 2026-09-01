# Q8 · Why does L2 normalisation change the relationship between cosine similarity and dot product?


Cosine is `q·d / (‖q‖‖d‖)`. After L2 normalisation both norms are 1, so the denominator
vanishes and cosine *is* the dot product. The rankings become identical.

The engineering consequence is the part that matters: an index configured for inner product
returns the same ranking as one configured for cosine **only if you normalise on write**. Mix
those up and every ranking silently changes — longer vectors win on inner product regardless of
direction. So: normalise on write, or configure the index for cosine, and know which one you
did. It is also why a similarity threshold is not portable: cosine is a relative score, not a
calibrated probability, and 0.82 on one corpus is not 0.82 on another.
