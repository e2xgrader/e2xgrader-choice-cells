from typing import Any, Callable, Dict, Tuple, Union

from bs4 import BeautifulSoup
from bs4.element import Tag

from .utils import (
    get_choices,
    get_instructor_choices,
    has_instructor_choices,
    is_multiplechoice,
    is_singlechoice,
)


def create_input_box(soup: BeautifulSoup, input_type: str, index: int, cell: Dict[str, Any]) -> Tag:
    """Create an input box for the choice cell.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.
        input_type (str): The type of input box (radio or checkbox).
        index (int): The index of the choice.
        cell (Dict[str, Any]): The cell data.
    Returns:
        Tag: The input box tag.
    """
    box = soup.new_tag("input")
    box["type"] = input_type
    box["value"] = str(index)
    box["disabled"] = "disabled"
    if index in get_choices(cell):
        box["checked"] = "checked"
    return box


def create_instructor_feedback(
    soup: BeautifulSoup, index: int, cell: Dict[str, Any]
) -> Union[Tag, None]:
    """Create instructor feedback for the choice cell.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.
        index (int): The index of the choice.
        cell (Dict[str, Any]): The cell data.
    Returns:
        Union[Tag, None]: The feedback tag or None if no feedback is needed.
    """
    if not has_instructor_choices(cell):
        return None
    feedback = soup.new_tag("span")
    if index in get_instructor_choices(cell):
        feedback.string = "correct"
        feedback["style"] = "color:green"
    else:
        feedback.string = "false"
        feedback["style"] = "color:red"
    return feedback


def process_list_item(
    soup: BeautifulSoup,
    list_item: Tag,
    input_type: str,
    index: int,
    cell: Dict[str, Any],
) -> Tag:
    """Process a single list item and convert it to a choice cell.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.
        list_item (Tag): The list item tag.
        input_type (str): The type of input box (radio or checkbox).
        index (int): The index of the choice.
        cell (Dict[str, Any]): The cell data.
    Returns:
        Tag: The processed list item tag.
    """
    div = soup.new_tag("div")
    box = create_input_box(soup, input_type, index, cell)
    div.append(box)

    # Append children of the list item to the div
    for child in list_item.children:
        div.append(child)

    # Add instructor feedback if applicable
    feedback = create_instructor_feedback(soup, index, cell)
    if feedback:
        div.append(feedback)

    return div


def to_choice_cell(context: Dict[str, Any], source: str) -> str:
    """Convert a cell to a choice cell.

    Args:
        context (Dict[str, Any]): The context dictionary.
        source (str): The source HTML string.
    Returns:
        str: The modified HTML string.
    """
    cell = context.get("cell", {})
    soup = BeautifulSoup(source, "html.parser")
    if is_singlechoice(cell):
        input_type = "radio"
    elif is_multiplechoice(cell):
        input_type = "checkbox"
    else:
        input_type = None

    if not input_type:
        return source

    ul = soup.ul
    if not ul:
        return source

    form = soup.new_tag("form")
    form["class"] = "hbrs_checkbox"

    list_elems = ul.find_all("li")
    for i, list_item in enumerate(list_elems):
        div = process_list_item(soup, list_item, input_type, i, cell)
        form.append(div)

    ul.replace_with(form)
    return soup.prettify().replace("\n", "")


multiplechoice_filter: Tuple[str, Callable[[Any, str], str]] = (
    "multiplechoice",
    to_choice_cell,
)

singlechoice_filter: Tuple[str, Callable[[Any, str], str]] = (
    "singlechoice",
    to_choice_cell,
)
