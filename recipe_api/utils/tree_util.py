import collections


def index_normalizer(index, len_bin, len_node):
    if 0 <= index < 3:
        return index
    elif len_node - 3 <= index < len_node:
        diff = len_node - len_bin
        return index - diff
    else:
        ratio = (len_node - 3) / (len_bin - 3)
        normalized_index = int(index / ratio)
        return normalized_index


def analyze_trees(trees):
    """
    Return
    1) 3 most frequent actions, (and their 3 most co-occurring ingredient, histogram)
    2) 3 most frequent ingredients, (...)
    """
    bin_size = 9
    action_bins = collections.defaultdict(lambda: [0 for _ in range(bin_size)])
    ingredient_bins = collections.defaultdict(lambda: [0 for _ in range(bin_size)])
    action_ingredient_count = collections.defaultdict(lambda: collections.defaultdict(int))
    ingredient_action_count = collections.defaultdict(lambda: collections.defaultdict(int))

    for tree in trees:
        for index, t in enumerate(tree):
            action = t['word']
            action_bins[action][index_normalizer(index, bin_size, len(tree))] += 1
            for ingredient in t['ingredient']:
                ingredient_bins[ingredient][index_normalizer(index, 9, len(tree))] += 1
                action_ingredient_count[action][ingredient] += 1
                ingredient_action_count[ingredient][action] += 1

    actions_sorted = sorted(action_bins.items(), key=lambda p: sum(p[1]), reverse=True)
    ingredients_sorted = sorted(ingredient_bins.items(), key=lambda p: sum(p[1]), reverse=True)
    top3_action = [k[0] for k in actions_sorted[:3]]
    top3_ingredient = [k[0] for k in ingredients_sorted[:3]]

    result = {"actions": [], "ingredients": []}
    for action in top3_action:
        frequent_neighbors = sorted(action_ingredient_count[action].items(), key=lambda p: p[1], reverse=True)
        result['actions'].append({
            "action": action,
            "histogram": action_bins[action],
            "neighbors": [p[0] for p in frequent_neighbors[:3]]
        })
    for ingredient in top3_ingredient:
        frequent_neighbors = sorted(ingredient_action_count[ingredient].items(), key=lambda p: p[1], reverse=True)
        result['ingredients'].append({
            "ingredient": ingredient,
            "histogram": ingredient_bins[ingredient],
            "neighbors": [p[0] for p in frequent_neighbors[:3]]
        })
    return result


def make_node(recipe, annotation):
    tree = make_tree(annotation.recipe, annotation)
    actions = [t['word'] for t in tree]
    ingredients = [item for t in tree for item in t['ingredient']]
    return {'actions': actions, 'ingredients': ingredients }


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
