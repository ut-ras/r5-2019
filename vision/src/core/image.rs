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
/// - width: width of the image, in pixels
/// - heightght: height of the image, in pixels
/// - data: flattened image vector. Each row in the image is appended
///     horizontally.
pub struct Image {
    width: u32,
    height: u32,
    data: Vec<u32>
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


/// # Convert RGB pixel to HSV pixel
///
/// ## Parameters
/// 
/// - p : input pixel to modify and convert to HSV
fn rgb_to_hsv(p: &mut Pixel) {
    let v = cmp::max(cmp::max(p.h, p.s), p.v);
    let delta = v - cmp::min(cmp::min(p.h, p.s), p.v);

    let h =
        if      v == p.h { ((255 * (p.s - p.v) / delta) % 1530) / 6 }
        else if v == p.s { ((255 * (p.v - p.h) / delta) + 510 ) / 6 }
        else if v == p.v { ((255 * (p.h - p.s) / delta) + 1020) / 6 }
        else             { 0 };
    let s = delta / v;

    p.h = h;
    p.s = s;
    p.v = v;
}


/// # Convert HSV pixel to RGB pixel
///
/// ## Parameters
/// - p : input pixel to modify and convert to RGB
fn hsv_to_rgb(p: &mut Pixel) {
    let c = p.s * p.v / 255;
    let x = c * (255 - (((6 * p.h) % 510) - 255).abs()) / 255;
    let m = p.v - c;

    let (r, g, b) = match p.h {
        0   ... 42  => (c, x, 0),
        43  ... 85  => (x, c, 0),
        86  ... 127 => (0, c, x),
        128 ... 170 => (0, x, c),
        171 ... 212 => (x, 0, c),
        213 ... 255 => (c, 0, x),
        _           => (0, 0, 0),
    };
    
    p.h = r + m;
    p.s = g + m;
    p.v = b + m;
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
    fn unpack(&self, idx: usize) -> Pixel {
        let packed = self.data[idx];
        Pixel {
            h:      ((packed >> H_OFFSET) & BYTE_MASK) as i32,
            s:      ((packed >> S_OFFSET) & BYTE_MASK) as i32,
            v:      ((packed >> V_OFFSET) & BYTE_MASK) as i32,
            mask:   ((packed >> M_OFFSET) & BYTE_MASK) as i32,
        }
    }

    /// # Pack a pixel struct and store
    ///
    /// ## Parameters
    ///
    /// - input : pixel value to pack and store
    /// - idx : destination to store to
    fn pack(&mut self, input: &Pixel, idx: usize) {
        self.data[idx] = (
            input.h     << H_OFFSET |
            input.s     << S_OFFSET |
            input.v     << V_OFFSET |
            input.mask  << M_OFFSET) as u32;
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
    pub fn access(&self, x: u32, y: u32) -> Pixel {
        debug_assert!(x < self.width);
        debug_assert!(y < self.height);

        self.unpack((self.width * y + x) as usize)
    }

    /// # Iterate over pixels
    ///
    /// ## Parameters
    ///
    /// - f : function to call on all pixels; pixels are read and passed into
    ///     f. f is then allowed to modify the pixel. After, the pixel is
    ///     packed and stored.
    pub fn iter_pixels(&mut self, f: &Fn(&mut Pixel)) {
        for x in 0..self.width * self.height {
            let mut p = self.unpack(x as usize);
            f(&mut p);
            self.pack(&mut p, x as usize);
        }
    }

    /// # Iterate over pixels
    ///
    /// ## Parameters
    ///
    /// - f : function to call on all pixels. Works the same as iter_pixls,
    ///     except with additional x and y arguments.
    /// - border : number of pixels along the edges to exclude.
    pub fn enum_pixels(&mut self, f: &Fn(&mut Pixel, u32, u32), border: u32) {
        for x in border .. self.width - border {
            for y in border .. self.height - border {
                let mut p = self.unpack((y * self.width + x) as usize);
                f(&mut p, x, y);
                self.pack(&mut p, x as usize);
            }
        }
    }

    /// # Convert color spaces.
    ///
    /// ## Parameters
    ///
    /// - format : target color space; ColorSpace::RGB or ColorSpace::HSV
    pub fn cvt_color(&mut self, format: ColorSpace) {
        match format {
            ColorSpace::HSV => { self.iter_pixels(&rgb_to_hsv); },
            ColorSpace::RGB => { self.iter_pixels(&hsv_to_rgb); },
        }
    }
}
