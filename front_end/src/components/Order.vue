<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h2>订单</h2>
        <hr><br>
        <alert :message=message :status=msgStatus v-if="showMessage"></alert>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 30%">订单号</th>
              <th scope="col" style="width: 30%">总金额</th>
              <th scope="col" style="width: 20%">状态</th>
              <th scope="col" style="width: 20%">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.price }}</td>
              <td>{{ order.status }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    v-if="order.status === '待支付'"
                    type="button"
                    class="btn btn-primary"
                  >
                    去支付
                  </button>
                  <button
                    v-else-if="order.status === '待发货'"
                    type="button"
                    class="btn btn-primary"
                  >
                    提醒发货
                  </button>
                  <button
                    v-else-if="order.status === '已发货'"
                    type="button"
                    class="btn btn-primary"
                  >
                    查看物流
                  </button>
                  <button
                    v-else-if="order.status === '已完成'"
                    type="button"
                    class="btn btn-primary"
                  >
                    去评价
                  </button>
                  <button
                    v-else-if="order.status === '已取消'"
                    type="button"
                    class="btn btn-danger"
                  >
                    删除订单记录
                  </button>
                  <button
                    v-else-if="order.status === '已退款'"
                    type="button"
                    class="btn btn-primary"
                  >
                    查看退款进度
                  </button>
                  <button
                    v-else-if="order.status === '已退货'"
                    type="button"
                    class="btn btn-primary"
                  >
                    查看退货进度
                  </button>
                  <button type="button" class="btn btn-secondary">订单详情</button>
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
  name: 'Order',
  data() {
    return {
      orders: [],
      message: '',
      msgStatus: 'success',
      showMessage: false,
    };
  },
  props: ['user'],
  components: {
    alert: Alert,
  },
  methods: {
    getOrder() {
      const path = `http://localhost:8000/order/?user=${this.user.username}`;
      axios.get(path)
        .then((res) => {
          this.orders = res.data.orders;
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
  },
  created() {
    if (this.user.is_login) {
      this.getOrder();
    } else {
      this.$router.push({ name: 'Login' });
    }
  },
};
</script>

<style scoped>

</style>
