//!
//! # Core Image access routines
//!


use core::convert::*;
use core::types::*;


impl Image {

    /// # Get image pixel
    ///
    /// ## Parameters
    ///
    /// - x, y: coordinates of the pixel to fetch
    ///
    /// ## Returns
    ///
    /// Unpacked pixel struct
    fn get(&self, x: usize, y: usize) -> Pixel {
        debug_assert!(x < self.width);
        debug_assert!(y < self.height);

        let packed = self.data[x][y];
        Pixel {
            h:      (packed >> H_OFFSET) & BYTE_MASK,
            s:      (packed >> S_OFFSET) & BYTE_MASK,
            v:      (packed >> V_OFFSET) & BYTE_MASK,
            mask:   (packed >> M_OFFSET) & BYTE_MASK,
            x:      x,
            y:      y,
        }
    }

    /// # Pack a pixel struct and store
    ///
    /// ## Parameters
    ///
    /// - input : pixel value to pack and store
    fn set(&mut self, input: &Pixel) {
        debug_assert!(input.x < self.width);
        debug_assert!(input.y < self.height);

        self.data[input.x][input.y] = (
            input.h     << H_OFFSET |
            input.s     << S_OFFSET |
            input.v     << V_OFFSET |
            input.mask  << M_OFFSET) as u32;
    }

    /// # Iterate over pixels
    ///
    /// ## Parameters
    ///
    /// - f : function to call on all pixels; pixels are read and passed into
    ///     f. f is then allowed to modify the pixel. After, the pixel is
    ///     packed and stored.
    pub fn iter_pixels(&mut self, f: &Fn(&mut Pixel)) {
        for x in 0..self.width {
            for y in 0..self.height {
                let mut p = self.get(x, y);
                f(&mut p);
                self.set(&mut p);
            }
        }
    }

    /// # Iterate over pixels, with borrowing
    ///
    /// ## Parameters
    ///
    /// - f : function to call; same as iter_pixels
    pub fn iter_borrow(&mut self, f: &Fn(&mut Pixel, &Image), border: usize) {
        for x in border .. self.width - border {
            for y in border .. self.height - border {
                let mut p = self.get(x, y);
                f(&mut p, &self);
                self.set(&mut p);
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
