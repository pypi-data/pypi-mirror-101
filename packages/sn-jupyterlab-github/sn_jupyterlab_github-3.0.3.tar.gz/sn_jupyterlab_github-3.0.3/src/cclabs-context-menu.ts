/**
 * Custom filebrowser context menu for CC Labs
 * This file can mostly be copied and pasted from:
 * https://github.com/jupyterlab/jupyterlab/blob/master/packages/filebrowser-extension/src/index.ts
 * (We're just adding our own 'Share Gist' option, and removing some others).
 * This is the best solution at least until https://github.com/jupyterlab/jupyterlab/issues/3994 is closed
 */

import { DocumentRegistry } from '@jupyterlab/docregistry';

import { JupyterFrontEnd } from '@jupyterlab/application';

import { Contents } from '@jupyterlab/services';

import { Menu } from '@lumino/widgets';

namespace CommandIDs {
  export const copy = 'filebrowser:copy';

  export const copyDownloadLink = 'filebrowser:copy-download-link';

  // For main browser only.
  export const createLauncher = 'filebrowser:create-main-launcher';

  export const cut = 'filebrowser:cut';

  export const del = 'filebrowser:delete';

  export const download = 'filebrowser:download';

  export const duplicate = 'filebrowser:duplicate';

  // For main browser only.
  export const hideBrowser = 'filebrowser:hide-main';

  export const navigate = 'filebrowser:navigate';

  export const open = 'filebrowser:open';

  export const openBrowserTab = 'filebrowser:open-browser-tab';

  export const paste = 'filebrowser:paste';

  export const rename = 'filebrowser:rename';

  // For main browser only.
  export const share = 'filebrowser:share-main';

  // For main browser only.
  export const copyPath = 'filebrowser:copy-path';

  export const showBrowser = 'filebrowser:activate';

  export const shutdown = 'filebrowser:shutdown';

  // For main browser only.
  export const toggleBrowser = 'filebrowser:toggle-main';
}

namespace CCLabsCommandIDs {
  export const shareGist = 'github:share-gist';
}

export function createContextMenu(
  model: Contents.IModel | undefined,
  app: JupyterFrontEnd,
  registry: DocumentRegistry
): Menu {
  const { commands } = app;
  const menu = new Menu({ commands });

  // If the user did not click on any file, we still want to show
  // paste as a possibility.
  if (!model) {
    menu.addItem({ command: CommandIDs.paste });
    return menu;
  }

  menu.addItem({ command: CommandIDs.open });

  const path = model.path;
  if (model.type !== 'directory') {
    const factories = registry.preferredWidgetFactories(path).map(f => f.name);
    const notebookFactory = registry.getWidgetFactory('notebook')!.name;
    if (
      model.type === 'notebook' &&
      factories.indexOf(notebookFactory) === -1
    ) {
      factories.unshift(notebookFactory);
    }
    if (path && factories.length > 1) {
      const command = 'docmanager:open';
      const openWith = new Menu({ commands });
      openWith.title.label = 'Open With';
      factories.forEach(factory => {
        openWith.addItem({ args: { factory, path }, command });
      });
      menu.addItem({ type: 'submenu', submenu: openWith });
    }
    // menu.addItem({ command: CommandIDs.openBrowserTab }); // probably causes issues on CC Labs
  }

  menu.addItem({ command: CommandIDs.rename });
  menu.addItem({ command: CommandIDs.del });
  menu.addItem({ command: CommandIDs.cut });

  if (model.type !== 'directory') {
    menu.addItem({ command: CommandIDs.copy });
  }

  menu.addItem({ command: CommandIDs.paste });

  if (model.type !== 'directory') {
    menu.addItem({ command: CommandIDs.duplicate });
    menu.addItem({ command: CommandIDs.download });
    menu.addItem({ command: CommandIDs.shutdown });
  }

  // menu.addItem({ command: CommandIDs.share }); // sharing doesn't work on CC Labs
  menu.addItem({ command: CommandIDs.copyPath });
  // menu.addItem({ command: CommandIDs.copyDownloadLink }); // also won't work on CC Labs

  // CC Labs Specific
  if (model.type !== 'directory') {
    menu.addItem({ args: { path }, command: CCLabsCommandIDs.shareGist });
  }

  return menu;
}
