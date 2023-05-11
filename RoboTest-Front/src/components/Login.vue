<template>
<div class="page">
  <div class="title">Login</div>
  <el-form ref="form" :model="form" label-width="80px" class="loginForm">
    <el-form-item>
      <el-input v-model="form.username" placeholder="Username"></el-input>
    </el-form-item>
    <el-form-item>
      <el-input v-model="form.password" show-password placeholder="Password"></el-input>
    </el-form-item>
    <el-form-item>
      <div type="primary" @click="onSubmit" class="loginButton">Login</div>
    </el-form-item>
  </el-form>
  <div class="outBorder"></div>
</div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message({
        message: 'Login Successful',
        center: true,
        type: 'success'
      });
      this.$router.push({
        path: `/recordrobot`
      })
    },
    jumpToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
.title {
  font-size: 30px;
  margin-bottom: 50px;
  padding-top: 300px;
  margin-left: 49%;
}
.page {
}
.loginButton {
  width: 418px;
  border: 1px solid black;
  margin-top: 20px;
  text-align: center;
  background-color: SteelBlue;
  color: white;
  font-size: 18px;
}
.loginButton:hover {
  cursor: pointer;
}
.loginForm {
  width: 500px;
  margin-left: 760px;
}
.outBorder {
  width: 600px;
  height: 400px;
  background: #f3f5f8;
  margin-left: 740px;
  margin-top: -340px;
  border: 1px #95a5a6 solid;
  box-shadow: 10px 10px 2px #888888;
}
</style>
