import click


class GroupedOption(click.Option):
    """A click.Option with an extra field ``group`` of type ``OptionGroup``."""

    def __init__(self, *args, group=None, **attrs):
        super().__init__(*args, **attrs)
        self.group = group


argument = click.argument


def option(*param_decls, cls=None, group=None, **kwargs):
    """Attaches an ``Option`` to the command.
    Refer to :class:`click.Option` and :class:`click.Parameter` for more info
    about the accepted parameters.
    """
    if cls is None:
        cls = GroupedOption

    def decorator(f):
        func = click.option(*param_decls, cls=cls, **kwargs)(f)
        new_option = func.__click_params__[-1]
        new_option.group = group
        if group and group.hidden:
            new_option.hidden = True
        return func

    return decorator