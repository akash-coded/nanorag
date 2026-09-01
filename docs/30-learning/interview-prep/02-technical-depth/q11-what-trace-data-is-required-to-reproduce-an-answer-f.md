# Q11 · What trace data is required to reproduce an answer failure?

Retrieved chunk ids and their scores at each stage, the packed context with full provenance
(doc id, chunk ordinal, title, publication date, score), the assembled prompt, the model
response, per-stage latency, the index version and the encoder tag.

The test of whether you have enough: can you **diff two runs of the same query** and see which
chunks moved? The row that matters most in that diff is "retrieved then dropped, of which
gold" — it separates *we could not find it* from *we found it and threw it away*, and those
have completely different fixes. Almost nobody instruments the second one.

Without a trace you cannot reproduce a failure, cannot diff a change, and cannot turn a
production failure into a regression case — which means your eval set can never learn anything
your users found.
