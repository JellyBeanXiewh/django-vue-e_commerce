<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h2>购物车</h2>
        <hr><br><br>
        <alert :message=message :status=msgStatus v-if="showMessage"></alert>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 10%"></th>
              <th scope="col" style="width: 30%">商品名称</th>
              <th scope="col" style="width: 20%">单价</th>
              <th scope="col" style="width: 20%">数量</th>
              <th scope="col" style="width: 20%">操作</th>
            </tr>
          </thead>
          <tbody v-if="items.length !== 0">
            <tr v-for="(item, index) in items" :key="index">
              <td style="width: 10%">
                <b-form-checkbox v-model="item.selected"></b-form-checkbox>
              </td>
              <td>
                <router-link v-bind:to="{ name: 'Item', params: { itemid: item.id }}">
                  {{ item.name }}
                </router-link>
              </td>
              <td>{{ item.price }}</td>
              <td>
                <div class="spinbtn">
                  <b-form-spinbutton
                    inline
                    min=1
                    :max=item.inventory
                    v-model=item.amount
                    @change="updateItem(item)"
                  >
                  </b-form-spinbutton>
                </div>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="deleteItem(item)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td></td>
              <td></td>
              <td>
                <p class="text-center">购物车暂无商品</p>
              </td>
              <td></td>
              <td></td>
            </tr>
          </tbody>
        </table>
        <hr>
        <div>
          <p class="text-right">共计：<span class="money">{{ this.sumMoney }}</span> 元</p>
        </div>
        <hr>
        <div class="text-right">
          <button type="button" class="btn btn-outline-danger" @click="purchase">去结算</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      items: [],
      selected: [],
      message: '',
      msgStatus: 'success',
      showMessage: false,
    };
  },
  computed: {
    sumMoney() {
      let sum = 0;
      for (let i = 0; i < this.items.length; i += 1) {
        if (this.items[i].selected) {
          sum += this.items[i].price * this.items[i].amount;
        }
      }
      return sum;
    },
  },
  props: ['user'],
  components: {
    alert: Alert,
  },
  methods: {
    getCartItem() {
      const path = `http://localhost:8000/cart/?user=${this.user.username}`;
      axios.get(path)
        .then((res) => {
          this.items = res.data.items;
          // this.items.forEach((item) => {
          //   // eslint-disable-next-line no-param-reassign
          //   item.selected = false;
          // });
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
    },
    updateItem(item) {
      const path = 'http://localhost:8000/update_cart_item/';
      const payload = {
        user: this.user.username,
        item_id: item.id,
        amount: item.amount,
      };
      axios.post(path, payload)
        .then(() => {
          this.getCartItem();
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
          this.getCartItem();
        });
    },
    deleteItem(item) {
      const path = 'http://localhost:8000/delete_cart_item/';
      const payload = {
        user: this.user.username,
        item_id: item.id,
      };
      axios.post(path, payload)
        .then((res) => {
          this.msgStatus = res.data.status;
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 5000);
          this.getCartItem();
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
          this.getCartItem();
        });
    },
    purchase() {
      let item_list = [];
      for (let i = 0; i < this.items.length; i += 1) {
        if (this.items[i].selected) {
          item_list.push({
            id: this.items[i].id,
            amount: this.items[i].amount,
          });
        }
      }
      if (item_list.length === 0) {
        this.msgStatus = 'danger';
        this.message = '未选中商品';
        this.showMessage = true;
        setTimeout(() => {
          this.showMessage = false;
        }, 5000);
      } else {
        const details = {
          user: this.user.username,
          items: item_list,
        };
        const path = 'http://localhost:8000/order/';
        axios.post(path, details)
          .then((res) => {
            if (res.data.status === 'success') {
              this.$router.push({ name: 'Order' });
            } else {
              this.msgStatus = res.data.status;
              this.message = res.data.message;
              this.showMessage = true;
              setTimeout(() => {
                this.showMessage = false;
              }, 5000);
            }
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
      }
    },
  },
  created() {
    if (this.user.is_login) {
      this.getCartItem();
    } else {
      this.$router.push({ name: 'Login' });
    }
  },
};
</script>

<style scoped>
  .spinbtn {
    min-width: 50px;
    max-width: 150px;
    text-align: center
  }

  .money {
    color: red;
    font-size: 300%;
  }
</style>
