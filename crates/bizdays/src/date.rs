//! Calendar dates as a `Date(i32)` newtype: days since 1970-01-01.
//!
//! Same memory layout as Arrow `date32`, Polars `Date` and Spark `DateType`,
//! so vectors of dates can cross the FFI boundary without conversion.
//! Civil conversion (year/month/day <-> days) follows Howard Hinnant's
//! `days_from_civil` / `civil_from_days` algorithms.
//!
//! Roadmap: Phase 1.
//! Rust Book: ch. 5 (structs), ch. 10.2 (traits: `Display`, `Ord`, `From`).

// TODO(phase 1):
// - [ ] red test: `Date::from_ymd(2026, 10, 12)` round-trips through `to_ymd`
// - [ ] `pub struct Date(i32)` with derives (Copy, Eq, Ord, Hash, Debug)
// - [ ] `from_ymd` returning `Result<Date, Error>` (invalid dates are errors)
// - [ ] `to_ymd` using Hinnant's `civil_from_days`
// - [ ] `weekday()` (1970-01-01 was a Thursday)
// - [ ] `Display` / `FromStr` for ISO 8601 (`YYYY-MM-DD`)
// - [ ] proptest: `from_ymd(to_ymd(d)) == d` for the supported range
