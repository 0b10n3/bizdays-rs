//! Business-day calendars for financial applications, focused on the
//! Brazilian market (ANBIMA and B3 holiday calendars).
//!
//! **Status:** pre-alpha, phase 0 — API not implemented yet.
//!
//! # Counting semantics
//!
//! `bizdays(from, to)` counts business days in the half-open interval
//! `[from, to)`: `from` is included, `to` is excluded. When `from > to` the
//! result is negative. This matches the Brazilian BUS/252 convention, NumPy's
//! `busday_count` and Polars' `business_day_count`.

#![forbid(unsafe_code)]

mod adjust;
mod calendar;
mod compose;
mod date;
mod daycount;
mod error;
mod getdate;
mod kernels;
mod registry;
mod weekmask;

/// Version of this crate, as declared in `Cargo.toml`.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
