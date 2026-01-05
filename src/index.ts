import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

//import { IE2xCellPluginRegistry } from '@e2xgrader/cell-registry';
import { E2xGraderCellRegistry } from '@e2xgrader/core';
import { choiceCellPlugins } from './plugin';

/**
 * Initialization data for the @e2xgrader/choice-cells extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@e2xgrader/choice-cells:plugin',
  description:
    'A JupyterLab extension that provides single and multiplechoice cells',
  autoStart: true,
  requires: [E2xGraderCellRegistry.IE2xGraderCellRegistry],
  activate: async (
    app: JupyterFrontEnd,
    cellRegistry: E2xGraderCellRegistry.IE2xGraderCellRegistry
  ) => {
    console.log('JupyterLab extension @e2xgrader/choice-cells is activated!');
    // Register the choice cell plugins
    choiceCellPlugins.forEach(plugin => {
      cellRegistry.registerPlugin(plugin);
    });
  }
};

export default plugin;
