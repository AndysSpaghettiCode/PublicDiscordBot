def parse_text(file_name_str):


    file1 = open(file_name_str, "r")

    current_line_str = file1.readline()
    path_list = []
    dialogue_list = []

    total_options_list = []
    while current_line_str:

        if current_line_str == "StartPath\n":
            path_str = file1.readline()
            path_list.append(path_str.replace("\n",""))

            while current_line_str != "EndPath\n":
                current_line_str = file1.readline()

                if not current_line_str:
                    print("error")
                    break

        elif current_line_str == "StartDialogue\n":
            dialogue_str = ""
            current_line_str = file1.readline()

            while current_line_str != "EndDialogue\n":
                dialogue_str += current_line_str
                current_line_str = file1.readline()
                if not current_line_str:
                    print("error")
                    break
            dialogue_str = dialogue_str.replace("\n"," ")
            dialogue_str = dialogue_str.replace("\space ", "\n")
            dialogue_list.append(dialogue_str)

        elif current_line_str == "StartOptions\n":
            options_list = []
            while current_line_str != "EndOptions\n" and current_line_str != "EndOptions":

                current_line_str = file1.readline()

                if current_line_str != "EndOptions\n" and current_line_str != "EndOptions":
                    current_line_str = current_line_str.replace("\n", "")
                    current_line_str = current_line_str.split(': ', 1)
                    options_list.append(current_line_str)

                if not current_line_str:
                    print("error")
                    break
            total_options_list.append(options_list)

        current_line_str = file1.readline()
    print(path_list)

    if len(path_list) == len(dialogue_list) == len(total_options_list):
        print("parsed sucessfully.... probably")
        return (path_list, dialogue_list, total_options_list)
    else:
        print("parsed unsucessfully")
        return
