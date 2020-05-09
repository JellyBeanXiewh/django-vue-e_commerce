<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h2>商品详情</h2>
        <hr><br>
        <alert :message=message :status=msgStatus v-if="showMessage"></alert>
        <br>
        <table class="table table-hover">
          <tbody>
            <tr>
              <td style="width: 35%">商品名称</td>
              <td>{{ item.name }}</td>
            </tr>
            <tr>
              <td>价格</td>
              <td><h1>{{ item.price }}</h1></td>
            </tr>
            <tr>
              <td>库存剩余</td>
              <td>{{ item.inventory }}</td>
            </tr>
            <tr>
              <td>数量</td>
              <td>
                <div class="spinbtn">
                  <b-form-spinbutton
                    size="sm"
                    inline
                    min=1
                    :max=item.inventory
                    v-model="amount"></b-form-spinbutton>
                </div>
              </td>
            </tr>
            <tr>
              <td></td>
              <td>
                <button
                  type="button"
                  class="btn btn-success"
                  @click="addToCart"
                  :disabled="item.inventory === 0"
                >
                  加入购物车
                </button>
              </td>
            </tr>
            <tr>
              <td>商品描述</td>
              <td>{{ item.description }}</td>
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
  name: 'Item',
  data() {
    return {
      amount: 1,
      message: '',
      msgStatus: 'success',
      showMessage: false,
      item: {},
      itemID: this.$route.params.itemid,
    };
  },
  props: ['user'],
  methods: {
    getItemInfo() {
      const path = `http://localhost:8000/item/${this.itemID}`;
      axios.get(path)
        .then((res) => {
          // eslint-disable-next-line no-console
          console.log(res);
          this.item = res.data.item;
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
    addToCart() {
      if (this.user.is_login) {
        const path = 'http://localhost:8000/cart/';
        const payload = {
          user: this.user.username,
          item_id: this.itemID,
          amount: this.amount,
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
            // eslint-disable-next-line
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
  components: {
    alert: Alert,
  },
  created() {
    this.getItemInfo();
  },
};
</script>

<style scoped>
  h1 {
    color: red;
  }

  .spinbtn {
    min-width: 50px;
    max-width: 150px;
    text-align: center
  }
</style>
