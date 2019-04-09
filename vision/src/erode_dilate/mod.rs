//!
//! # Erode and Dilation module
//!
//! Contains routines for mask erosion and dilation. Pretty simple.
//!
//! ## Summary
//!
//! - Erode masks by one pixel with ```erode_dilate::erode```.
//! - Dilate masks by one pixel with ```erode_dilate::dilate```.

mod erode;
pub use self::erode::*;
