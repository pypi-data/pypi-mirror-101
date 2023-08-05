import { IDisposable, DisposableDelegate } from '@lumino/disposable';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ToolbarButton } from '@jupyterlab/apputils';

import { DocumentRegistry } from '@jupyterlab/docregistry';

import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';

export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * Create a new extension object.
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const tokenParams = new URLSearchParams(window.location.search);
    const urlParams = new URLSearchParams(window.location.search);
    const domain_url = urlParams.get('d');
    const grading_url = 'https://' + domain_url + '/lti/results';
    const token = tokenParams.get('t');

    let callback = () => {
      if (
        confirm(
          'By clicking on "OK" I certify that I have successfully completed this lab exercise'
        )
      ) {
        try {
          let xhr = new XMLHttpRequest();
          xhr.open('PUT', grading_url, true);
          xhr.setRequestHeader('Authorization', 'Bearer ' + token);
          xhr.setRequestHeader('Content-Type', 'application/json');
          xhr.onload = function() {
            let response = JSON.parse(xhr.responseText);
            if (xhr.status == 200) {
              console.log(response);
              alert('Lab Completed');
            } else {
              alert('An error occured');
            }
          };
          xhr.send('{}');
        } catch (err) {
          console.log(err);
          alert('An error occured');
        }
      } else {
        console.log('Canceled');
      }
    };

    if (token && domain_url) {
      let button = new ToolbarButton({
        className: 'myButton',
        label: 'Mark this Lab as Complete',
        onClick: callback,
        tooltip: 'Mark this Lab as Complete'
      });

      panel.toolbar.insertItem(9, 'runAll', button);
      return new DisposableDelegate(() => {
        button.dispose();
      });
    }
  }
}

/**
 * Initialization data for the myextension extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-grading',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
  }
};

export default extension;
