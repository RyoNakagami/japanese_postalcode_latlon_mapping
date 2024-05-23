def dict_flatten(dictionary: dict, feature: str) -> dict:
    items = []
    for key, value in dictionary.items():
        items.append([key, value[feature]])
    return dict(items)
