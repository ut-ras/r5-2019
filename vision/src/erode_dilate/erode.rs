//!
//! # Erosion and dilation
//!


use core;


/// Temporary reserved mask value; 0x000000FF for now.
pub const TMP_MASK: u32 = 0x000000FF;


/// # Count the number of adjacent pixels matching given mask values
///
/// ## Parameters
///
/// - x : target x coordinate
/// - y : target y coordinate
/// - tgt : target mask to count
/// - intermediate : secondary mask value to count
///
/// ## Returns
///
/// Number of values within B_1(x, y) that match, including (x, y) in the
/// infinity norm.
fn check_adjacent(
		image: &core::Image,
		x: usize, y: usize, tgt: u32, intermediate: u32) -> u32 {

	let mut res = 0;

	for row in image.data[y-1 .. y+1].iter() {
		for pixel in row[x-1 .. x+1].iter() {
			let mask = pixel & core::BYTE_MASK;
			if (mask == tgt) || (mask == intermediate) {
				res += 1;
			}
		}
	}

	return res;
}


/// # Erode an image mask by 1 pixel
///
/// ## Parameters
///
/// - image : image to erode
/// - tgt : target mask to erode
/// - default : mask value to replace eroded pixels with
pub fn erode(image: &mut core::Image, tgt: u32, default: u32) {

	debug_assert!(default & core::BYTE_MASK == default);

	// Closure to run erosion
	let check = |p: &mut core::Pixel, img: &core::Image| {
		if check_adjacent(img, p.x, p.y, tgt, TMP_MASK) != 9 {
			p.mask = TMP_MASK;
		}
	};
	image.iter_borrow(&check, 1);

	// Closure to turn tmp mask into default
	let unify = |p: &mut core::Pixel| {
		if p.mask == TMP_MASK { p.mask = default; }
	};
	image.iter_pixels(&unify);
}


/// # Dilate an image mask by 1 pixel
///
/// ## Parameters
/// - image : image to dilate
/// - tgt : target mask to dilate
pub fn dilate(image: &mut core::Image, tgt: u32) {

	// Closure to run dilation
	let check = |p: &mut core::Pixel, img: &core::Image| {
		if check_adjacent(img, p.x, p.y, tgt, tgt) > 0 && p.mask != tgt {
			p.mask = TMP_MASK;
		}
	};
	image.iter_borrow(&check, 1);

    // Closure to turn tmp mask to default
	let unify = |p: &mut core::Pixel| {
		if p.mask == TMP_MASK { p.mask = tgt; }
	};
	image.iter_pixels(&unify);
}
