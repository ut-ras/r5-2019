//!
//! # Core Image Structs and Definitions
//!


/// Image width; must be constant
pub const IMAGE_WIDTH: usize = 400;
/// Image height; must be constant
pub const IMAGE_HEIGHT: usize = 300;


/// # Color Space
///
/// ## Members
///
/// - RGB: RGB (red-green-blue) color space
/// - HSV: HSV (hue-saturation-value) color space
pub enum ColorSpace { RGB, HSV }


/// # Unpacked Pixel Struct
///
/// ## Members
///
/// - h: hue value
/// - s: saturation value
/// - v: 'value' (lightness)
/// - mask: mask membership indicator
/// - x: x coordinate
/// - y: y coordinate
pub struct Pixel {
    pub h: u32,
    pub s: u32,
    pub v: u32,
    pub mask: u32,
    pub x: usize,
    pub y: usize,
}


/// # Image struct
///
/// ## Members
///
/// - width: width of the image, in pixels
/// - heightght: height of the image, in pixels
/// - data: flattened image vector. Each row in the image is appended
///     horizontally.
pub struct Image {
    pub width: usize,
    pub height: usize,
    pub data: [[u32; IMAGE_HEIGHT]; IMAGE_WIDTH],
}


/// Hue offset
pub const H_OFFSET: u32 = 24;
/// Saturation offset
pub const S_OFFSET: u32 = 16;
/// Value offset
pub const V_OFFSET: u32 = 8;
/// Mask offset
pub const M_OFFSET: u32 = 0;
/// Single byte mask
pub const BYTE_MASK: u32 = 0x000000FF;
