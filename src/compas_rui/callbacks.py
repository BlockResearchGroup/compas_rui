import scriptcontext as sc  # type: ignore


def register_callback(callback):
    if callback.__name__ not in sc.sticky:
        sc.sticky[callback.__name__] = True
        sc.doc.ReplaceRhinoObject += callback
