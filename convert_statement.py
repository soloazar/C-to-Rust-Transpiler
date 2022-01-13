import global_values
from write_to_rust_file import write_to_rust_file

node_list = []
node_right = []

def convert_statement(args):
    node_list.clear()
    node_right.clear()

    a =""
    left = ""

    if args["lvalue"]["_nodetype"]=="ID":
        left=args["lvalue"]["name"]
    elif args["lvalue"]["_nodetype"] == "ArrayRef":
        subscript= args["lvalue"]["subscript"]
        if type(subscript) is dict:
            for key, value in subscript.items():
                if key == "name":
                    left = args["lvalue"]["name"]["name"] + "[" + args["lvalue"]["subscript"]["name"] + "]"
                elif key =="value":
                    left = args["lvalue"]["name"]["name"] + "[" + args["lvalue"]["subscript"]["value"] + "]"


    a=a+left+args["op"]
    # print(a)
    b = a

    for key, value in args.items():
        if key == "rvalue":
            if type(value) is dict:
                node_l = loop_init(value)
                #           print(node_l)
                for i in node_l:
                    b = b + i
                b=b+";"
            else:
                b = "&"+ args["name"]+ ";"

    print(b)
    write_to_rust_file(b,'a')

    return (b)
    node_list.clear()
    node_right.clear()

