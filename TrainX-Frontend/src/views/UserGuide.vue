<template>
  <v-container>
    <v-layout justify-center>
      <v-flex md10>
        <div class="white-background shadow content">
          <h1>TrainX User Guide</h1>

          <h2>TrainX</h2>
          <p>
            TrainX enables the user to take part in an active learning cycle.
          </p>
          <p>
            The user creates a new session to sample a dataset or chooses an already existing one to continue working on it.
            After uploading a chosen dataset a first sampling takes place using a random sampling algorithm.
            Through exchangeable sampling strategies promising samples are selected for feedback.
            The user gives feedback by annotating more tokens or editing existing annotations.
            When satisfied the user can upload this feedback. An upsampling takes place where the given annotations are applied to the whole Dataset. This means annotated tokens will be annotated in the whole dataset and not only in the sentence where they where annotated.
            Now the user can prompt a training where a model is trained with the given annotations.            
          </p>

          <p>
            This active learning cycle can be repeated multiple times until the trained model is satisfying. The user can then donwload the model and all the previously trained models for this session.
          </p>

          <h2>Open the landingpage</h2>
          <p>The landingpage is your command central within TrainX. From here you can access all functionalities of TrainX.</p>
          <ul>
            <li>Click on the TrainX logo in the toolbar at the top of the page.</li>
          </ul>

          <h2>Create a session</h2>
          <p>All your progress, made annotations and your dataset are stored within your training session. To start a new training session you need to create a new session first.</p>
          <ul>
            <li>Open the landing page and click on <i>NEW SESSION</i></li>
            <li>Enter a title and a description for your training session. The description is optional but can help you to better identify a specific session later.</li>
            <li>To cancel the session creation simply click out of the input form.</li>
            <li>If you are satisfied with your session title and description click <i>CREATE SESSION</i></li>
          </ul>

          <h2>Load an old session</h2>
          <p>To continue your work on a training session.</p>
          <ul>
            <li>Open the landing page and click on <i>OLD SESSION</i></li>
            <li>Select the session you want to continue working on by clicking on it.</li>
          </ul>

          <h2>Get Status</h2>
          <p>To get the current status of the backend.</p>
          <ul>
            <li>Open the landing page and click on <i>GET STATUS</i></li>
          </ul>
          <p>The answer can be one of the following options:</p>
          <ul>
            <li><i>NOT CREATED</i> - The Session has no dataset</li>
            <li><i>CREATED</i> - The Session got a new job</li>
            <li><i>ANNOTATED</i> - Uploaded feedback was added to the dataset through upsampling</li>
            <li><i>ERROR</i> - An error occured</li>
            <li><i>QUEUED</i> - A job was queued</li>
            <li><i>RUNNING</i> - A job is beeing processed</li>
            <li><i>FINISHED</i> - A trainign was finished</li>
          </ul>


          <h2>Upload a dataset</h2>
          <p>Upload a dataset to your training session to start annotating samples.</p>
          <ul>
            <li>Open the landing page and click on <i>UPLOAD DATASET</i></li>
            <li>Click on </li>
            <li>Select your dataset in the opening dialogue. It should be a JSON filetype.</li>
            <li>Click on the upload button next to the <i>SELECT FILE</i>-input.</li>
            <li>This might take a while, depending on the size of your selected dataset.</li>
          </ul>

          <h2>Get samples</h2>
          <p>You want a subset of your dataset to manually annotate it.</p>
          <ul>
            <li>Open the landing page and click on <i>GET SAMPLES</i>.</li>
            <li>You will be guided to a display of samples where you can annotate them.</li>
          </ul>

          <h2>Annotate</h2>
          <p>To annotate samples</p>
          <ul>
            <li>Open the landing page and click on <i>GET SAMPLES</i></li>
            <li>You are presented with a sample from your datset.</li>
            <li>Already existing annotations are highlighted in the text.</li>
            <li>To annotate tokens mark them with your cursor.</li>
            <li>The annotations are auto-completed until the next whitespace or punctuation marks, so you don't need to mark the complete token. If you don't want that behaviour press the _alt_-key on windows or the _option_-key on mac while marking a token.</li>
            <li>To remove an annotation click on it.</li>
            <li>To merge two annotations and the tokens between them, if there are any, mark over the both existing annotations, like you whould in a real life text.</li>
            <li>When you are done with a sample, click on the checkmark in the right corner of the sample card. The Sample will be closed.</li>
            <li>To reopen samples click on the circle arrow in the right corner of the toolbar.</li>
            <li>To remove all annotations at once from an sample click on the cross in the right corner of the sample card.</li>
            <li>The Samples you get are paginated, for example the first ten samples selected from your dataset. To get the next ten click on the arrows on top or at the bottom of the screen. This brings you the next set of samples.</li>
          </ul>

          <h2>Color Coding</h2>
          <p>The sources of the annotated tokens are color coded</p>
          <table>
            <tr>
              <th>Source</th>
              <th>Color</th>
              <th>Meaning</th>
            </tr>
            <tr>
              <td>Gold</td>
              <td><div class="rectangle highlight-GOLD"></div></td>
              <td>Annotated by hand</td>
            </tr>
            <tr>
              <td>User</td>
              <td><div class="rectangle highlight-USER"></div></td>
              <td>Annotations added by the user</td>
            </tr>
            <tr>
              <td>Silver</td>
              <td><div class="rectangle highlight-SILVER"></div></td>
              <td>Automatic generated annotations, e.g. through upsampling</td>
            </tr>
            <tr>
              <td>Predicted</td>
              <td><div class="rectangle highlight-PRED"></div></td>
              <td>Annotated through a machine learning model</td>
            </tr>
          </table>

          <h2>Upload samples</h2>
          <p>To upload samples you annotated</p>
          <ul>
            <li>Open the landing page and click on <i>UPLOAD SAMPLES</i>.</li>
            <li>You can continue by requesting new samples via <i>GET SAMPLES</i>.</li>
          </ul>

          <h2>Start training</h2>
          <p>After you uploaded your annotated samples you can request more samples or start a training by</p>
          <ul>
            <li>Open the landing page and click on <i>START TRAINING</i>.</li>
          </ul>

          <h2>Supported browsers</h2>
          <p>Supported browsers are</p>
          <ul>
            <li>Firefox</li>
            <li>Chrome</li>
          </ul>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'UserGuide'
}
</script>

<style scoped lang="scss">
@import 'sass-material-design-colors/palette.scss';

h2 {
  margin: 1rem 0 ;
  border-bottom: 1px solid grey;
}

table {
  border-collapse: collapse;
}

th, td {
  padding: 15px;
  text-align: left;
}

table, th, td {
  border: 1px solid black;
}

.rectangle {
  width: 100px;
  height: 18px;
}

.white-background {
  background-color: #FFFFFF;
}

.shadow {
  box-shadow: 0 3px 5px -1px rgba(0,0,0,.2),0 5px 8px 0 rgba(0,0,0,.14),0 1px 14px 0 rgba(0,0,0,.12)
}

.content {
  padding: 20px;
}

.highlight-GOLD {
  background-color: #FDFB49;
}

.highlight-USER {
  background-color: #6FCD35;
}

.highlight-SILVER {
  background-color: #C0C0C0;
}

.highlight-PRED {
  background-color:#74BFF8;
}
</style>
