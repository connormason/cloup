# Fork Changelog

List of changes made to [connormason/cloup](https://github.com/connormason/cloup) that diverge from the default
[cloup](https://github.com/janluke/cloup) library

## Option Groups
- Option groups accept a `post_parse_callback`, which is run after arguments are parsed, and allows manipulation of the
context. This is useful for more complicated option group factories
