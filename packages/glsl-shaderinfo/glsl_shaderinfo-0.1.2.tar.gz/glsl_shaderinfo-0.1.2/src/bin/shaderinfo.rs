use std::collections::HashMap;
use std::fmt::Debug;
use std::fs;

use argparse::{ArgumentParser, Store};

use glsl_shaderinfo::glsl_shaderinfo::utils::{get_names, pluralise};
use glsl_shaderinfo::glsl_shaderinfo::{get_info, BlockInfo, Declaration};

fn print_declarations<T: Declaration + Debug>(declarations: &Vec<T>, label: &str) {
    let count = declarations.len();
    let pluralised = pluralise(&label, count);
    println!("{} {} declared", count, pluralised);
    if count > 0 {
        println!("--> {:?}", get_names(declarations));
        println!("--> {:?}", declarations);
    }
}

fn print_blocks(declarations: &HashMap<String, BlockInfo>, label: &str) {
    let count = declarations.len();
    let pluralised = pluralise(&label, count);
    println!("{} {} declared", count, pluralised);
    if count > 0 {
        println!("--> {:?}", declarations.keys());
        println!("--> {:?}", declarations);
    }
}

fn main() {
    /*
    TODO:
    -----
    This doesn't actually work any more, ever since I added the PyO3
    annotations to lib.rs... I get an error when running it:

    dyld: Symbol not found: _PyBaseObject_Type

    It seems something does not get linked properly by PyO3
    */
    let mut filename = String::new();
    {
        let mut parser = ArgumentParser::new();
        parser.set_description("Prints info about vars used in a GLSL shader.");
        parser
            .refer(&mut filename)
            .add_argument("filename", Store, "GLSL shader file to parse info from.")
            .required();
        parser.parse_args_or_exit();
    }

    let _err = format!("Unable to read the file: {}", filename);
    let contents = fs::read_to_string(filename).expect(_err.as_str());
    let info = get_info(&contents);

    println!("GLSL version: {}", info.version_str);

    print_declarations(&info.vars, "variable");
    print_blocks(&info.blocks, "block");
    print_declarations(&info.inputs, "input");
    print_declarations(&info.outputs, "output");
    print_declarations(&info.uniforms, "uniform");
}
