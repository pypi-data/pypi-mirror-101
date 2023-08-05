"""The implementation of manipulating HTL and js expression files.

Mainly following interfaces are defined:

- empty_expression_dir : Remove expression directory
    (EXPRESSION_ROOT_DIR) to initialize.
- append_expression : Append html and js expression to file.
- wrap_by_script_tag_and_append_expression : Wrap an expression
    string by script tags and append it's expression to file.
- get_current_expression : Get current expression string.
- remove_expression_file : Remove expression file.
"""

import os
from typing import List

EXPRESSION_ROOT_DIR: str = '../.apysc_expression/'
EXPRESSION_FILE_PATH: str = os.path.join(
    EXPRESSION_ROOT_DIR, 'expression.txt')
INDENT_NUM_FILE_PATH: str = os.path.join(
    EXPRESSION_ROOT_DIR, 'indent_num.txt')
LAST_SCOPE_FILE_PATH: str = os.path.join(
    EXPRESSION_ROOT_DIR, 'last_scope.txt')


def empty_expression_dir() -> None:
    """
    Remove expression directory (EXPRESSION_ROOT_DIR) to initialize.
    """
    from apysc.file import file_util
    file_util.empty_directory(directory_path=EXPRESSION_ROOT_DIR)


def append_expression(expression: str) -> None:
    """
    Append html and js expression to file.

    Parameters
    ----------
    expression : str
        HTML and js Expression string.
    """
    from apysc.expression import indent_num
    from apysc.expression import last_scope
    from apysc.file import file_util
    from apysc.string import indent_util
    current_indent_num: int = indent_num.get_current_indent_num()
    expression = indent_util.append_spaces_to_expression(
        expression=expression, indent_num=current_indent_num)
    dir_path: str = file_util.get_abs_directory_path_from_file_path(
        file_path=EXPRESSION_FILE_PATH)
    os.makedirs(dir_path, exist_ok=True)
    file_util.append_plain_txt(
        txt=f'{expression}\n', file_path=EXPRESSION_FILE_PATH)
    _merge_script_section()
    last_scope.set_last_scope(value=last_scope.LastScope.NORMAL)


def wrap_by_script_tag_and_append_expression(expression: str) -> None:
    """
    Wrap an expression string by script tags and append it's
    expression to file (helper function of `append_expression`).

    Parameters
    ----------
    expression : str
        HTML and js Expression string.
    """
    from apysc.html import html_util
    expression = html_util.wrap_expression_by_script_tag(
        expression=expression)
    append_expression(expression=expression)


def _merge_script_section() -> None:
    """
    Merge expression's script section (If there are multiple
    script tag in expression file, then they will be merged).
    """
    from apysc.file import file_util
    from apysc.html import html_const
    from apysc.html.html_util import ScriptLineUtil
    result_expression: str = ''
    current_expression: str = file_util.read_txt(
        file_path=EXPRESSION_FILE_PATH)
    current_exp_lines: List[str] = current_expression.splitlines()
    script_line_util: ScriptLineUtil = ScriptLineUtil(
        html=current_expression)
    script_strings: str = ''
    for i, current_exp_line in enumerate(current_exp_lines):
        if current_exp_line == html_const.SCRIPT_START_TAG:
            continue
        if current_exp_line == html_const.SCRIPT_END_TAG:
            continue
        line_num: int = i + 1
        if script_line_util.is_script_line(line_number=line_num):
            if current_exp_line == '':
                continue
            script_strings += f'{current_exp_line}\n'
            continue
        result_expression += f'{current_exp_line}\n'
    if script_strings != '':
        result_expression += (
            f'{html_const.SCRIPT_START_TAG}\n'
            f'{script_strings}'
            f'{html_const.SCRIPT_END_TAG}\n'
        )
    file_util.save_plain_txt(
        txt=result_expression,
        file_path=EXPRESSION_FILE_PATH)


def get_current_expression() -> str:
    """
    Get current expression's string from file.

    Returns
    -------
    current_expression : str
        Current expression's string.
    """
    from apysc.file import file_util
    if not os.path.isfile(EXPRESSION_FILE_PATH):
        return ''
    current_expression: str = file_util.read_txt(
        file_path=EXPRESSION_FILE_PATH)
    current_expression = current_expression.strip()
    return current_expression


def remove_expression_file() -> None:
    """
    Remove expression file.
    """
    from apysc.file import file_util
    file_util.remove_file_if_exists(file_path=EXPRESSION_FILE_PATH)
