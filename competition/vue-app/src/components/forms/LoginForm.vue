<template>
  <v-form ref="form">
    <slot :form="form" :alerts="alerts">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-card color="tertiary">
              <v-card-title class="text-h3 tertiary-text--text">
                <slot name="title">Login</slot>
              </v-card-title>
              <v-alert v-model="alerts.status" dense :type="alerts.type">
                  {{ alerts.msg }}
              </v-alert>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                    autofocus
                    required
                    v-model="form.username.value"
                    label="Username"
                    :rules="form.username.rules"
                    @keydown.enter="login($event)">
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                    required
                    type="password"
                    v-model="form.password.value"
                    label="Password"
                    :rules="form.password.rules"
                    @keydown.enter="login($event)">
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-btn color="primary" class="primary-text--text" @click="login($event)">
                  <slot name="btn">Login</slot>
                </v-btn>
              </v-container>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </slot>
  </v-form>
</template>

<script>
  export default {
    name: "LoginForm",
    events: ['success'],
    data: () => ({
      form: {
        username: {
          value: '',
          rules: [],
        },
        password: {
          value: '',
          rules: [],
        },
      },
      alerts: {
        status: false,
        type: null,
        msg: null
      }
    }),
    methods: {
      alert(type, msg, timeout) {
        this.alerts.status = !!type && !!msg;
        this.alerts.type = type;
        this.alerts.msg = msg;

        if (timeout && !isNaN(timeout)) {
          setTimeout(() => {
            this.alert(null);
          }, timeout);
        }
      },
      async login(event) {
        if (event) event.preventDefault();

        /* Log the user in */
        try {
          /* Clear any possible previous errors */
          this.alert(null);
          /* Attempt login */
          await this.$store.dispatch('login', {username: this.form.username.value, password: this.form.password.value});
          /* Login successful */
          this.$emit('success');
        } catch (e) {
          /* Login failed */
          this.alert('error', 'Login failed, please try again');
          /* Clear password credentials */
          this.form.password.value = '';
        }
      }
    },
    mounted() {
      /* Check if redirected from a 403 */
      if (this.$route.query.status === 403)
        this.alert('error', 'Permission denied');
      else if (this.$route.query.status === 401)
        this.alert('warning', 'Please log in', 1500);
    }
  }
</script>

<style scoped>

</style>