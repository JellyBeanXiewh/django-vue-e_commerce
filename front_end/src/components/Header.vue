<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <div class="container">
        <b-navbar-brand>桃饱商城</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item v-for="site in sites" v-bind:key="site.name">
              <router-link v-bind:to="site.url" exact>{{site.name}}</router-link>
            </b-nav-item>
          </b-navbar-nav>
          <b-navbar-nav class="ml-auto">
            <div v-if="this.user.is_login">
              <b-nav-item-dropdown right v-bind:text="this.user.username">
                <b-dropdown-item @click="onLogout">注销</b-dropdown-item>
              </b-nav-item-dropdown>
            </div>
            <div v-else>
              <b-nav-item>
                <router-link to="/login" exact>登录 / 注册</router-link>
              </b-nav-item>
            </div>
          </b-navbar-nav>
        </b-collapse>
      </div>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      sites: [
        {
          name: '主页',
          url: '/',
        },
        {
          name: '购物车',
          url: '/cart',
        },
        {
          name: '订单',
          url: '/order',
        },
      ],
    };
  },
  props: ['user'],
  methods: {
    onLogout() {
      this.$emit('update:user', { username: '', is_login: false });
      this.$router.push({ name: 'Index' });
    },
  },
};
</script>

<style scoped>
  a {
    color: white;
    text-decoration: none;
    padding: 10px 15px;
    border-radius: 8px;
  }
</style>
