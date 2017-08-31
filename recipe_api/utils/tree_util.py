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


def analyze_trees(trees, cluster_labels):
    """
    Return
    1) 3 most frequent actions, (and their 3 most co-occurring ingredient, histogram)
    2) 3 most frequent ingredients, (...)
    """
    bin_size = 9
    action_bins = collections.defaultdict(lambda: [[] for _ in range(bin_size)])
    ingredient_bins = collections.defaultdict(lambda: [[] for _ in range(bin_size)])
    action_ingredient_count = collections.defaultdict(lambda: collections.defaultdict(int))
    ingredient_action_count = collections.defaultdict(lambda: collections.defaultdict(int))

    for tree in trees:
        for index, t in enumerate(tree):
            cluster_label = cluster_labels[index]
            normalized_index = index_normalizer(index, bin_size, len(tree))
            action = t['word']
            action_bins[action][normalized_index].append(cluster_label)
            for ingredient in t['ingredient']:
                ingredient_bins[ingredient][normalized_index].append(cluster_label)
                action_ingredient_count[action][ingredient] += 1
                ingredient_action_count[ingredient][action] += 1

    actions_sorted = sorted(action_bins.items(), key=lambda p: sum(map(len, p[1])), reverse=True)
    ingredients_sorted = sorted(ingredient_bins.items(), key=lambda p: sum(map(len, p[1])), reverse=True)
    top3_action = [k[0] for k in actions_sorted[:3]]
    top3_ingredient = [k[0] for k in ingredients_sorted[:3]]

    result = {"actions": [], "ingredients": []}
    for action in top3_action:
        frequent_neighbors = sorted(action_ingredient_count[action].items(), key=lambda p: p[1], reverse=True)
        result['actions'].append({
            "action": action,
            "histogram": map(len, action_bins[action]),
            "histogram_detail": map(into_proportion, action_bins[action]),
            "neighbors": [p[0] for p in frequent_neighbors[:3]]
        })
    for ingredient in top3_ingredient:
        frequent_neighbors = sorted(ingredient_action_count[ingredient].items(), key=lambda p: p[1], reverse=True)
        result['ingredients'].append({
            "ingredient": ingredient,
            "histogram": map(len, ingredient_bins[ingredient]),
            "histogram_detail": map(into_proportion, ingredient_bins[ingredient]),
            "neighbors": [p[0] for p in frequent_neighbors[:3]],
        })
    return result


def count_tree_with_filter(trees, action, ingredient):
    bin_size = 9
    bins = [0 for _ in range(bin_size)]
    for tree in trees:
        for index, t in enumerate(tree):
            if t['word'] == action and ingredient in t['ingredient']:
                bins[index_normalizer(index, bin_size, len(tree))] += 1
    return bins


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
    last_ingredient_index = [-1, -1, -1]
    for tag in tags:
        if current_node["word"] == "" and tag['tag'] == 0:
            current_node["word"] = get_word(instructions, tag['index'])
        elif current_node["word"] != "" and tag['tag'] == 0:
            nodes.append(current_node)
            current_node = {"word": "", "ingredient": []}
        elif current_node["word"] == "" and tag['tag'] == 0:
            pass
        elif current_node["word"] != "" and tag['tag'] == 1:
            ingredient = get_word(instructions, tag['index'])
            is_continued_ingredient = (
                last_ingredient_index[0] == tag['index'][0] and last_ingredient_index[1] == tag['index'][1] and
                last_ingredient_index[2] == tag['index'][2] - 1)
            if is_continued_ingredient:
                current_node['ingredient'][-1] += (' ' + ingredient)
            else:
                current_node['ingredient'].append(ingredient)
            last_ingredient_index = tag['index']
    return nodes


def get_word(instructions, index):
    """
    :param instruction: json object of instruction.
    :param index: [int, int, int]
    :return:
    """
    token = get_token(instructions, index)
    word = token['originalText']
    return word.lower()


def get_token(instructions, index):
    sentences = instructions[index[0]]
    tokens = sentences[index[1]]
    token = tokens['tokens'][index[2]]
    return token


def into_proportion(items):
    counter = collections.Counter(items)
    total_count = sum(counter.values())
    proportions = {k: v / total_count for k, v in counter.items()}
    return proportions
