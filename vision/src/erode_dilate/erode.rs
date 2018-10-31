
use core::image;


pub const TMP_MASK: u32 = 0x000000FF;


fn checkAdjacent(
		image: &mut image::Image,
		x: u32, y: u32, tgt: u32, intermediate: u32) {

	let mut res = 0;

	for i in x-1..x+1 {
		for j in y-1..y+1 {
			let mask = (image.data[y * image.width + x] >> image::M_OFFSET) & image::BYTE_MASK;
			if mask == tgt || mask == intermediate {
				res += 1;
			}
		}
	}

	return res;
}


fn erode(&mut image: image::Image, tgt: u32, default: u32) {

	let tmp = TMP_MASK;

	debug_assert!(default & image::BYTE_MASK == default);

	// Run erosion
	for x in 1..image.width - 1 {
		for y in 1..image.height - 1 {
			if checkAdjacent(image, x, y, tgt, tmp) != 9 {
				let idx = y * image.width + x;
				image[idx] = (image[idx] & 0xFFFFFF00) | tmp;
			}
		}
	}

	// Closure to turn tmp mask into default
	let unify = |p: &mut image::Pixel| { if p.mask == tmp { p.mask = default; }};

	image.iter_pixels(&unify)
}


fn dilate(image: &mut image::Image, tgt: u32, default: u32) {

	let tmp = TMP_MASK;

	for x in 1..image.width - 1 {
		for y in 1..image.height - 1 {
			if checkAdjacent(image, x, y, tgt, tgt) > 0 {
				let idx = y * image.width + x;
				image[idx] = (image[idx] & 0xFFFFFF00) | tmp;
			}
		}
	}

	let unify = |p: &mut image::Pixel| { if p.mask == tmp { p.mask = tgt; }};

	image.iter_pixels(&unify);
}
