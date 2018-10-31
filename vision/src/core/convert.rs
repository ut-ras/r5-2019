//!
//! # Core Image conversion routines
//!


use std::cmp;
use core::types::*;


/// # Convert RGB pixel to HSV pixel
///
/// ## Parameters
/// 
/// - p : input pixel to modify and convert to HSV
pub fn rgb_to_hsv(p: &mut Pixel) {
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
pub fn hsv_to_rgb(p: &mut Pixel) {
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
