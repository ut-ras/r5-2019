//!
//! # Python Image interaction module
//!


extern crate cpython;

use cpython::{Python, PyObject, PyList, PyResult};
use core::Image;


fn to_py_array(py: Python, img: &Image) {

	let mut column = Vec::new();

	for y in 0 .. img.height {

		let mut row = Vec::new();

		for x in 0..img.width {

			let pixel = img.acess(x, y);
			let py_pixel = PyList::new(py, &[
				PyInt::new(py, pixel.h as c_long),
				PyInt::new(py, pixel.s as c_long),
				PyInt::new(py, pixel.v as c_long)
			]);

			row.push(py_pixel);
		}

		column.push(row);
	}

	return column.

}


fn extract(py: Python) -> PyResult<PyList> {
	Ok(())
}
