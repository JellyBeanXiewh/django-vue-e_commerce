<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h2>商品浏览</h2>
        <hr><br>
        <alert :message=message :status=msgStatus v-if="showMessage"></alert>
        <b-dropdown dropright text="商品类别" variant="outline-primary">
<!--          <b-dropdown-item onclick="">An item</b-dropdown-item>-->
<!--          <b-dropdown-item onclick="">Another item</b-dropdown-item>-->
          <b-dropdown-item @click="getItems()">全部</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item
            v-for="type in itemTypes"
            :key="type.id"
            @click="getItemFromType(type.id)"
          >
            {{ type.name }}
          </b-dropdown-item>
        </b-dropdown>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 40%">商品名称</th>
              <th scope="col" style="width: 35%">单价</th>
              <th scope="col" style="width: 25%">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td>
                <router-link v-bind:to="{ name: 'Item', params: { itemid: item.id }}">
                  {{ item.name }}
                </router-link>
              </td>
              <td>{{ item.price }}</td>
              <td>
                <div class="btn-group">
                  <button
                    type="button"
                    class="btn btn-success btn-sm"
                    @click="addToCart(item.id)"
                  >
                    加入购物车</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Index',
  data() {
    return {
      items: [],
      itemTypes: [],
      message: '',
      msgStatus: 'success',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  props: ['user'],
  methods: {
    getItems() {
      const path = 'http://localhost:8000/item/';
      axios.get(path)
        .then((res) => {
          this.items = res.data.items;
        })
        .catch((error) => {
          this.msgStatus = 'danger';
          this.message = error;
          this.showMessage = true;
          // eslint-disable-next-line
          console.error(error);
          setTimeout(() => {
            this.showMessage = false;
          }, 5000);
        });
    },
    getItemTypes() {
      const path = 'http://localhost:8000/item_type/';
      axios.get(path)
        .then((res) => {
          this.itemTypes = res.data.type;
        })
        .catch((error) => {
          this.msgStatus = 'danger';
          this.message = error;
          this.showMessage = true;
          // eslint-disable-next-line
          console.error(error);
          setTimeout(() => {
            this.showMessage = false;
          }, 5000);
        });
    },
    getItemFromType(typeID) {
      const path = `http://localhost:8000/item_type/${typeID}/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data.items;
        })
        .catch((error) => {
          this.msgStatus = 'danger';
          this.message = error;
          this.showMessage = true;
          // eslint-disable-next-line
          console.error(error);
          setTimeout(() => {
            this.showMessage = false;
          }, 5000);
        });
    },
    addToCart(itemID) {
      if (this.user.is_login) {
        const path = 'http://localhost:8000/cart/';
        const payload = {
          user: this.user.username,
          item_id: itemID,
          amount: 1,
        };
        axios.post(path, payload)
          .then((res) => {
            this.msgStatus = res.data.status;
            this.message = res.data.message;
            this.showMessage = true;
            setTimeout(() => {
              this.showMessage = false;
            }, 5000);
          })
          .catch((error) => {
            this.msgStatus = 'danger';
            this.message = error;
            this.showMessage = true;
            // eslint-disable-next-line no-console
            console.error(error);
            setTimeout(() => {
              this.showMessage = false;
            }, 5000);
          });
      } else {
        this.$router.push({ name: 'Login' });
      }
    },
  },
  created() {
    this.getItems();
    this.getItemTypes();
  },
};
</script>
