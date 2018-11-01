
class FormHelper():

    @staticmethod
    def make_options(model_items, option_all=True):
        options = []
        if option_all:
            options.append((-1, 'Все'))
        for item in model_items:
            options.append((item.id, item.name))
        return options

    @staticmethod
    def get_option_id(model_items, alias):
        for item in model_items:
            if item.alias == alias:
                return item.id

    @staticmethod
    def get_params_from_post(params_keys, request):
        params = {}
        for key in params_keys:
            if params_keys[key] in ('bool', 'int'):
                params[key] = request.POST.get(key)
            elif params_keys[key] == 'list':
                params[key] = request.POST.getlist(key)
        return params

    @staticmethod
    def make_acomp_options(model_items):
        options = []
        for item in model_items:
            options.append({"id": item.id, "text": item.name, "label": item.name})
        return options
