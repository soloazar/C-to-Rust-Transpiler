import convert_int as int_convertor
import convert_char as char_convertor
import convert_float as float_convertor
import convert_double as double_convertor
import convert_statement as statement_convertor
import convert_array as array_convertor
import global_values
from convert_for import convert_for
from write_to_rust_file import write_to_rust_file


def convert_if(args):
    convert_if.cond_list=[]
    cond = ""


    for key,value in args.items():

        if key == "cond":
            if type(value) is dict:
                node_list=loop_cond(value)
                for i in node_list:
                    cond=cond+i
                if_cond="if"+" "+cond+" "+"{"
                write_to_rust_file(if_cond, 'a')
                if_true=args["iftrue"]
                for i, j in if_true.items():
                    if i == "block_items":
                        for k in j:
                            global_values.for_loop_init.append(k["coord"])
                        get_all_values(i, j)
                write_to_rust_file("}", 'a')


        elif key =="iffalse":
            for i,j in value.items():
                if i=="block_items":
                    for k in j:

                        global_values.for_loop_init.append(k["coord"])
                    write_to_rust_file("else {", 'a')
                    get_all_values(i,j)
                    write_to_rust_file("}", 'a')


    print(global_values.for_loop_init)








def loop_cond(args):
    for key, value in args.items():
        if key == "left":
            if value["_nodetype"] == "ID":
                name = value["name"]
                convert_if.cond_list.append(name)

            elif value["_nodetype"] == "Constant":

                val = value["value"]
                convert_if.cond_list.append(val)
            else:
                loop_cond(value)

        else:
            if key == "op":
                op = value
                convert_if.cond_list.append(op)
            elif key == "right":

                if value["_nodetype"] == "ID":
                    name = "&" + value["name"]
                    convert_if.cond_list.append(name)

                else:

                    val = value["value"]
                    convert_if.cond_list.append(val)
            elif key == "value":

                val = value
                convert_if.cond_list.append(val)

    return (convert_if.cond_list)





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

