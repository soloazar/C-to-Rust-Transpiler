def write_to_rust_file(data,mode):
    with open('playground/src/main.rs', mode) as f:
        f.write(data)
        f.write('\n')
