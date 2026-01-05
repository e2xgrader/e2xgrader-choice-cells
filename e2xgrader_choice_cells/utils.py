from e2xgrader_core.cells.e2xgrader import (
    get_e2xgrader_cell_type,
    get_e2xgrader_metadata_value,
    set_e2xgrader_metadata_value,
)


def is_singlechoice(cell):
    """
    Check if the cell is a single choice cell.
    """
    return get_e2xgrader_cell_type(cell) == "singlechoice"


def is_multiplechoice(cell):
    """
    Check if the cell is a multiple choice cell.
    """
    return get_e2xgrader_cell_type(cell) == "multiplechoice"


def get_choices(cell):
    """
    Get the choices from a cell.
    """
    choices = []
    if is_singlechoice(cell) or is_multiplechoice(cell):
        choices = get_e2xgrader_metadata_value(cell, "choice", default=[])
        choices = [int(choice) for choice in choices]
    return choices


def has_instructor_choices(cell):
    """
    Check if the cell has instructor choices.
    """
    source = get_e2xgrader_metadata_value(cell, "source", default={})
    return "choice" in source


def get_instructor_choices(cell):
    """
    Get the instructor choices from a cell.
    """
    source = get_e2xgrader_metadata_value(cell, "source", default={})
    choices = source.get("choice", [])
    return [int(choice) for choice in choices]


def clear_choices(cell):
    """
    Clear the choices from a cell.
    """
    if is_singlechoice(cell) or is_multiplechoice(cell):
        set_e2xgrader_metadata_value(cell, "choice", [])
