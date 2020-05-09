import Vue from 'vue';
import Router from 'vue-router';
import Index from './components/Index.vue';
import Cart from './components/Cart.vue';
import Item from './components/Item.vue';
import Login from './components/Login.vue';
import Order from './components/Order.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart,
    },
    {
      path: '/item/:itemid',
      name: 'Item',
      component: Item,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/order',
      name: 'Order',
      component: Order,
    },
  ],
});
