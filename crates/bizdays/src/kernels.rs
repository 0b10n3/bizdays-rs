//! Vectorized operations over `&[i32]` with nulls.
//!
//! Kernels take slices (and validity masks) and write into preallocated output
//! buffers. They back the NumPy, Polars, Arrow and Spark adapters.
//!
//! Roadmap: Phase 3.
//! Rust Book: ch. 4.3 (slices), ch. 13.2 (iterators).

// TODO(phase 3):
// - [ ] `bizdays_kernel(from: &[i32], to: &[i32], out: &mut [i32])` with
//       scalar/same-length broadcasting
// - [ ] null propagation via validity bitmaps
// - [ ] no allocation in the hot loop
// - [ ] proptest: kernel == map of the scalar function
