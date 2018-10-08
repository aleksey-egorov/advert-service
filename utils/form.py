

def make_options(model_items):
    options = [(-1, 'Все')]
    for item in model_items:
        options.append((item.id, item.name))
    return options