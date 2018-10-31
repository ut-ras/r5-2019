//!
//! # Core Image access routines
//!


use core::convert::*;
use core::types::*;


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
            h:      (packed >> H_OFFSET) & BYTE_MASK,
            s:      (packed >> S_OFFSET) & BYTE_MASK,
            v:      (packed >> V_OFFSET) & BYTE_MASK,
            mask:   (packed >> M_OFFSET) & BYTE_MASK,
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

    /// # Iterate over pixels, with coordinates
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

    /// # Iterate over pixels, with borrowing
    ///
    /// ## Parameters
    ///
    /// - f : function to call on all pixels. Same as enum_pixels, except
    ///   with additional image borrowing argument.
    /// - border : number of pixels along the edges to exclude.
    pub fn enum_borrow(
            &mut self,
            f: &Fn(&mut Pixel, u32, u32, &mut Image),
            border: u32) {
        for x in border .. self.width - border {
            for y in border .. self.height - border {
                let mut p = self.unpack((y * self.width + x) as usize);
                f(&mut p, x, y, self);
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
