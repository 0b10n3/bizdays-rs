//! Calendar composition: `union` and `intersection`.
//!
//! Composition is materialized: the result is a new `Calendar` with its own
//! index. A day is a business day in the union if and only if it is a business
//! day in both calendars (holidays are the union).
//!
//! Roadmap: Phase 2.
//! Rust Book: ch. 8 (collections), ch. 13.2 (iterators).

// TODO(phase 2):
// - [ ] `union(&a, &b) -> Result<Calendar, Error>` (e.g. ANBIMA ∪ NY for FX T+2)
// - [ ] `intersection(&a, &b)`
// - [ ] define behaviour for mismatched ranges (ADR first)
// - [ ] proptest: union business day <=> business day in both
