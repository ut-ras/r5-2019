
use core::image;


fn checkAdjacent(image: &mut Image, x: u32, y: u32, tgt: u32, intermediate: u32) {
	let mut res = 0;

	for i in x-1..x+1 {
		for j in y-1..y+1 {
			let mask = image.data[y * image.width + x] & 0x000000FF;
			if(mask == tgt || mask == intermediate) {
				res += 1;
			}
		}
	}

	return res;
}


fn erode(&mut image, tgt: u32, default: u32) {

	let tmp = 0x000000FF;

	debug_assert(default & 0x000000FF == default);

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
	fn unify (p: &mut Pixel) { if p.mask == tmp { p.mask = default; }}

	image.iter_pixels(&unify)
}


fn dilate(image: &mut Image, tgt: u32, default: u32) {

	let tmp = 0x000000FF;

	for x in 1..image.width - 1 {
		for y in 1..image.height - 1 {
			if checkAdjacent(image, x, y, tgt, tgt) > 0 {
				let idx = y * image.width + x;
				image[idx] = (image[idx] & 0xFFFFFF00) | tmp;
			}
		}
	}

	fn unify (p: &mut Pixel) { if p.mask == tmp { p.mask = tgt; }}

	image.iter_pixels(&unify);
}
