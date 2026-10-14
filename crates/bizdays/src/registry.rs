//! Built-in calendars (ANBIMA, B3, later NY).
//!
//! The `.cal` files in `data/` are embedded with `include_str!` and parsed
//! lazily, once, through `OnceLock`.
//!
//! Roadmap: Phase 2.
//! Rust Book: ch. 19 (macros: `include_str!`); std docs for `OnceLock`.

// TODO(phase 2):
// - [ ] `.cal` parser: weekday names header, then ISO dates
// - [ ] `Calendar::anbima()`, `Calendar::b3()` returning `&'static Calendar`
// - [ ] tolerate duplicated dates (ANBIMA lists 2079-04-21 twice upstream)
// - [ ] lookup by name (case-insensitive)
// - [ ] expose `DATA_VERSION`
