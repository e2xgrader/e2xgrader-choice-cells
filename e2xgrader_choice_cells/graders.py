from logging import Logger
from typing import Optional, Tuple

from e2xgrader_core.base.grader import BaseGrader
from nbformat.notebooknode import NotebookNode

from .utils import get_choices, get_instructor_choices


class SingleChoiceGrader(BaseGrader):
    """
    Grader for single choice cells.
    """

    def determine_grade(
        self, cell: NotebookNode, log: Optional[Logger] = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata.get("nbgrader", {}).get("points"))
        student_choices = get_choices(cell)
        instructor_choices = get_instructor_choices(cell)
        if (
            (len(student_choices) > 0)
            and (len(instructor_choices) > 0)
            and (student_choices == instructor_choices)
        ):
            return max_points, max_points
        return 0.0, max_points


class MultipleChoiceGrader(BaseGrader):
    """
    Grader for multiple choice cells.
    Student must select all correct answers and no incorrect answers.
    """

    def determine_grade(
        self, cell: NotebookNode, log: Optional[Logger] = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata.get("nbgrader", {}).get("points"))
        student_choices = get_choices(cell)
        instructor_choices = get_instructor_choices(cell)
        # Return 0 points if the student did not select all correct answers
        for choice in instructor_choices:
            if choice not in student_choices:
                return 0, max_points

        # Return 0 points if the student did select an incorrect answer
        for choice in student_choices:
            if choice not in instructor_choices:
                return 0, max_points

        return max_points, max_points


singlechoice_grader: Tuple[str, BaseGrader] = ("singlechoice", SingleChoiceGrader())
multiplechoice_grader: Tuple[str, BaseGrader] = ("multiplechoice", MultipleChoiceGrader())
