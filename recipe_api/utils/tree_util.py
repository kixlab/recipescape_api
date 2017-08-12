def make_tree(recipe, annotation):
    tags = annotation.annotations
    instructions = recipe.instructions['instructions']
    nodes = []
    current_node = {"word": "", "ingredient": []}
    for tag in tags:
        if current_node["word"] == "" and tag['tag'] == 0:
            current_node["word"] = get_word(instructions, tag['index'])
        elif current_node["word"] != "" and tag['tag'] == 0:
            nodes.append(current_node)
            current_node = {"word": "", "ingredient": []}
        elif current_node["word"] == "" and tag['tag'] == 0:
            pass
        elif current_node["word"] != "" and tag['tag'] == 1:
            current_node['ingredient'].append(get_word(instructions, tag['index']))
    return nodes


def get_word(instructions, index):
    """
    :param instruction: json object of instruction.
    :param index: [int, int, int]
    :return:
    """
    sentences  = instructions[index[0]]
    tokens = sentences[index[1]]
    word = tokens['tokens'][index[2]]['originalText']
    return word.lower()
