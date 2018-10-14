//!
//! # Core Image Structs and Access Routines
//!


/// # Color Space
///
/// ## Members
/// - RGB: RGB (red-green-blue) color space
/// - HSV: HSV (hue-saturation-value) color space
pub enum ColorSpace { RGB, HSV }


/// # Unpacked Pixel Struct
///
/// ## Members
/// - h: hue value
/// - s: saturation value
/// - v: 'value' (lightness)
/// - mask: mask membership indicator
pub struct Pixel { h: i32, s: i32, v: i32, mask: i32 }

/// # Image struct
///
/// ## Members
///
/// - colorspace: RGB or HSV color space
/// - width: width of the image, in pixels
/// - height: height of the image, in pixels
/// - data: flattened image vector. Each row in the image is appended
///     horizontally.
pub struct Image {
    colorspace: ColorSpace,
    width: i32,
    height: i32,
    data: Vec<i32>
}

impl Image {

    /// # Access and unpack an image pixel
    /// Since images are stored as flattened vectors, the target index
    /// is ```y * width + x```.
    ///
    /// ## Parameters
    ///
    /// - x : x coordinate
    /// - y : y coordinate
    ///
    /// ## Returns
    /// Unpacked pixel struct
    pub fn access(&self, x: i32, y: i32) -> Pixel {
        debug_assert!(x < self.width);
        debug_assert!(y < self.height);

        let packed = self.data.get(self.width * y + x);

        Pixel {
            h: packed & 0xF000 >> 24,
            s: packed & 0x0F00 >> 16,
            v: packed & 0x00F0 >> 8,
            mask: packed & 0x000F,
        }
    }

    /// # Convert color spaces.
    ///
    /// ## Parameters
    ///
    /// - format : target color space; ColorSpace::RGB or ColorSpace::HSV
    pub fn cvt_color(&self, format: ColorSpace) {

    }
}
