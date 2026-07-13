import {
  CellPresets,
  E2xGraderCellRegistry,
  E2XMarkdownCell,
  NbgraderCellType,
  E2xGraderSharedCell
} from '@e2xgrader/core';
import { Widget } from '@lumino/widgets';
import { TranslationBundle } from '@jupyterlab/translation';

const BASE_CELL_TYPE: string = 'markdown';
const NBGRADER_CELL_TYPE: NbgraderCellType = NbgraderCellType.TASK;

export namespace ChoiceCellUtils {
  export function get_choices(cell: E2XMarkdownCell): string[] {
    return cell.getE2xMetadataField('choice') ?? [];
  }

  export function set_choices(cell: E2XMarkdownCell, choices: string[]): void {
    cell.setE2xMetadataField('choice', choices);
  }

  export function add_choice(cell: E2XMarkdownCell, choice: string): void {
    const choices = get_choices(cell);
    if (!choices.includes(choice)) {
      choices.push(choice);
      set_choices(cell, choices);
    }
  }
  export function remove_choice(cell: E2XMarkdownCell, choice: string): void {
    const choices = get_choices(cell);
    const index = choices.indexOf(choice);
    if (index !== -1) {
      choices.splice(index, 1);
      set_choices(cell, choices);
    }
  }

  export function get_choice_count(cell: E2XMarkdownCell): number {
    return cell.getE2xMetadataField('num_of_choices') ?? 0;
  }
  export function set_choice_count(cell: E2XMarkdownCell, count: number): void {
    cell.setE2xMetadataField('num_of_choices', count);
  }

  export function get_choice(cell: E2XMarkdownCell): string {
    return cell.getE2xMetadataField('choice') ?? '';
  }

  export function set_choice(cell: E2XMarkdownCell, choice: string): void {
    cell.setE2xMetadataField('choice', choice);
  }
}

export class MultipleChoice
  implements E2xGraderCellRegistry.IE2xGraderCellPlugin
{
  public cellType: string = MultipleChoice.E2X_MULTIPLECHOICE_CELL_TYPE;
  public label: string = this._trans.__('Multiple Choice');
  public cleanMetadata: Record<string, any> = MultipleChoice.cleanMetadata;

  constructor(private _trans: TranslationBundle) {}

  createChoiceElement(
    cell: E2XMarkdownCell,
    value: string,
    selected: boolean
  ): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'checkbox';
    choice.name = cell.model.id;
    choice.value = value;
    choice.id = choice.name + '-choice-' + choice.value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        ChoiceCellUtils.add_choice(cell, value);
      } else {
        ChoiceCellUtils.remove_choice(cell, value);
      }
    };
    return choice;
  }

  public renderCell(widget: Widget, cell: E2XMarkdownCell): void {
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(MultipleChoice.E2X_MULTIPLECHOICE_FORM_CLASS);
    if (ChoiceCellUtils.get_choice_count(cell) !== items.length) {
      ChoiceCellUtils.set_choice_count(cell, items.length);
      ChoiceCellUtils.set_choices(cell, []);
    }
    const choices = ChoiceCellUtils.get_choices(cell);
    items.forEach((item, index) => {
      const input = this.createChoiceElement(
        cell,
        index.toString(),
        choices.includes(index.toString())
      );
      const label = document.createElement('label');
      label.htmlFor = input.id;
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }

  public getTaskPreset(
    taskName?: string,
    points?: number
  ): E2xGraderSharedCell[] {
    return [
      {
        cell_type: BASE_CELL_TYPE,
        metadata: CellPresets.getCleanMetadata(NBGRADER_CELL_TYPE, {
          e2xgraderCellType: MultipleChoice.E2X_MULTIPLECHOICE_CELL_TYPE,
          taskName: taskName,
          points: points
        }),
        source: this._trans.__(
          '## Multiplechoice Question\n' +
            '\n' +
            '- Choice 1\n' +
            '- Choice 2\n' +
            '- Choice 3\n' +
            '\n' +
            '<!-- Hint: Add the choices as list items, then run the cell and select the correct answer(s). -->'
        )
      }
    ];
  }
}

export namespace MultipleChoice {
  export const E2X_MULTIPLECHOICE_CELL_TYPE = 'multiplechoice';
  export const E2X_MULTIPLECHOICE_FORM_CLASS = 'e2x-multiplechoice-form';

  export const cleanMetadata = {
    choice: [] as string[],
    num_of_choices: 0,
    type: E2X_MULTIPLECHOICE_CELL_TYPE
  } as Record<string, any>;
}

export class SingleChoice
  implements E2xGraderCellRegistry.IE2xGraderCellPlugin
{
  public cellType: string = SingleChoice.E2X_SINGLECHOICE_CELL_TYPE;
  public label: string = this._trans.__('Single Choice');
  public cleanMetadata: Record<string, any> = SingleChoice.cleanMetadata;

  constructor(private _trans: TranslationBundle) {}

  createChoiceElement(
    cell: E2XMarkdownCell,
    value: string,
    selected: boolean
  ): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'radio';
    choice.name = cell.model.id;
    choice.value = value;
    choice.id = choice.name + '-choice-' + choice.value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        ChoiceCellUtils.set_choice(cell, value);
      }
    };
    return choice;
  }

  public renderCell(widget: Widget, cell: E2XMarkdownCell): void {
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(SingleChoice.E2X_SINGLECHOICE_FORM_CLASS);
    const choice = ChoiceCellUtils.get_choice(cell);
    if (choice !== '' && parseInt(choice) >= items.length) {
      ChoiceCellUtils.set_choice(cell, '');
    }
    items.forEach((item, index) => {
      const input = this.createChoiceElement(
        cell,
        index.toString(),
        choice === index.toString()
      );
      const label = document.createElement('label');
      label.htmlFor = input.id;
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }

  public getTaskPreset(
    taskName?: string,
    points?: number
  ): E2xGraderSharedCell[] {
    return [
      {
        cell_type: BASE_CELL_TYPE,
        metadata: CellPresets.getCleanMetadata(NBGRADER_CELL_TYPE, {
          e2xgraderCellType: SingleChoice.E2X_SINGLECHOICE_CELL_TYPE,
          taskName: taskName,
          points: points
        }),
        source: this._trans.__(
          '## Singlechoice Question\n' +
            '\n' +
            '- Choice 1\n' +
            '- Choice 2\n' +
            '- Choice 3\n' +
            '\n' +
            '<!-- Hint: Add the choices as list items, then run the cell and select the correct answer. -->'
        )
      }
    ];
  }
}

export namespace SingleChoice {
  export const E2X_SINGLECHOICE_CELL_TYPE = 'singlechoice';
  export const E2X_SINGLECHOICE_FORM_CLASS = 'e2x-singlechoice-form';
  export const cleanMetadata = {
    choice: '' as string,
    type: E2X_SINGLECHOICE_CELL_TYPE
  } as Record<string, any>;
}
