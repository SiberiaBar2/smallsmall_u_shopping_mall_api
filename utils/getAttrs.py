def get_attrs(object):
    class_vars = {
        key: value for key, value in object.__dict__.items()
        if not callable(value) and not key.startswith('__')
    }

    return class_vars

def get_methods(object):
    class_methods = {
        key: value for key, value in object.__dict__.items()
        if callable(value) and not key.startswith('__')
    }

    return class_methods
