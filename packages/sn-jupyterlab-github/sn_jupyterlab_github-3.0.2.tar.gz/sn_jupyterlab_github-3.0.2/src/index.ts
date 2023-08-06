// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IDocumentManager } from '@jupyterlab/docmanager';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import '../style/index.css';

/**
 * Begin CC Labs Specific Code
 */
import '../style/cclabs.css';
import { addShareGistCommand } from './cclabs-gist-sharing';

/**
 * End CC Labs Specific Code
 */

/**
 * The ID for the plugin.
 */
const PLUGIN_ID = 'sn-jupyterlab-github:drive';

/**
 * The JupyterLab plugin for the GitHub Filebrowser.
 */
const fileBrowserPlugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  requires: [
    IDocumentManager,
    IFileBrowserFactory,
    ILayoutRestorer,
    ISettingRegistry
  ],
  activate: activateFileBrowser,
  autoStart: true
};

/**
 * Activate the file browser.
 */
function activateFileBrowser(
  app: JupyterFrontEnd,
  manager: IDocumentManager,
  factory: IFileBrowserFactory,
  restorer: ILayoutRestorer,
  settingRegistry: ISettingRegistry
): void {
  // Fetch the initial state of the settings.
  Promise.all([settingRegistry.load(PLUGIN_ID), app.restored])
    .then(([settings]) => {
      // Don't warn about access token on initial page load, but do for every setting thereafter.
    })
    .catch((reason: Error) => {
      console.error(reason.message);
    });

  /**
   * Begin CC Labs Specific Code
   */
  const { registry } = manager;
  const { tracker } = factory;
  addShareGistCommand(
    factory.defaultBrowser,
    app,
    app.commands,
    registry,
    tracker
  );
  /**
   * End CC Labs Specific Code
   */

  return;
}

export default fileBrowserPlugin;

/**
 * A namespace for module-private functions.
 */
