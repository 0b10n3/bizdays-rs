//! `enum DayCount`: day-count conventions.
//!
//! BUS/252, ACT/360, ACT/365F and 30/360. Formulas in `docs/convencoes.md`.
//!
//! Roadmap: Phase 2.
//! Rust Book: ch. 6 (enums), ch. 10.2 (traits).

// TODO(phase 2):
// - [ ] `pub enum DayCount { Bus252, Act360, Act365F, Thirty360 }`
// - [ ] `year_fraction(from, to, &Calendar)` (only BUS/252 needs the calendar)
// - [ ] pick the 30/360 variant explicitly and document it
