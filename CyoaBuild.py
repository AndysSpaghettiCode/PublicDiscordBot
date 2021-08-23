import discord


class cyoa_node:
    def __init__(self, loc, dia, options):
        self.loc = loc
        self.dia = dia
        self.options = options


def cyoa_dict(path_import_list, dialogue_import_list, options_import_list):

    cyoa_nodes_list = [cyoa_node(path_import_list[i], dialogue_import_list[i], options_import_list[i]) for i in range(len(path_import_list))]
    cyoa_nodes_dict = dict()

    for i in range(len(cyoa_nodes_list)):
        cyoa_nodes_dict[cyoa_nodes_list[i].loc] = cyoa_nodes_list[i]

    return cyoa_nodes_dict

async def print_node(ctx_obj, current_node_obj):
    return_message_str =  current_node_obj.dia + "\n"
    for idx_int in range(len(current_node_obj.options)):
        return_message_str += "\n"
        return_message_str += str(idx_int+1) + ": " + current_node_obj.options[idx_int][1]
    await ctx_obj.channel.send(return_message_str)


def next_node(cyoa_nodes_dict, current_node_obj, choice_num_str):

    sent_list = current_node_obj.options[int(choice_num_str)-1][0].split(' ', 1)

    if sent_list[0] == "Option":
        if current_node_obj.loc != "0":
            dict_key_str = current_node_obj.loc + "." + sent_list[1]
        else:
            dict_key_str = sent_list[1]
        next_node_obj = cyoa_nodes_dict[dict_key_str]
    elif sent_list[0] == "Redirect":
        next_node_obj = cyoa_nodes_dict[sent_list[1]]

    return next_node_obj






