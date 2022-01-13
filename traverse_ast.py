import sys

#sys.path.extend(['.', '..'])
import global_values
from extract_ast import export_ast
import convert_int as int_convertor
import convert_char as char_convertor
import convert_float as float_convertor
import convert_double as double_convertor
import convert_statement as statement_convertor
import convert_array as array_convertor
import convert_for as for_convertor
import convert_if as if_convertor
import convert_struct as struct_convertor
import convert_function as function_convertor
from write_to_rust_file import write_to_rust_file

nodetype="node"
global indent_level
ast_dict,ast_json = export_ast()
write_to_rust_file("",'w')
with open('ast.txt', 'w') as f:
    print(ast_json, file=f)

print (ast_json)
def transpile():
    result=[]

    def get_dict_values(parent,args):
        global nodetype
        for key,value in args.items():
            if key=="stmt":
                pass
            else:
                if type(value) != dict and type(value) != list:
                    a = 2
                    # print(key,":",value)

                    if key == "_nodetype":
                        nodetype = key






                elif type(value) is list:
                    get_all_values(key, value)

                elif type(value) is dict:
                    # print(key,"--")

                    get_dict_values(key, value)


    def get_all_values(key, args):
        global nodetype
        for i in args:
            if type(i) != dict and type(i) != list:
                #print(key,":",i)

                a=1


            elif type(i) is dict:
                if i["_nodetype"] == "FuncDef":
                    function_convertor.convert_function(i)

                elif i["_nodetype"] == "For":
                    for_convertor.convert_for(i)
                elif i["_nodetype"] == "If":
                    if_convertor.convert_if(i)

                elif i["_nodetype"] == "Decl":
                    for val in global_values.for_loop_init:
                        if val ==i["coord"]:
                            pass
                    if i["coord"] in global_values.for_loop_init:
                        pass
                    #if i["type"]["_nodetype"]=="Struct":
                     #   struct_convertor.convert_struct(i)

                    elif i["type"]["_nodetype"]=="TypeDecl":



                        for j in i["type"]["type"]["names"]:

                            if j=="int":

                                result=""
                                result=result+int_convertor.convert_int(i)
                            elif j=="char":
                                char_convertor.convert_char(i)
                            elif j=="float":
                                float_convertor.convert_float(i)
                            elif j=="double":
                                double_convertor.convert_double(i)
                    elif i["type"]["_nodetype"]=="ArrayDecl":
                        array_convertor.convert_array(i)

                elif i["_nodetype"] == "Assignment":
                    if i["coord"] in global_values.for_loop_init:
                        pass
                    else:
                        statement_convertor.convert_statement(i)
                    #print(result)
                else:
                    get_dict_values(key,i)





            elif type(i) is list:
                get_all_values(key,i)


    get_all_values("ext",ast_dict["ext"])


transpile()

borrow_int_rust="fn borrow_i32(id:i32) -> i32{\n    let new_val;\n    new_val=id;\n    new_val\n}"
borrow_i64_rust="fn borrow_i64(id:i64) -> i64{\n    let new_val;\n    new_val=id;\n    new_val\n}"
borrow_i128_rust="fn borrow_i128(id:i28) -> i128{\n    let new_val;\n    new_val=id;\n    new_val\n}"

borrow_float_rust="fn borrow_float(id:f32) -> f32{\n    let new_val;\n    new_val=id;\n    new_val\n}"
borrow_char_rust="fn borrow_char(id:char) -> char{\n    let new_val;\n    new_val=id;\n    new_val\n}"
borrow_double_rust="fn borrow_double(id:f64) -> f64{\n    let new_val;\n    new_val=id;\n    new_val\n}"

if global_values.i32_borrow:
    write_to_rust_file(borrow_int_rust,'a')

    print(borrow_int_rust)
if global_values.i64_borrow:
    write_to_rust_file(borrow_i64_rust,'a')

    print(borrow_i64_rust)
if global_values.i128_borrow:
    write_to_rust_file(borrow_i128_rust,'a')

    print(borrow_i128_rust)
if global_values.float_borrow:
    write_to_rust_file(borrow_float_rust,'a')

    print(borrow_float_rust)
if global_values.char_borrow:
    write_to_rust_file(borrow_double_rust,'a')

    print(borrow_char_rust)
if global_values.double_borrow:
    write_to_rust_file(borrow_double_rust,'a')

    print(borrow_double_rust)


























