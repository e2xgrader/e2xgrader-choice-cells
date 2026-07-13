import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';

import { E2xGraderCellRegistry } from '@e2xgrader/core';
import {MultipleChoice, SingleChoice} from "./plugin";

/**
 * Initialization data for the @e2xgrader/choice-cells extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@e2xgrader/choice-cells:plugin',
  description:
    'A JupyterLab extension that provides single and multiplechoice cells',
  autoStart: true,
  requires: [E2xGraderCellRegistry.IE2xGraderCellRegistry],
  optional: [ITranslator],
  activate: async (
    app: JupyterFrontEnd,
    cellRegistry: E2xGraderCellRegistry.IE2xGraderCellRegistry,
    translator: ITranslator
  ) => {
    console.log('JupyterLab extension @e2xgrader/choice-cells is activated!');

    const trans = (translator ?? nullTranslator).load('e2xgrader_choice_cells');

    // Register the choice cell plugins
    cellRegistry.registerPlugin(new SingleChoice(trans));
    cellRegistry.registerPlugin(new MultipleChoice(trans));
  }
};

export default plugin;
