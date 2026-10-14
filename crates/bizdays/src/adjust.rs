//! `enum Adjustment`: business-day rolling conventions.
//!
//! Variants: following, preceding, modified following, modified preceding.
//!
//! Roadmap: Phase 1.
//! Rust Book: ch. 6 (enums and `match`).

// TODO(phase 1):
// - [ ] `pub enum Adjustment { Following, Preceding, ModifiedFollowing, ModifiedPreceding }`
// - [ ] `Calendar::adjust(d, Adjustment)` using the `bizlist` index
// - [ ] golden tests against `tests/fixtures/roll.csv`
// - [ ] proptest: `following(d) >= d` and is a business day
