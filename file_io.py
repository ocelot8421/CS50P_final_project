def save_elements_into_python_file(elements, file_name):
        
    with open(file_name, mode="w", encoding="utf-8") as output_file:
            output_file.write("default_gardening_elements = [\n")
            for element in elements:
                output_file.write("    " + str(element)+ ",\n")                
            output_file.write("]")