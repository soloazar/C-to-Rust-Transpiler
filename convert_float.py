import global_values
from extract_ast import export_ast
from write_to_rust_file import write_to_rust_file

node_list = []
node_right = []


def convert_float(args):
    node_list.clear()
    name = args["name"]
    convert_float.mutability = False
    mutability_checker(name, args)
    if convert_float.mutability:
        mut = " mut "
    else:
        mut = " "
    a = "let" +mut+ args["name"] + ":" + "f32" + " " + "=" + " "
    # print(a)
    b=a
    global_values.declaration_tracker[args["name"]] = "float"
    for key, value in args.items():
        if key == "init":

            if type(value) is dict:
                node_l = loop_init(value)
                #           print(node_l)

                for i in node_l:
                    b = b + i
                b=b+";"

            else:
                b="let"+mut+args["name"]+":"+"f32"+";"

    print(b)
    write_to_rust_file(b,'a')

    return (b)

    node_list.clear()


def loop_init(args):
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
            if key == "left":
                loop_init(value)

            else:
                if key == "op":
                    op = value
                    node_list.append(op)
                elif key == "right":

                    if value["_nodetype"] == "ID":
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


                    else:

                        val = value["value"]
                        node_list.append(val)
                elif key == "value":

                    val = value
                    node_list.append(val)

    return (node_list)




def mutability_checker(name,args):
    ast_dict, ast_json = export_ast()
    def get_dict_values(parent,args):
        for key,value in args.items():
            if key=="stmt":
                pass
            else:
                if type(value) != dict and type(value) != list:
                    pass
                elif type(value) is list:
                    get_all_values(key, value)
                elif type(value) is dict:

                    get_dict_values(key, value)

    def get_all_values(key, args):
        global nodetype
        for i in args:

            if type(i) is dict:
                if i["_nodetype"] == "FuncDef":
                    value = i["body"]["block_items"]
                    get_all_values("block_items", value)

                elif i["_nodetype"] == "For":
                    value = i["stmt"]["block_items"]
                    get_all_values("block_items", value)
                elif i["_nodetype"] == "If":
                    # convert_if(i)
                    get_all_values("key", i)

                if i["_nodetype"] == "Assignment":

                    if i["lvalue"]["name"] == name:
                        convert_float.mutability = True
                else:
                    get_dict_values(key, i)

            elif type(i) is list:

                get_all_values(key, i)

    get_all_values("ext",ast_dict["ext"])



