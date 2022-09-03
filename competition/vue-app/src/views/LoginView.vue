<template>
  <login-form @success="onLoginSuccess"/>
</template>

<script>
  import LoginForm from "../components/forms/LoginForm";
  export default {
    name: "LoginView",
    components: {LoginForm},
    data: () => ({
      previousRoute: null,
    }),
    methods: {
      async onLoginSuccess() {
        this.$emit('global-alert', {type:'success', msg: 'Successfully logged in', timeout:1500});
        /* Redirect to previous route */
        await this.$router.replace({path: this.previousRoute ? this.previousRoute.fullPath : '/'});
      },
    },
    beforeRouteEnter(to, from, next) {
      /* Set the previous route */
      next(vm => {
        vm.previousRoute = from;
      })
    },
  }
</script>

<style scoped>

</style>