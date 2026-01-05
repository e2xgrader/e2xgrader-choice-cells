import json
from typing import Tuple, Type

import nbgrader.utils as nbgrader_utils
from e2xgrader_base.cells.e2xgrader import set_e2xgrader_metadata_value
from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.api import MissingEntry
from nbgrader.preprocessors import NbGraderPreprocessor

from .utils import clear_choices


class ChoiceCellPreprocessor:

    @staticmethod
    def clear_hidden_tests(
        preprocessor: NbGraderPreprocessor,
        cell: NotebookNode,
        resources: ResourcesDict,
        cell_index: int,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Preprocess a cell to clear hidden tests.

        Args:
            preprocessor (NbGraderPreprocessor): The preprocessor instance.
            cell (NotebookNode): The cell to preprocess.
            resources (ResourcesDict): The resources dictionary.
            cell_index (int): The index of the cell.

        Returns:
            Tuple[NotebookNode, ResourcesDict]: The preprocessed cell and resources.
        """

        clear_choices(cell)

        return cell, resources

    @staticmethod
    def overwrite_cells(
        preprocessor: NbGraderPreprocessor,
        cell: NotebookNode,
        resources: ResourcesDict,
        cell_index: int,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Preprocess a cell to overwrite cells.

        Args:
            preprocessor (NbGraderPreprocessor): The preprocessor instance.
            cell (NotebookNode): The cell to preprocess.
            resources (ResourcesDict): The resources dictionary.
            cell_index (int): The index of the cell.

        Returns:
            Tuple[NotebookNode, ResourcesDict]: The preprocessed cell and resources.
        """

        grade_id = cell.metadata.get("nbgrader", {}).get("grade_id", None)
        if grade_id is None:
            return cell, resources
        try:
            source_cell = preprocessor.gradebook.find_source_cell(
                grade_id,
                preprocessor.notebook_id,
                preprocessor.assignment_id,
            )
        except MissingEntry:
            preprocessor.log.warning(
                (
                    f"Could not find source cell for grade_id {grade_id} "
                    f"in notebook {preprocessor.notebook_id}"
                )
            )
            del cell.metadata["nbgrader"]["grade_id"]
            return cell, resources

        set_e2xgrader_metadata_value(
            cell,
            "source",
            json.loads(source_cell.source),
        )

        return cell, resources

    @staticmethod
    def save_cells(
        preprocessor: NbGraderPreprocessor,
        cell: NotebookNode,
        resources: ResourcesDict,
        cell_index: int,
    ) -> Tuple[NotebookNode, ResourcesDict]:
        """
        Preprocess a cell to save cells.

        Args:
            preprocessor (NbGraderPreprocessor): The preprocessor instance.
            cell (NotebookNode): The cell to preprocess.
            resources (ResourcesDict): The resources dictionary.
            cell_index (int): The index of the cell.

        Returns:
            Tuple[NotebookNode, ResourcesDict]: The preprocessed cell and resources.
        """
        if nbgrader_utils.is_grade(cell):
            preprocessor._create_grade_cell(cell)

        if nbgrader_utils.is_solution(cell):
            preprocessor._create_solution_cell(cell)

        if nbgrader_utils.is_task(cell):
            preprocessor._create_task_cell(cell)

        if (
            nbgrader_utils.is_grade(cell)
            or nbgrader_utils.is_solution(cell)
            or nbgrader_utils.is_locked(cell)
            or nbgrader_utils.is_task(cell)
        ):
            grade_id = cell.metadata.nbgrader["grade_id"]

            try:
                source_cell = preprocessor.gradebook.find_source_cell(
                    grade_id, preprocessor.notebook_id, preprocessor.assignment_id
                ).to_dict()
                del source_cell["name"]
                del source_cell["notebook"]
                del source_cell["assignment"]
            except MissingEntry:
                source_cell = {}

            source = json.dumps(cell.metadata.extended_cell)

            source_cell.update(
                {
                    "cell_type": cell.cell_type,
                    "locked": nbgrader_utils.is_locked(cell),
                    "source": source,
                    "checksum": cell.metadata.nbgrader.get("checksum", None),
                }
            )

            preprocessor.new_source_cells[grade_id] = source_cell

        return cell, resources


singlechoice_preprocessor: Tuple[str, Type] = ("singlechoice", ChoiceCellPreprocessor)
multiplechoice_preprocessor: Tuple[str, Type] = (
    "multiplechoice",
    ChoiceCellPreprocessor,
)
