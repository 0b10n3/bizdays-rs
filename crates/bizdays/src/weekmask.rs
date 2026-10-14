//! `Weekmask(u8)`: bitmask of the weekdays that are *not* business days.
//!
//! Bit 0 = Monday ... bit 6 = Sunday. The default for Brazil is
//! Saturday + Sunday.
//!
//! Roadmap: Phase 1.
//! Rust Book: ch. 5 (newtypes), ch. 3.2 (integer types, bit operations).

// TODO(phase 1):
// - [ ] `pub struct Weekmask(u8)` with a weekend-only constructor
// - [ ] `is_nonbiz(weekday) -> bool`
// - [ ] parse from day names as found in `.cal` headers ("Saturday", "Sunday")
// - [ ] reject masks where every day is non-business
