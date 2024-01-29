use std::collections::HashMap;
use std::ffi::{c_char, c_void};
use std::ptr::null_mut;
use std::sync::RwLock;
use anyhow::{Error, Result};
use nix::libc;

/// The code in this file is just a skeleton. You are allowed (and encouraged!)
/// to change if it doesn't fit your needs or ideas.
#[no_mangle]
pub extern "C" fn __runtime_init() {
    todo!()
}

#[no_mangle]
pub extern "C" fn __runtime_cleanup() {
    todo!()
}

#[no_mangle]
pub extern "C" fn __runtime_check_addr(/* your arguments */) {
    todo!()
}

#[no_mangle]
pub extern "C" fn __runtime_malloc(size: usize) -> *mut c_void {
    todo!()
}

#[no_mangle]
pub extern "C" fn __runtime_free(ptr: *mut c_void) {
    todo!()
}