def loop_init(args):
    if args["_nodetype"] == "ArrayRef":
        subscript= args["subscript"]
        if type(subscript) is dict:
            for key, value in subscript.items():
                if key == "name":
                    for i, j in global_values.declaration_tracker.items():

                        if i == args["name"]["name"]:
                            if j == "i32":
                                global_values.i32_borrow = True
                                val = "borrow_i32" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)
                            elif j == "i64":
                                global_values.i64_borrow = True
                                val = "borrow_i64" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)
                            elif j == "i128":
                                global_values.i128_borrow = True
                                val = "borrow_i128" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)
                            elif j == "float":
                                global_values.float_borrow = True
                                val = "borrow_float" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)
                            elif j == "char":
                                global_values.char_borrow = True
                                val = "borrow_char" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)
                            elif j == "double":
                                global_values.double_borrow = True
                                val = "borrow_double" + "(" + args["name"]["name"] + "[" + args["subscript"]["name"] + "]" + ")"
                                node_list.append(val)

                    #val = args["name"]["name"] + "[" + args["subscript"]["name"] + "]"
                    #node_list.append(val)
                elif key =="value":
                    for i, j in global_values.declaration_tracker.items():

                        if i == args["name"]["name"]:
                            if j == "i32":
                                global_values.i32_borrow = True
                                val = "borrow_i32" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                            elif j == "i64":
                                global_values.i64_borrow = True
                                val = "borrow_i64" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                            elif j == "i128":
                                global_values.i128_borrow = True
                                val = "borrow_i128" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                            elif j == "float":
                                global_values.float_borrow = True
                                val = "borrow_float" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                            elif j == "char":
                                global_values.char_borrow = True
                                val = "borrow_char" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                            elif j == "double":
                                global_values.double_borrow = True
                                val = "borrow_double" + "(" + args["name"]["name"] + "[" + args["subscript"]["value"] + "]" + ")"
                                node_list.append(val)
                    #val = args["name"]["name"] + "[" + args["subscript"]["value"] + "]"
                    #node_list.append(val)

    if args["_nodetype"]=="ID":
        for i, j in global_values.declaration_tracker.items():

            if i == args["name"]:
                if j == "i32":
                    global_values.i32_borrow = True
                    val = "borrow_i32" + "(" + args["name"] + ")"
                    node_list.append(val)
                elif j == "i64":
                    global_values.i64_borrow = True
                    val = "borrow_i64" + "(" + args["name"] + ")"
                    node_list.append(val)
                elif j == "i128":
                    global_values.i128_borrow = True
                    val = "borrow_i128" + "(" + args["name"] + ")"
                    node_list.append(val)
                elif j == "float":
                    global_values.float_borrow = True
                    val = "borrow_float" + "(" + args["name"] + ")"
                    node_list.append(val)
                elif j == "char":
                    global_values.char_borrow = True
                    val = "borrow_char" + "(" + args["name"] + ")"
                    node_list.append(val)
                elif j == "double":
                    global_values.double_borrow = True
                    val = "borrow_double" + "(" + args["name"] + ")"
                    node_list.append(val)

    elif args["_nodetype"]=="Constant":
        val = args["value"]
        node_list.append(val)
    elif args["_nodetype"]=="BinaryOp":
        for key, value in args.items():
            if key=="Constant":
                val= args["value"]
                node_list.append(val)
            elif key == "left":
                loop_init(value)

            else:
                if key == "op":
                    op = value
                    node_list.append(op)
                elif key == "right":

                    if value["_nodetype"] == "ID":
                        for i, j in global_values.declaration_tracker.items():
                            if i == value["name"]:
                                if j == "i32":
                                    global_values.i32_borrow = True
                                    val = "borrow_i32" + "(" + value["name"] + ")"
                                    node_list.append(val)
                                elif j == "i64":
                                    global_values.i64_borrow = True
                                    val = "borrow_i64" + "(" + value["name"] + ")"
                                    node_list.append(val)
                                elif j == "i128":
                                    global_values.i128_borrow = True
                                    val = "borrow_i128" + "(" + value["name"] + ")"
                                    node_list.append(val)
                                elif j == "float":
                                    global_values.float_borrow = True
                                    val = "borrow_float" + "(" + value["name"] + ")"
                                    node_list.append(val)
                                elif j == "char":
                                    global_values.char_borrow = True
                                    val = "borrow_char" + "(" + value["name"] + ")"
                                    node_list.append(val)
                                elif j == "double":
                                    global_values.double_borrow = True
                                    val = "borrow_double" + "(" + value["name"] + ")"
                                    node_list.append(val)
                    elif value["_nodetype"] == "ArrayRef":
                        subscript = value["subscript"]
                        if type(subscript) is dict:
                            for key, vals in subscript.items():
                                if key == "name":
                                    for i, j in global_values.declaration_tracker.items():

                                        if i == args["name"]["name"]:
                                            if j == "i32":
                                                global_values.i32_borrow = True
                                                val = "borrow_i32" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "i64":
                                                global_values.i64_borrow = True
                                                val = "borrow_i64" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "i128":
                                                global_values.i128_borrow = True
                                                val = "borrow_i128" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "float":
                                                global_values.float_borrow = True
                                                val = "borrow_float" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "char":
                                                global_values.char_borrow = True
                                                val = "borrow_char" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "double":
                                                global_values.double_borrow = True
                                                val = "borrow_double" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["name"] + "]" + ")"
                                                node_list.append(val)

                                    # val = args["name"]["name"] + "[" + args["subscript"]["name"] + "]"
                                    # node_list.append(val)
                                elif key == "value":
                                    for i, j in global_values.declaration_tracker.items():

                                        if i == value["name"]["name"]:
                                            if j == "i32":
                                                global_values.i32_borrow = True
                                                val = "borrow_i32" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "i64":
                                                global_values.i64_borrow = True
                                                val = "borrow_i64" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "i128":
                                                global_values.i128_borrow = True
                                                val = "borrow_i128" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "float":
                                                global_values.float_borrow = True
                                                val = "borrow_float" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "char":
                                                global_values.char_borrow = True
                                                val = "borrow_char" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                            elif j == "double":
                                                global_values.double_borrow = True
                                                val = "borrow_double" + "(" + value["name"]["name"] + "[" + \
                                                      value["subscript"]["value"] + "]" + ")"
                                                node_list.append(val)
                                    # val = args["name"]["name"] + "[" + args["subscript"]["value"] + "]"
                                    # node_list.append(val)

                    else:

                        val = value["value"]
                        node_list.append(val)
                elif key == "name":
                    for i,j in global_values.declaration_tracker.items():
                        if i == value:
                            if j == "i32":
                                global_values.i32_borrow = True
                                val = "borrow_i32" + "(" + value["name"] + ")"
                                node_list.append(val)
                            elif j == "i64":
                                global_values.i64_borrow = True
                                val = "borrow_i64" + "(" + value["name"] + ")"
                                node_list.append(val)
                            elif j == "i128":
                                global_values.i128_borrow = True
                                val = "borrow_i128" + "(" + value["name"] + ")"
                                node_list.append(val)
                            elif j=="float":
                                global_values.float_borrow=True
                                val = "borrow_float" + "(" + value + ")"
                                node_list.append(val)
                            elif j=="char":
                                global_values.char_borrow=True
                                val = "borrow_char" + "(" + value + ")"
                                node_list.append(val)
                elif key == "value":


                    val = value
                    node_list.append(val)

    #print(node_list)
    return (node_list)




