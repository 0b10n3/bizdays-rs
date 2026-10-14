//! `enum Error`: every fallible operation returns `Result<_, bizdays::Error>`.
//!
//! Built with `thiserror` (added in Phase 1).
//!
//! Roadmap: Phase 1.
//! Rust Book: ch. 9 (error handling), ch. 9.2 (`Result` and `?`).

// TODO(phase 1):
// - [ ] add `thiserror` (ask the maintainer first, see AGENTS.md section 6)
// - [ ] variants: invalid date, date out of calendar range, invalid weekmask,
//       unsorted/duplicate holidays, parse errors
// - [ ] English messages that include the offending value
