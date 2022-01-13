import convert_int as int_convertor
import convert_char as char_convertor
import convert_float as float_convertor
import convert_double as double_convertor
import convert_statement as statement_convertor
import convert_array as array_convertor
import global_values
from write_to_rust_file import write_to_rust_file

node_list = []


def convert_for(args):
    cond = ""
    init = ""
    next = ""
    while_statement="while"
    for key, value in args.items():
        if key == "cond":
            if type(value) is dict:
                node_list=loop_cond(value)
                for i in node_list:
                    cond=cond+i
                while_statement=while_statement+" "+cond+" "+"{"
        elif key == "init":
            if type(value) is dict:
                for i,j in value.items():
                    if i=="decls":

                        decls=j
                #decls=value["decls"]
                        for val in decls:
                            init=init+"let"+" "+"mut"+" "+val["name"]+":i32"+" "+"="+val["init"]["value"]+";"
                            global_values.for_loop_init.append(val["coord"])

                init_val=init

                write_to_rust_file(init_val,'a')
                write_to_rust_file(while_statement,'a')




        elif key=="next":
            next=loop_next(value)

        elif key =="stmt":
            for i,j in value.items():
                if i=="block_items":
                    result=get_all_values(i, j)
            #stmt_block_items=value["block_items"]
            #result=get_all_values(key, stmt_block_items)

    print(init_val)
    print(while_statement)
    print(result)
    write_to_rust_file(next,'a')

    print(next)
    write_to_rust_file("}",'a')

    print("}")

def loop_next(args):
    lvalue=args["expr"]["name"]
    if args["op"] == "++":
        rvalue="+=1"
    next=lvalue+rvalue+";"
    return (next)



def loop_cond(args):
    for key, value in args.items():
        if key == "left":
            if value["_nodetype"] == "ID":
                name = value["name"]
                node_list.append(name)

            elif value["_nodetype"] == "Constant":

                val = value["value"]
                node_list.append(val)
            else:
                loop_cond(value)

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
            elif key == "value":

                val = value
                node_list.append(val)

    return (node_list)


def get_dict_values(parent, args):
    global nodetype
    for key, value in args.items():
        if key == "stmt":
            pass
        else:
            if type(value) != dict and type(value) != list:
                pass

            elif type(value) is list:
                get_all_values(key, value)

            elif type(value) is dict:
                # print(key,"--")

                get_dict_values(key, value)


def get_all_values(key, args):
    result=""
    list_len=len(args)
    iteration_number=0
    for i in args:
        iteration_number+=1
        if type(i) != dict and type(i) != list:
            # print(key,":",i)

            a = 1


        elif type(i) is dict:
            if i["_nodetype"] == "For":
                convert_for(i)

            elif i["_nodetype"] == "Decl":
                if i["type"]["_nodetype"] == "TypeDecl":

                    for j in i["type"]["type"]["names"]:

                        if j == "int":
                            result=int_convertor.convert_int(i)

                        elif j == "char":
                            char_convertor.convert_char(i)
                        elif j == "float":
                            float_convertor.convert_float(i)
                        elif j == "double":
                            double_convertor.convert_double(i)
                elif i["type"]["_nodetype"] == "ArrayDecl":
                    array_convertor.convert_array(i)

            elif i["_nodetype"] == "Assignment":
                result=statement_convertor.convert_statement(i)
            else:
                get_dict_values(key, i)





        elif type(i) is list:
            get_all_values(key, i)
        #print(result)
        #if iteration_number==list_len:
          #  print("")
    return (result)










