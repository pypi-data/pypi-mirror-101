import { ServerConnection } from '@jupyterlab/services';

import { URLExt } from '@jupyterlab/coreutils';

// file browser disabled
// export function showGitHubFilebrowser() {
// document.getElementById('github-filebrowser')!.style.display = 'flex';
// }

// export function hideGitHubSignInButton() {
// document.getElementById('github-filebrowser-signin')!.style.display = 'none';
// }

function createGitHubSignInButton(context: any) {
  getGitHubOauthLink().then(link => void 0);

  const setting = ServerConnection.makeSettings();
  const url = URLExt.join(setting.baseUrl, '/github/client-id');
  ServerConnection.makeRequest(url, { method: 'GET' }, setting).then(
    (response: any) => {
      response.json().then((data: any) => {
        context._browser.node.style.display = 'none';

        const signinwrapper = document.createElement('div');
        signinwrapper.id = 'github-filebrowser-signin';
        signinwrapper.className = 'signin-button-wrapper';

        const signinbutton = document.createElement('a');
        signinbutton.className = 'btn btn-lg btn-block btn-social btn-github';

        // make server request here to get details of button click
        signinbutton.addEventListener('click', () => {
          const popup_height = 750;
          const popup_width = 600;
          const popup_x_position = (screen.width + popup_width) / 2;
          const popup_y_position = (screen.height + popup_height) / 2;
          const url = encodeURI(
            `https://github.com/login/oauth/authorize?client_id=${data.client_id}&scope=gist read:user`
          );
          const popup = window.open(
            url,
            '_blank',
            `toolbar=no,scrollbars=yes,resizable=yes,top=${popup_y_position},left=${popup_x_position},width=${popup_width},height=${popup_height}`
          )!;
          (function (popup) {
            window.addEventListener(
              'message',
              event => {
                // file browser is disabled
                // hideGitHubSignInButton();
                // showGitHubFilebrowser();
                // popup.close();
                // // show user their github account
                // context.userName.name = event.data;
              },
              false
            );
          })(popup);
        });
        signinwrapper.appendChild(signinbutton);

        const signinbuttonicon = document.createElement('span');
        signinbuttonicon.className = 'fa fa-github';
        signinbutton.appendChild(signinbuttonicon);
        const signinbuttontext = document.createElement('span');
        signinbuttontext.innerHTML += 'Sign in with GitHub';
        signinbutton.appendChild(signinbuttontext);

        context._browser.node.insertAdjacentElement('afterend', signinwrapper);
      });
    }
  );
}

export function setupGitHubBrowserAuthentication(context: any) {
  // creates the signin button
  createGitHubSignInButton(context);
}

export function getGitHubOauthLink() {
  return new Promise<string>(resolve => {
    const setting = ServerConnection.makeSettings();
    const url = URLExt.join(setting.baseUrl, '/github/client-id');
    ServerConnection.makeRequest(url, { method: 'GET' }, setting).then(
      (response: any) => {
        response.json().then((data: any) => {
          const github_url = encodeURI(
            `https://github.com/login/oauth/authorize?client_id=${data.client_id}&scope=gist read:user`
          );
          resolve(github_url);
        });
      }
    );
  });
}
