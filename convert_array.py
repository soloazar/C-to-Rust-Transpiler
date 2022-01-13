import global_values
from extract_ast import export_ast
from write_to_rust_file import write_to_rust_file

node_list = []
node_right = []

def convert_array(args,*indent_level):
    name = args["type"]["type"]["declname"]
    convert_array.mutability = False
    mutability_checker(name,args)
    if convert_array.mutability:
        mut = " mut "
    else:
        mut = " "
    node_list.clear()
    node_right.clear()
    a =""
    left = ""
    dim_type=""
    dim_value = ""
    dim=""
    convert_array.int_level=0

    if type(args["type"]["dim"]) is dict:
        for i in args["type"]["type"]["type"]["names"]:
 #           if i == "int":
#                dim_type = "i32"

            if i == "char":
                dim_type = "char"
                dim_value = args["type"]["dim"]["value"]
                dim = dim_type + ";" + dim_value
            elif i == "float":
                dim_type = "f32"
                dim_value = args["type"]["dim"]["value"]
                dim = dim_type + ";" + dim_value
            elif i == "double":
                dim_type = "f64"
                dim_value = args["type"]["dim"]["value"]
                dim = dim_type + ";" + dim_value
            else:
                if i == "int":
                    convert_array.int_level = convert_array.int_level+1
                elif i=="long":
                    convert_array.int_level = convert_array.int_level+1
        if convert_array.int_level==0:

            dim_value = args["type"]["dim"]["value"]
            dim = dim_type + ";" + dim_value
        elif convert_array.int_level == 1:
            dim_type = "i32"
            dim_value = args["type"]["dim"]["value"]
            dim = dim_type + ";" + dim_value
        elif convert_array.int_level == 2:
            dim_type = "i64"
            dim_value = args["type"]["dim"]["value"]
            dim = dim_type + ";" + dim_value
        elif convert_array.int_level == 3:
            dim_type = "i128"
            dim_value = args["type"]["dim"]["value"]
            dim = dim_type + ";" + dim_value

    if args["type"]["type"]["_nodetype"]=="TypeDecl":
        left="let"+mut+args["type"]["type"]["declname"]+":"+"["+dim+"]"+"="+"["

    a=left
    b = a

    for key, value in args.items():
        if key == "init":



            if type(value) is dict:
                for i in value["exprs"]:
                    node_l = loop_init(i)

                for i in range((len(node_l)),int(dim_value)):
                    node_l.append("0")
                for i in range (0,len(node_l)):

                    if i==0:
                        b=b+node_l[i]
                    else:
                        b=b+","+node_l[i]
                b = b +"]"+ ";"

            else:
                b = "let"+mut+args["type"]["type"]["declname"]+":"+"["+dim+"]"+";"

    print(b)
    global_values.declaration_tracker[args["type"]["type"]["declname"]]=dim_type

    write_to_rust_file(b,'a')

    return (b)
    node_list.clear()
    node_right.clear()

def loop_init(args):
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
                    name = "&" + value["name"]
                    node_list.append(name)

                else:

                    val = value["value"]
                    node_list.append(val)
            elif key == "name":

                val = "&"+value
                node_list.append(val)
            elif key == "value":

                val = value
                node_list.append(val)

    #print(node_list)
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
            if type(i) != dict and type(i) != list:

                pass
            elif type(i) is dict:

                if i["_nodetype"] == "Assignment":
                    if i["lvalue"]["name"]==name:
                        convert_array.mutability=True
                    elif i["lvalue"]["name"]["name"]==name:
                        convert_array.mutability=True
                get_dict_values(key,i)

            elif type(i) is list:

                get_all_values(key,i)

    get_all_values("ext",ast_dict["ext"])
