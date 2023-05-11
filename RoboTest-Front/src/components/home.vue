<template>
  <el-container class="container">
    <el-header class="header" height="110px">
      <h1 style="#ffffff">Console</h1>
    </el-header>
    <el-main class="main">
      <div class="box1" @click="Goto1()">Project1</div>
      <div class="box2" @click="Goto2()">Project2</div>
      <div class="box3" @click="Goto3()">Project3</div>
    </el-main>
  </el-container>
</template>

<script>
export default {
  methods: {
    Goto1() {

    },
    Goto2() {

    },
    Goto3() {

    },
  },
};
</script>

<style>
.container {
  height: 100%;
}
.header {
  background-color: #040d16;
  text-align: center;
  color: #ffffff;
  font-size:25px;
}
.main {
  background-color: #ffffff;
  color: #333;
}
.box1 {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-125%, -125%);
  width: 550px;
  padding: 61px;
  background-image: url("../../static/images/title1.png");
  box-sizing: border-box;
  border-radius: 15px;
}
.box1:hover {
  border: 0.1px solid #000;
  transition: all 0.3s;
  box-shadow: 0px 15px 25px rgba(0, 0, 0, 0.5);
}

.box2 {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(25%, -125%);
  width: 550px;
  padding: 61px;
  background-image: url("../../static/images/title2.png");
  box-sizing: border-box;
  border-radius: 15px;
}
.box2:hover {
  border: 0.1px solid #000;
  transition: all 0.3s;
  box-shadow: 0px 15px 25px rgba(0, 0, 0, 0.5);
}
.box3 {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-125%, 100%);
  width: 550px;
  padding: 61px;
  background-image: url("../../static/images/title3.png");
  box-sizing: border-box;
  border-radius: 15px;
}
.box3:hover {
  border: 0.1px solid #000;
  transition: all 0.3s;
  box-shadow: 0px 15px 25px rgba(0, 0, 0, 0.5);
}
</style>
