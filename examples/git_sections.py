"""
This example shows how to use ``cloup.Section`` to organize the subcommands of
a multi-command in many ``--help`` sections.

The code was generated by parsing ``git --help`` and taking
- the first 3 sections;
- for each section, the first 3 commands after shuffling them.
"""
from __future__ import annotations

import cloup


def f(**kwargs):
    """Dummy command callback."""
    print(**kwargs)


# In a real big application, you would import the following commands from separate modules =========
git_clone = cloup.command('clone', help='Clone a repository into a new directory')(f)
git_init = cloup.command('init', help='Create an empty Git repository or reinitialize an existing one')(f)

git_rm = cloup.command('rm', help='Remove files from the working tree and from the index')(f)
git_sparse_checkout = cloup.command('sparse-checkout', help='Initialize and modify the sparse-checkout')(f)
git_mv = cloup.command('mv', help='Move or rename a file, a directory, or a symlink')(f)

git_status = cloup.command('status', help='Show the working tree status')(f)
git_diff = cloup.command('diff', help='Show changes between commits, commit and working tree, etc')(f)
git_bisect = cloup.command('bisect', help='Use binary search to find the commit that introduced a bug')(f)


# ==================================================================================================


# If "align_sections=True" (default), the help column of all sections will
# be aligned; otherwise, each section will be formatted independently.
@cloup.group('git', align_sections=True)
def git():
    return 0


"""
git.section() creates a new Section object, adds it to git and returns it.

In the help, sections are shown in the same order they are added.
Commands in each sections are shown in the same order they are listed, unless
you pass the argument "sorted=True".
"""
git.section(
    'Start a working area (see also: git help tutorial)',
    git_clone,
    git_init,
)
git.section(
    'Work on the current change (see also: git help everyday)',
    git_rm,
    git_sparse_checkout,
    git_mv,
)
git.section(
    'Examine the history and state (see also: git help revisions)',
    git_status,
    git_diff,
    git_bisect,
)

"""
In alternative, you can either:
- pass a list of Section objects as argument "sections" to cloup.Group or @cloup.group
- use git.add_section(section) to add an existing Section object
- use git.add_command(cmd, name, section, ...); the section must NOT contain the command
- use @git.command(cmd, name, section, ...)

Individual commands don't store the section they belong to.
Also, cloup.command doesn't accept a "section" argument.
"""

# The following commands will be added to the "default section" (a sorted Section)
git.add_command(cloup.command('fake-2', help='Fake command #2')(f))
git.add_command(cloup.command('fake-1', help='Fake command #1')(f))

if __name__ == '__main__':
    git()
