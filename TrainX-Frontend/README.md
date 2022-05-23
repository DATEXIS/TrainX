# TraiNER

> A Graphical Training Interface for Named Entity Recognition

## Browser Support

| ![Firefox](https://raw.github.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png) | ![Chrome](https://raw.github.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png) |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Latest ✔                                                                                    | Latest ✔                                                                                 |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need a current version of _npm_, 6.5.0 was used during development.

### Installing

After cloning the repository, install dependencies. You can then run a development server or build the project.

```bash
# install dependencies
npm install

# serve with hot reload at localhost:4200
npm run dev

# build for production with minification
npm run build
```

### Run tests

To run unit tests:

```bash
npm run test:unit
```

## TraiNER User Guide

### Create a session

All your progress, made annotations and your dataset is stored within your training session. So to start a new trianing session you need to create a new session.

- Open the landing page and click on _new session_
- Enter a title and a description for your training session. Both values are optional but recommended to identify your session later.
- To abbort this process just click outside of the input form, to close it.
- If you are satisfied with your session click on _create session_

### Load an old session

To continue your work on a training session you need to load the session.

- Open the landing page and click on _old session_
- Select a Session to continue working on it by clicking on it

### Open the landingpage

The landingpage is your command central withing TraiNER. From here you can access all functionalities of TraiNER.

- Click on _TraiNER_ in the toolbar, at the top of the screen.

### Upload a dataset

Upload your dataset to start annotating samples of it

- Open the landing page and click on _upload dataset_
- Click on _select file_
- Select your dataset in the opening dialogue. It should be a JSON filetype.
- Click on the upload button next to the _select file_-input.
- This might take a while, depending on the size of your selected dataset.

### Get samples

You want a subset of your dataset to manually annotate it.

- Open the landing page and click on _get samples_
- You will be guided to a display of samples where you can annotate them

### Upload samples

To upload samples you annotated

- Open the landing page and click on _upload samples_
- You can continue by requesting new samples via _get samples_

### Start training

After you uploaded your annotated samples you can request more samples or start a training by

- Open the landing page and click on _start training_

### Get metric

To see metrics for your training session

- Open the landing page and click on _get metric_

### Annotate

To annotate samples

- Open the landing page and click on _get samples_
- You are presented with a sample from your datset.
- Already existing annotations are highlighted in the text.
- To annotate tokens mark them with your cursor.
- The annotations are auto-completed until the next whitespace or punctuation marks, so you don't need to mark the complete token. If you don't want that behaviour press the _alt_-key on windows or the _option_-key on mac while marking a token.
- To remove an annotation click on it.
- To merge two annotations and the tokens between them, if there are any, mark over the both existing annotations, like you whould in a real life text.
- When you are done with a sample, click on the checkmark in the right corner of the sample card. The Sample will be closed.
- To reopen samples click on the circle arrow in the right corner of the toolbar.
- To remove all annotations at once from an sample click on the cross in the right corner of the sample card.
- A counter runs in the top right corner, in the toolbar, displaying the time you used to annotate this set of samples. This is used to calculate the total annotation time for your metrics.
- The Samples you get are paginated, for example the first ten samples selected from your dataset. To get the next ten click on the arrows on top or at the bottom of the screen. This brings you the next set of samples.

## Built With

-   [Vue.js](https://vuejs.org/) - Frontend framework
-   [Vuetify](https://vuetifyjs.com/) - Material Design component framework
-   [Webpack](https://webpack.js.org/) - Module bundler and build tool
-   [Axios](https://github.com/axios/axios) - Promise based HTTP requests

## Releases

A new release of this software is defined by a new [SemVer](http://semver.org/) version number, which is set as Git tag. This triggers an automated creation of a new Docker image in the Datexis repository, which also has the version number as tag. Example:

- git tag v6.1.3
- git push --tags

## Authors

-   **Tobias Klatt** - _Initial work_ - [GitHub](https://github.com/T0biWan/)

See also the list of [contributors](https://github.com/T0biWan/bachelor-frontend-prototype/graphs/contributors) who participated in this project.
