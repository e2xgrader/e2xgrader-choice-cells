import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the @e2xgrader/choice-cells extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@e2xgrader/choice-cells:plugin',
  description: 'A JupyterLab extension that provides single and multiplechoice cells',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension @e2xgrader/choice-cells is activated!');
  }
};

export default plugin;
