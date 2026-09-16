# Data retention policy

Phase 1 only produces synthetic, in-memory values. Future providers default to memory TTL caching. Actual API responses, market CSV/SQLite files, and news bodies must never be committed. Provider-specific cache, persistence, attribution, and redistribution requirements belong in `THIRD_PARTY_DATA.md`.

