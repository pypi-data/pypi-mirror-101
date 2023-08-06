import { ServerConnection } from '@jupyterlab/services';

import { URLExt } from '@jupyterlab/coreutils';

// import { createContextMenu } from './cclabs-context-menu';

import {
  getGitHubOauthLink
  // hideGitHubSignInButton,
  // showGitHubFilebrowser
} from './cclabs-authentication';

import { Dialog, showDialog } from '@jupyterlab/apputils';

import { Widget } from '@lumino/widgets';

function createGist(path: string) {
  return new Promise((resolve, reject) => {
    const setting = ServerConnection.makeSettings();
    const url = URLExt.join(setting.baseUrl, '/github/share-gist');
    ServerConnection.makeRequest(
      url,
      { method: 'POST', body: JSON.stringify({ path }) },
      setting
    ).then((response: any) => {
      response
        .json()
        .then((gist: any) => {
          if (gist.html_url) {
            resolve(gist.html_url);
          } else {
            reject(gist.error);
          }
        })
        .catch((err: any) => {
          console.log(err);
        });
    });
  });
}

export function addShareGistCommand(
  browser: any,
  app: any,
  commands: any,
  registry: any,
  tracker: any
) {
  commands.addCommand('github:share-gist', {
    execute: () => {
      const widget = tracker.currentWidget;
      const model = widget?.selectedItems().next();
      if (!model) {
        return;
      }
      const path = encodeURI(model.path);
      createGist(path)
        .then((gist_url: any) => {
          showDialog({
            title: 'Your gist is now available on GitHub:',
            body: new Private.GistLink(gist_url),
            buttons: [Dialog.okButton({ label: 'Dismiss' })]
          });
        })
        .catch((gist_err: string) => {
          if (gist_err === 'unauthenticated') {
            getGitHubOauthLink().then(link => {
              showDialog({
                title: 'Sign in to Share your Gist',
                body: 'You need to sign in to GitHub to share Gists.',
                buttons: [
                  Dialog.cancelButton(),
                  Dialog.okButton({ label: 'Sign in' })
                ]
              }).then((result: any) => {
                if (result.button.accept) {
                  const popup_height = 750;
                  const popup_width = 600;
                  const popup_x_position = (screen.width + popup_width) / 2;
                  const popup_y_position = (screen.height + popup_height) / 2;
                  const popup = window.open(
                    link,
                    '_blank',
                    `toolbar=no,scrollbars=yes,resizable=yes,top=${popup_y_position},left=${popup_x_position},width=${popup_width},height=${popup_height}`
                  );
                  (function (popup) {
                    const eventListener = (event: any) => {
                      popup!.close();
                      window.removeEventListener('message', eventListener);
                      createGist(path).then((gist_url: any) => {
                        showDialog({
                          title: 'Your gist is now available on GitHub:',
                          body: new Private.GistLink(gist_url),
                          buttons: [Dialog.okButton({ label: 'Dismiss' })]
                        });
                      });
                    };
                    window.addEventListener('message', eventListener, false);
                  })(popup);
                }
              });
            });
            // need to get sign in uri here
          } else {
            showDialog({
              title: 'Gist creation unsuccessful',
              body: gist_err,
              buttons: [Dialog.okButton({ label: 'Dismiss' })]
            });
          }
        });
    },
    iconClass: 'jp-MaterialIcon jp-GitHub-logo',
    label: 'Share on GitHub'
  });

  // function clickIsInFilebrowser(event: any) {
  // return (
  // event.target.matches('#filebrowser > div > ul > li > span') ||
  // event.target.matches('#filebrowser > div > ul > li')
  // );
  // }

  app.contextMenu.addItem({
    command: 'github:share-gist',
    selector: '.jp-DirListing-item'
  });

  // document.addEventListener(
  // 'contextmenu',
  // (event: any) => {
  // if (clickIsInFilebrowser(event)) {
  // event.preventDefault();
  // event.stopPropagation();
  // event.stopImmediatePropagation();
  // const menu = createContextMenu(
  // browser.modelForClick(event),
  // commands,
  // registry
  // );
  // menu.open(event!.clientX!, event!.clientY!);
  // }
  // },
  // true
  // );
}
function createGistLinkNode(link: string) {
  const body = document.createElement('div');
  body.setAttribute(
    'style',
    'display: inline-flex; align-items: center;  flex-direction: row; padding-bottom: 15px;'
  );

  const copyButton = document.createElement('button');
  copyButton.className =
    'p-Widget jp-mod-styled jp-CopyIcon jp-ToolbarButtonComponent copyGistUrl';
  copyButton.title = 'Copy link to clipboard';
  copyButton.setAttribute('style', 'width: 30px; height: 30px;');

  const copyIcon = document.createElement('span');
  copyIcon.className = 'jp-CopyIcon jp-Icon jp-Icon-16';
  copyButton.appendChild(copyIcon);

  const linkText = document.createElement('span');
  linkText.setAttribute('style', 'padding-right: 10px;');
  linkText.innerHTML = link;

  copyButton.onclick = () => {
    // Select the email link anchor text
    const range = document.createRange();
    range.selectNode(linkText);
    window.getSelection().addRange(range);

    try {
      // Now that we've selected the anchor text, execute the copy command
      document.execCommand('copy');
    } catch (err) {
      console.log('Oops, unable to copy');
    }

    // Remove the selections - NOTE: Should use
    // removeRange(range) when it is supported
    window.getSelection().removeAllRanges();
  };

  body.appendChild(linkText);
  body.appendChild(copyButton);
  return body;
}

namespace Private {
  export class GistLink extends Widget {
    constructor(link: string) {
      super({ node: createGistLinkNode(link) });
    }
  }
}
