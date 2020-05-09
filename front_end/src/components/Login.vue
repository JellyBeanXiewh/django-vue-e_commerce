<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h2>登录</h2>
        <hr><br>
        <alert :message=message :status=msgStatus v-if="showMessage"></alert>
        <br>
        <div class="row justify-content-md-center">
          <div class="card">
            <div class="card-body text-center">
              <b-form @submit="onSubmit">
                <b-form-group
                  id="input-group-1"
                  label="用户名"
                  label-for="input-1"
                >
                  <b-form-input
                    id="input-1"
                    v-model="form.username"
                    type="text"
                    required
                    placeholder="请输入用户名"
                  ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="密码" label-for="input-2">
                  <b-form-input
                    id="input-2"
                    v-model="form.password"
                    type="password"
                    required
                    placeholder="请输入密码"
                  ></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">登录</b-button>
              </b-form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
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
    onSubmit(evt) {
      evt.preventDefault();
      const path = 'http://localhost:8000/login/';
      axios.post(path, this.form)
        .then((res) => {
          if (res.data.is_valid) {
            this.$emit('update:user', { username: this.form.username, is_login: true });
            this.$router.push({ name: 'Index' });
          } else {
            this.msgStatus = 'danger';
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
          // eslint-disable-next-line
          console.error(error);
          setTimeout(() => {
            this.showMessage = false;
          }, 5000);
        });
    },
  },
  created() {
    if (this.user.is_login) {
      this.$router.push({ name: 'Index' });
    }
  },
};
</script>
