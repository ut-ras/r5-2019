//!
//! # Core Image Module
//!
//! Contains image definitions and access routines.
//!
//! ## Summary
//!
//! - Create and store images with ```core::Image```. This type has
//!   attributes ```width```, ```height```, and ```data```; ```data``` is
//!   a vector containing packed, unrolled H-S-V-Mask data.
//! - Access pixels with ```core::Image.acess```. This returns a
//!   ```core::Pixel``` struct with ```h```, ```s```, ```v```, and ```mask```
//!   entries.


mod convert;
mod types;
mod image;

pub use self::types::*;
pub use self::image::*;
pub use self::convert::*;
