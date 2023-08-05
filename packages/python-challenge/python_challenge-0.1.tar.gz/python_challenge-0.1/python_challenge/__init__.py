def is_val_in_tree(tree, val):
    if isinstance(tree, list):
        return any(is_val_in_tree(subtree, val) for subtree in tree)
    return tree == val