<template>
<div style="width: 100%; height: 100%;">
  <el-card class="box-card" style="border: 1px solid #cccccc; box-shadow: 0 0 0 black; border-radius: 0; display: flex; flex-direction: column; width: 390px">
    <div class="createButton" @click="monkeyFormVis = true" style="width: 350px">
    <i class="el-icon-document-add" style="margin-right: 5px;"></i>Create the auto exploration script
    </div>
  </el-card>
  <el-dialog
      title="Auto exploration parameter settings"
      :visible.sync="monkeyFormVis"
      width="40%"
      :before-close="handleClose">
      <el-form :model="form">
        <el-form-item label="Execute exploration times" :label-width="100">
          <el-input v-model="form.monkey_time" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="bottom left coordinates - Example: -6.8027, 0.8077" :label-width="100">
          <el-input v-model="form.left_bottom" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="top right coordinates - Example: 6.5729, 6.9426" :label-width="100">
          <el-input v-model="form.right_top" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="monkeyFormVis = false">Cancel</el-button>
        <el-button type="primary" @click="generateMonkey">OK</el-button>
      </div>
  </el-dialog>
</div>
</template>

<script>
export default {
  name: "Monkey",
  data() {
    return {
      monkeyFormVis: false,
      form: {
        monkey_time: '',
        left_bottom: '',
        right_top: ''
      }
    }
  },
  methods: {
    async generateMonkey() {
      const res = await this.$http.post("/monkey",{
        monkey_time : this.form.monkey_time,
        left_bottom : this.form.left_bottom,
        right_top   : this.form.right_top
      });
      this.monkeyFormVis = false
      this.$message({
        message: 'Auto exploration script created successfully',
        type: 'success'
      });
      this.$router.push({
        path:`/TestReplay`
      })
    }
  }
}

</script>

<style scoped>
.scriptArea {
  width: 50%;
  height: 50%;
  background: white;
  border: 1px solid black;
  margin-left: 25%;
}
.blankArea {
  width: 50%;
  height: 25%;
  /*background: green;*/
  margin-left: 25%;
}
.createButton {
  width: 160px;
  height: 40px;
  background: dodgerblue;
  text-align: center;
  line-height: 38px;
  font-size: 15px;
  font-weight: bold;
  color: white
}
.createButton:hover {
  cursor: pointer;
}
</style>
