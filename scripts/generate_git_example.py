from __future__ import annotations

import random
from pathlib import Path

random.seed(12345)

EXAMPLE_FILE_PATH = Path(__file__).parent.parent / 'examples/git_sections.py'
MAX_SECTION_COUNT = 3
MAX_COMMANDS_PER_SECTION = 3

GIT_HELP = """
start a working area (see also: git help tutorial)
   clone             Clone a repository into a new directory
   init              Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add               Add file contents to the index
   mv                Move or rename a file, a directory, or a symlink
   restore           Restore working tree files
   rm                Remove files from the working tree and from the index
   sparse-checkout   Initialize and modify the sparse-checkout

examine the history and state (see also: git help revisions)
   bisect            Use binary search to find the commit that introduced a bug
   diff              Show changes between commits, commit and working tree, etc
   grep              Print lines matching a pattern
   log               Show commit logs
   show              Show various types of objects
   status            Show the working tree status

grow, mark and tweak your common history
   branch            List, create, or delete branches
   commit            Record changes to the repository
   merge             Join two or more development histories together
   rebase            Reapply commits on top of another base tip
   reset             Reset current HEAD to the specified state
   switch            Switch branches
   tag               Create, list, delete or verify a tag object signed with GPG
""".strip()

CODE_TEMPLATE = """
\"\"\"
This example shows how to use ``cloup.Section`` to organize the subcommands of
a multi-command in many ``--help`` sections.

The code was generated by parsing "git --help" and taking
- the first {max_section_count} sections
- for each section, the first {max_commands_per_section} commands after shuffling them.
\"\"\"
import cloup


def f(**kwargs):
    \"\"\" Dummy command callback \"\"\"
    print(**kwargs)


# In a real big application, you would import the following commands from separate modules =========
{command_list}
# ==================================================================================================

\"\"\"
If "align_sections=True" (default), the help column of all sections will
be aligned; otherwise, each section will be formatted independently.
\"\"\"
@cloup.group('git', align_sections=True)
def git():
    return 0

\"\"\"
git.section() creates a new Section object, adds it to git and returns it.

In the help, sections are shown in the same order they are added.
Commands in each sections are shown in the same order they are listed, unless
you pass the argument "sorted_=True".
\"\"\"
{section_list}

\"\"\"
In alternative, you can either:
- pass a list of Section objects as argument "sections" to cloup.Group or @cloup.group
- use git.add_section(section) to add an existing Section object
- use git.add_command(cmd, name, section, ...); the section must NOT contain the command
- use @git.command(cmd, name, section, ...)

Individual commands don't store the section they belong to.
Also, cloup.command doesn't accept a "section" argument.
\"\"\"

# The following commands will be added to the "default section" (a sorted Section)
git.add_command(cloup.command('fake-2', help='Fake command #2')(f))
git.add_command(cloup.command('fake-1', help='Fake command #1')(f))


if __name__ == '__main__':
    git()
""".lstrip()


def parse_help(help_text):
    sections = []
    for text in help_text.split('\n\n'):
        title, *rows = map(str.strip, text.split('\n'))
        title = title.strip().capitalize()
        commands = []
        for row in rows:
            cmd, desc = map(str.strip, row.split(' ', 1))
            commands.append((cmd, desc))
        random.shuffle(commands)
        sections.append([title, commands])
    return sections


def get_command_var_name(cmd_name):
    return 'git_' + cmd_name.replace('-', '_')


def generate(out_path=EXAMPLE_FILE_PATH,
             max_section_count=MAX_SECTION_COUNT,
             max_commands_per_section=MAX_COMMANDS_PER_SECTION):
    sections = parse_help(GIT_HELP)[:max_section_count]
    for s in sections:
        s[1] = s[1][:max_commands_per_section]

    # Subcommand definitions
    commands_buffer = []
    for _, commands in sections:
        for cmd_name, desc in commands:
            var_name = get_command_var_name(cmd_name)
            commands_buffer.append(
                f'{var_name} = cloup.command({cmd_name!r}, help={desc!r})(f)')
        commands_buffer.append('')
    commands_list = '\n'.join(commands_buffer).strip()

    # Section list
    sections_buffer = []
    for title, commands in sections:
        sections_buffer.append('git.section(')
        sections_buffer.append(f'    {title!r},')
        for cmd_name, _ in commands:
            var_name = get_command_var_name(cmd_name)
            sections_buffer.append(f'    {var_name},')
        sections_buffer.append(')')
    section_list = '\n'.join(sections_buffer)

    code = CODE_TEMPLATE.format(max_section_count=max_section_count,
                                max_commands_per_section=max_commands_per_section,
                                command_list=commands_list,
                                section_list=section_list)

    print(code)
    with open(out_path, 'w', encoding='utf-8') as out_file:
        out_file.write(code)


if __name__ == '__main__':
    generate()
