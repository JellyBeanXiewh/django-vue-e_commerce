<template>
  <div id="app">
    <Header :user.sync="user"/>
    <br/>
    <router-view :user.sync="user"/>
  </div>
</template>

<style>
#app {
  margin-top: 0
}
</style>

<script>
import Header from './components/Header.vue';

export default {
  name: 'App',
  data() {
    return {
      user: {
        username: '',
        is_login: false,
      },
    };
  },
  components: {
    Header,
  },
};
</script>
