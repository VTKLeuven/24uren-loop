<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card color="tertiary">
          <v-card-title class="text-h4 tertiary-text--text">Queue Up</v-card-title>
          <v-card-subtitle class="text-subtitle-1 tertiary-text--text">Please scan your student card, or enter your unique identification in order to sign up for a lap.</v-card-subtitle>
          <v-alert dense type="success" v-model="alerts.success">
            You were successfully added to the queue.
          </v-alert>
          <v-alert dense type="warning" v-model="alerts.multiple">
            Oops! It seems there are multiple people with this identification.
          </v-alert>
          <v-alert dense type="error" v-model="alerts.error">
            Uh-oh. Something went seriously wrong. Please ask for IT support.
          </v-alert>
          <v-form ref="form" v-model="validRunner">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                  autofocus
                  required
                  v-model="form.identification.value"
                  label="Identification"
                  @input="change($event)"
                  @keydown.enter="submit($event)"
                  :rules="form.identification.rules">
                  </v-text-field>
                </v-col>
              </v-row>
              <template v-if="inputNewRunner">
                <v-row>
                  <v-col cols="12">
                    <v-text-field required v-model="form.firstName.value" label="First Name" placeholder="Jan" :rules="form.rules.name" />
                  </v-col>
                  <v-col cols="12">
                    <v-text-field required v-model="form.lastName.value" label="Last Name" placeholder="Janssens" :rules="form.rules.name" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-select v-if="universityChoices && universityChoices !== 'error'" required v-model="form.university.value"
                              :items="universityChoices" item-value="value" item-text="text" :rules="form.university.rules"
                              label="University" prepend-icon="school" />
                    <v-select v-else-if="universityChoices && universityChoices === 'error'" required label="An error occurred"
                              prepend-icon="group" error />
                    <v-select v-else label="Loading..." prepend-icon="group" disabled required />
                  </v-col>
                  <v-col cols="12">
                    <v-select v-if="groupChoices && groupChoices !== 'error'"
                              v-model="form.group.value" :items="groupChoices" label="Group" item-value="value"
                              item-text="text" prepend-icon="group" />
                    <v-select v-else-if="groupChoices && groupChoices === 'error'" label="An error occurred"
                              prepend-icon="group" error />
                    <v-select v-else label="Loading..." prepend-icon="group" disabled />
                  </v-col>
                </v-row>
                <v-btn color="primary" class="primary-text--text text-button" @click="create($event)" :disabled="!validRunner">Submit</v-btn>
              </template>
            </v-container>
          </v-form>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" v-if="showRunner">
        <v-card color="tertiary">
          <v-card-title class="text-h4 tertiary-text--text">Signed up information</v-card-title>
          <v-card-subtitle class="text-subtitle-1 tertiary-text--text">
            Name: {{ showRunner | fullName }}
          </v-card-subtitle>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-alert dense type="error" v-model="alerts.runnerQuickInfo.error.status">
                      {{ alerts.runnerQuickInfo.error.msg }}
                </v-alert>
                <runner-quick-info :runner="showRunner" @error="onRunnerQuickInfoError"/>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
  import RunnerQuickInfo from "../components/info/RunnerQuickInfo";
  export default {
    name: "QueueUpView",
    components: {RunnerQuickInfo},
    data: () => ({
      alerts: { /* Alert indicators */
        multiple: false,
        success: false,
        error: false,
        runnerQuickInfo: {
          error: {
            status: false,
            msg: ''
          }
        }
      },
      showRunner: null,

      validRunner: false, /* Checks if the entire form for creating a new runner is valid */
      inputNewRunner: false, /* Shows the 'new runner' form if true */

      existingRunner: null, /* The id of the runner if one is found (for later submissions) */

      form: { /* Form fields */
        identification: {
          value: '',
          rules: [identification => /^[rR]*[0-9]{7}$/.test(identification) || 'Your identification is your unique identifier, containing an "r" and 7 numbers'],
        },
        university: {
          value: null,
          rules: [university => !!university || 'You need to choose a university.'],
        },
        firstName: {
          value: '',
        },
        lastName: {
          value: ''
        },
        group: {
          value: null
        },

        rules: { /* General rules not bound to a specific field */
          name: [
            name => !!name || 'You cannot leave your name empty.',
            name => !!name && name.length >= 2 || 'Your name is too short.',
            name => !!name && name.length <= 30 || 'Your name is too long.'
          ],
        }
      },
    }),
    methods: {
      submit: function(event) {
        /* Prevent default actions */
        if (event) event.preventDefault();

        /* If an existing runner has been found previously (through the change function) */
        if (this.existingRunner) {
          /* Remove quick information */
          this.alerts.runnerQuickInfo.error.status = false;

          /* Post this data to the server */
          this.axios.post(`${this.$store.state.urls.queue_ticket}/`, {
            runner: this.existingRunner.id
          }).then(() => {
            /* Hide other alerts */
            this.disableAlerts();
            /* Show success alert */
            this.alerts.success = true;
            this.showRunner = this.existingRunner;
            /* Reset the form */
            this.resetForm();
          }).catch((err) => {
            console.log(err);
            /* Hide other alerts */
            this.disableAlerts();
            /* Show error alert */
            this.alerts.error = true;
            /* Remove quick information */
            this.showRunner = null;
            /* Reset the form */
            this.resetForm();
          });
        }
      },
      change: function(event) {
        /* If the enter key was pressed, do nothing */
        if (event && event.key && event.key === 'Enter') {
          event.preventDefault();
          return;
        }

        /* Reset the existing runner */
        this.existingRunner = null;
        /* Hide the 'new runner' form */
        this.inputNewRunner = false;
        /* Check if the identification has a wrong format */
        if (!this.form.identification.value || !this.$refs.form.inputs[0].validate()) return;

        /* Add 'r' if necessary */
        let identification = this.form.identification.value.toLowerCase();
        if (identification.charAt(0) !== 'r') identification = 'r' + identification;

        /* Retrieve the runner corresponding to that identification */
        this.axios.get(`${this.$store.state.urls.runner}/`, {
          params: {
            'identification': identification
          }
        }).then((response) => {
          /* Check if only a single runner is returned (which should be the case) */
          if(response.data.length === 1){
            /* Set the id of this runner to the existing runner */
            this.existingRunner = response.data[0];
          } else if(response.data.length > 1){
            /* Hide all alerts */
            this.disableAlerts();
            /* Show the multiple alert */
            this.alerts.multiple = true;
          } else {
            /* Hide all alerts */
            this.disableAlerts();
            /* Show the 'new runner' form */
            this.inputNewRunner = true;
          }
        }).catch((err) => {
          console.log('Error while retrieving runner: ', err);
          /* Hide all alerts */
          this.disableAlerts();
          /* Show an error alert to the user */
          this.alerts.error = true;
        })
      },
      create: function(event) {
        /* Called when a new runner is created */
        /* Prevent the default action */
        if (event) event.preventDefault();

        /* Add 'r' if necessary */
        let identification = this.form.identification.value.toLowerCase();
        if (identification.charAt(0) !== 'r') identification = 'r' + identification;

        /* Create the new runner in object form */
        let runnerObject = {
          'first_name': this.form.firstName.value,
          'last_name': this.form.lastName.value,
          'university': this.form.university.value,
          'identification': identification
        };
        /* If a group is selected, add it to the object */
        if (this.group) {
          runnerObject.group = this.form.group.value
        }

        /* Post the new runner to the server */
        this.axios.post(`${this.$store.state.urls.runner}/`, runnerObject).then((response) => {
          /* Set the existing runner id */
          this.existingRunner = response.data;
          /* Submit the runner to the queue */
          this.submit();
        }).catch((err) => {
          /* Log the error */
          console.log('Error while creating runner: ', err);
          /* Disable previous alerts and reset the form */
          this.disableAlerts();
          this.resetForm();
          /* Activate the error alert */
          this.alerts.error = true;
        })
      },
      disableAlerts: function() {
        this.alerts.success = false;
        this.alerts.multiple = false;
        this.alerts.error = false;
      },
      resetForm: function() {
        this.inputNewRunner = false;
        this.$refs.form.resetValidation();
        this.$refs.form.reset();
      },
      onRunnerQuickInfoError(msg) {
        this.alerts.runnerQuickInfo.error.status = true;
        this.alerts.runnerQuickInfo.error.msg = msg
      }
    },
    asyncComputed: {
      groupChoices: {
        async get() {
          try {
             let resp = await this.axios.get(`${this.$store.state.urls.group}/`);
             return resp.data.map((group) => ({text: group.name, value: group.id}));
          } catch (e) {
            console.log('Error while retrieving groups');
            return 'error';
          }
        },
        default() {
          return null;
        }
      },
      universityChoices: {
        async get() {
          try {
             let resp = await this.axios.get(`${this.$store.state.urls.university}/`);
             return resp.data.map((uni) => ({text: uni.full_name, value: uni.id}));
          } catch (e) {
            console.log('Error while retrieving universities');
            return 'error';
          }
        },
        default() {
          return null;
        }
      }
    },
  }
</script>

<style scoped>
.v-card__text, .v-card__title {
  word-break: normal; /* maybe !important  */
}
</style>