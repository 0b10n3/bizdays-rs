//! `getdate`: a small DSL such as `"first bizday after 15th day"`.
//!
//! Parsed into an AST (enum) and evaluated against a calendar for a given
//! year and optional month.
//!
//! Roadmap: Phase 2.
//! Rust Book: ch. 6 (enums), ch. 15.1 (`Box` for recursive types).

// TODO(phase 2):
// - [ ] grammar: ordinal + (day | bizday | weekday) [+ (before | after) expr]
// - [ ] tokenizer and recursive-descent parser -> AST
// - [ ] evaluator
// - [ ] golden tests against `tests/fixtures/getdate.csv`
