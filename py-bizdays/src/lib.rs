//! Python bindings for `bizdays`, exposed as `bizdays_rs._bizdays_rs`.

use pyo3::prelude::*;

/// Native extension module for the `bizdays_rs` Python package.
#[pymodule]
fn _bizdays_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", bizdays::VERSION)?;
    Ok(())
}
