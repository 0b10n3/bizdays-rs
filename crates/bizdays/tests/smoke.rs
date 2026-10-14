//! Smoke test: the crate links and exposes its version.

#[test]
fn version_is_not_empty() {
    assert!(!bizdays::VERSION.is_empty());
}
