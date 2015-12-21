# CANDL web app in Node.js

The CANDL web app is built using Node.js and React & Redux (from Facebook). Links:
https://facebook.github.io/react/docs/getting-started.html,  http://redux.js.org/

## Understanding, Configuring, and Building

There are a few pre-configured npm scripts:

  - `npm run build` uses webpack to build `bundle.js` and places it under the
    `public` directory. This bundle contains both the js and css for the app.
  - `npm run start` starts in "production mode" (no hot reloading). This simply
    spins up the server under `server/app.js.`
  - `npm run dev` is where the magic happens. This introduces the webpack dev
    and hot middleware (the correct environment variables are set via `npm
    better run`), which rebuilds the bundle on css or js changes and injects it
    into the browser using magic. No reloading necessary! Great for development.
  - `npm install` installs all modules listed in package.json.


Thus, to run in production:

```sh
npm install
npm run build
npm run start
```

To run in dev mode:

```sh
npm install
npm run dev
```

To handle the discrepancies between running the client code in "dev mode" or
"production mode", there are two helpers provided - `containers/Root.js` and
`store/configureStore.js`. These modules conditionally load the `.dev` or
`.prod` extension of their respective file depending on the environment
variables when webpack is running. The only difference in the respective
versions are loading the necessary tooling for the dev/debugging redux
awesomeness. In dev mode, the `DevTools` react component loads and renders which
provides a visual history of all the actions and allows you to go forwards and
backwards in time. It also logs all the state changes.

## APP OVERVIEW

All client side code originates in the client directory, all server code in the server directory. The CANDL code itself has been copied in its most recent form to the CANDL folder.

The main layout of the app is described in client/containers/App.js. See also client/actions/actions.js for action definitions and client/reducers/index.js for reducers. Posting to the server endpoint is handled in client/requester.js and the server-side uploading of files and running of python script is done in server/routes.js.

A user may click the "submit" button only once three files have been uploaded, and text entered in the email field. If everything checks out on the server-side (see below section for file-checking specifics) then the script "run_CANDL_outer.py" is called. Additional file checking may be taken care of here. If an error is found, that script may call sys.exit(1) to alert the client something has gone wrong. It will otherwise fork and call "run_CANDL_inner.py" then exit 0 so that the client may display a "everything is fine, CANDL is running" message to the user.

The inner script runs CANDL. Currently, output is saved in the proper directory.


## PLACES TO MAKE CHANGES

There are several places where the app may be tweaked for additional functionality.

  - File client/actions/actions.js beginning line 25. Here is where files may be checked on the client-side for proper formatting. Currently, we check that both graph files end with ".ppi". Further checking could be done on the email string, graph files or landmarks file.

  - File run_CANDL_outer.py beginning line 23. Here further format checking may be done in python. If this script calls "sys.exit(1)" the client will be alerted, and the user will be shown a "script not running," message. Currently no such checks are being done, but in-depth checking could assess the actual format of files or structure of the email string.

  - File run_CANDL_inner.py line 11. Here a "dunny" python script may be run in place of CANDL to test the infastructure of this web app. Comment out line 11 and uncomment line 12.

  - File run_CANDL_inner.py beginning line 34. Here is where the automatic email function may be added. Exact implementation of this will depend on the server on which the app is running. Sample code is provided using MIMEMultipart.
