<template>
  <div class="container">
    <div class="header">
      <el-row>
        <h3>RoboTest</h3>
      </el-row>
    </div>
    <div class="mainPart">
      <div class="aside">
        <el-menu :router="true" :unique-opened="true" background-color="white">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-s-tools"></i>
              <span>Test Settings</span>
            </template>
            <el-menu-item index="recordRobot">
              <i class="el-icon-video-camera-solid"></i>
              <span>Test Recording</span>
            </el-menu-item>
            <el-menu-item index="TestReplay">
              <i class="el-icon-video-camera"></i>
              <span>Test Replaying</span>
            </el-menu-item>
            <el-menu-item index="EditScript">
              <i class="el-icon-edit-outline"></i>
              <span>Script Editing</span>
            </el-menu-item>
            <el-menu-item index="Monkey">
              <i class="el-icon-mouse"></i>
              <span>Auto Exploration</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </div>
      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.header {
  background-color: SteelBlue;
  font-size: 25px;
  padding-left: 60px;
  color: white;
  -webkit-text-stroke: 1.0px SteelBlue;
  /*box-shadow: 4px 4px 2px black;*/
  height: 10%;
  z-index: 2;
}
.mainPart {
  display: flex;
  flex-direction: row;
  height: 90%;
}
.aside {
  background-color: white;
  width: 250px;
  /*box-shadow: 4px 4px 2px #cccccc;*/
  z-index: 2;
  border-right: 1px solid #cccccc
}
.main {
  background-color: #e9eef3;
  padding-top: 20px;
}
.middle {
  text-align: center;
}
.loginout {
  line-height: 60px;
  text-decoration: none;
}
</style>
