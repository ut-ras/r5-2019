//!
//! # Core Image Structs and Access Routines
//!

use std::cmp;


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

	/// # Unpack a packed 32-bit integer
	///
	/// ## Parameters
	///
	/// - idx : index of the value to fetch
	///
	/// ## Returns
	///
	/// Unpacked pixel struct
	fn unpack(&self, idx: i32) -> Pixel {
		let packed = self.data.get(idx);
        Pixel {
            h: packed & 0xF000 >> 24,
            s: packed & 0x0F00 >> 16,
            v: packed & 0x00F0 >> 8,
            mask: packed & 0x000F,
        }
	}

	/// # Pack a pixel struct and store
	///
	/// ## Parameters
	///
	/// - input : pixel value to pack and store
	/// - idx : destination to store to
	fn pack(&self, input: Pixel, idx: i32) {
		self.data[idx] = (
			input.h << 24 | input.s << 16 | input.v << 8 | input.mask);
	}

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
    ///
    /// Unpacked pixel struct
    pub fn access(&self, x: i32, y: i32) -> Pixel {
        debug_assert!(x < self.width);
        debug_assert!(y < self.height);

        unpack(&self, self.width * y + x);
    }

    /// # Convert color spaces.
    ///
    /// ## Parameters
    ///
    /// - format : target color space; ColorSpace::RGB or ColorSpace::HSV
    pub fn cvt_color(&self, format: ColorSpace) {

    	if format == ColorSpace::HSV && self.colorspace == ColorSpace::RGB {

    		for x in 0..self.width * self.height {
    			let pixel = access(&self, x);

    			let v = cmp::max(cmp::max(pixel.h, pixel.s), pixel.v);
    			let delta = v - cmp::min(cmp::min(pixel.h, pixel.s), pixel.v);
    			let h = 0;
    			let h = if v == self.h {
    				255 * (((pixel.s - pixel.v) / delta) % 6) / 6;
    			} else if v == self.s {
    				255 * (((pixel.v - pixel.h) / delta) + 2) / 6;
    			} else if v == self.v {
    				255 * (((pixel.h - pixel.s) / delta) + 4) / 6;
    			};
    			let s = delta / v;

    			let pixel:h = h;
    			let pixel:s = s;
    			let pixel:v = v;

    			pack(&self, pixel, x);
    		}
    	}
    }
}
