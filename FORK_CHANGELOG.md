# Fork Changelog

List of changes made to [connormason/cloup](https://github.com/connormason/cloup) that diverge from the default
[cloup](https://github.com/janluke/cloup) library

## Context
### Defaults
- The help text can be accessed with `-h` or `--help` by default (instead of just `-h`). This can be overridden by
providing the `help_option_names` context option
- The maximum content width of help text is 500 (so it fills the whole width of the terminal). This can be overridden
by providing the `max_content_width` context option

### Settings
- Added `tag_required_options`, which can be set to `False` to disable the "required" tag for required options
- Added `tag_optional_arguments`, which can be set to `False` to disable the "optional" tag for non-required arguments

## Arguments
- Arguments accept `hidden` arg, which determines if the arg is hidden from the "Positional arguments" help text
section. By default, the "Positional arguments" section is only displayed if any command arg has `help` text. `hidden`
will override this behavior (`hidden=True` will hide args with help text, `hidden=False` will show args with no help
text)
- Arguments accept `show_default` arg, which determines if the default value should be shown in the help text (just
like options)

## Options
- Options accept `nargs=-1` to consume arbitrary number of values, just like arguments do

## Option Groups
- Option groups accept a `post_parse_callback`, which is run after arguments are parsed, and allows manipulation of the
context. This is useful for more complicated option group factories
