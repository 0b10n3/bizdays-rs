//! `Calendar`, `CalendarBuilder` and the precomputed index.
//!
//! The index uses dense arrays covering the calendar range:
//! - `cum: Vec<u32>`: `cum[i]` = number of business days in `[start, start + i)`;
//! - `bizlist: Vec<i32>`: the business days themselves, in order.
//!
//! With these, `bizdays(a, b) = cum[b] - cum[a]`, `is_bizday`, `offset` and the
//! rolls are all O(1). `Calendar` is immutable, wraps an `Arc` and is
//! `Send + Sync`.
//!
//! Roadmap: Phase 1.
//! Rust Book: ch. 8.1 (`Vec`), ch. 16.3 / 16.4 (`Arc`, `Send`, `Sync`),
//! ch. 17 (builder pattern discussion).

// TODO(phase 1):
// - [ ] `CalendarBuilder { holidays, weekmask, start, end }` with validation
// - [ ] build `cum` and `bizlist` in one pass
// - [ ] `is_bizday`, `bizdays(from, to)` with `[from, to)` semantics
// - [ ] `offset(d, n)` (semantics pending: ADR-0005)
// - [ ] out-of-range dates -> `Error`, never panic
// - [ ] golden tests against `tests/fixtures/{bizdays,isbizday}.csv`
// - [ ] proptest: additivity and antisymmetry (AGENTS.md section 3)
