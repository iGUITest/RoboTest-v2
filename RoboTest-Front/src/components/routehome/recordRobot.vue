<template>
  <div>
    <el-card class="box-card" style="border: 1px solid #cccccc; box-shadow: 0 0 0 black; border-radius: 0; display: flex; flex-direction: column; width: 650px">
      <div style="display: flex; flex-direction: row;">
        <div class="optBtn" @click="showCreateRecordDialog()" style="width: 200px; height: 40px; background: lightseagreen; text-align: center; line-height: 38px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-video-play" style="margin-right: 5px;"></i>Start recording
        </div>
        <div class="optBtn" @click="existImg()" style="width: 200px; height: 40px; background: dodgerblue; text-align: center; line-height: 38px; margin-left: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-picture-outline" style="margin-right: 5px;"></i>Get pictures
        </div>
        <div class="optBtn" @click="endRecord()" style="width: 200px; height: 40px; background: orangered; text-align: center; line-height: 38px; margin-left: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-video-pause" style="margin-right: 5px;"></i>Stop recording
        </div>
      </div>
      <div class="buttonBox" style="display: flex; flex-direction: row;">
        <input type="file" ref="file" style="position:absolute; clip:rect(0 0 0 0);"
               @change="changeFunc()"/>
        <div class="optBtn" @click="sendControl()" style="width: 200px; height: 40px; background: lightseagreen; text-align: center; line-height: 38px; margin-top: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-upload" style="margin-right: 5px;"></i>Save instructions
        </div>
        <div class="optBtn" @click="clickFunc()" style="width: 200px; height: 40px; background: dodgerblue; text-align: center; line-height: 38px; margin-left: 10px; margin-top: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-picture" style="margin-right: 5px;"></i>Choose pictures
        </div>
        <div class="optBtn" @click="resetFunc()" style="width: 200px; height: 40px; background: orangered; text-align: center; line-height: 38px; margin-left: 10px; margin-top: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-delete-solid" style="margin-right: 5px;"></i>Reset instructions
        </div>
      </div>
    </el-card>
    <div><br></div>

    <el-card class="box-card" style="border: 1px solid #cccccc; box-shadow: 0 0 0 black; border-radius: 0">
      <el-col :span="12" style="margin-top: -15px;">
        <div>
          <h2>Screenshot</h2>
        </div>
        <div class="container" style="background-color: burlywood;"
             @mousedown="mousedown" @mouseup="mouseup" @mousemove="mousemove">
          <canvas id="myCanvas" ref="myCanvas"
                  :width="CW" :height="CH">
            <!--        @mousedown="mousedown" @mouseup="mouseup" @mousemove="mousemove"-->
          </canvas>
        </div>
        <div class="XList" style="width: 640px; height: 30px; line-height: 30px; background: #e9e9e9; border: 1px solid #cccccc; margin-top: 20px">
          <div style="margin-left: 10px">X : {{ XList }}</div>
        </div>
        <div class="YList" style="width: 640px; height: 30px; line-height: 30px; background: #e9e9e9; border: 1px solid #cccccc; margin-top: 20px">
          <div style="margin-left: 10px">Y : {{ YList }}</div>
        </div>
        <div><br></div>
        <div><br></div>

      </el-col>
      <el-col :span="12" style="margin-top: -15px;">
        <div>
          <h2>Script</h2>
          <div class="Script" style="white-space: pre-wrap; width: 640px; height: 580px; background: #e9e9e9; border: 1px solid #cccccc">
            <div style="margin-left: 20px;">{{ scriptFile }}</div>
          </div>
        </div>

      </el-col>
    </el-card>
    <el-dialog title="Create Script" :visible.sync="this.dialogCreateRecordVisible">
      <el-form :model="scriptInfo">
        <el-form-item label="Script name" :label-width="formLabelWidth">
          <el-input v-model="scriptInfo.name" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">Cancel</el-button>
        <el-button type="primary" @click="beginRecord">OK</el-button>
      </div>
    </el-dialog>

  </div>


</template>

<script>
let inputElement = null
export default {
  name: "hello-world",
  data() {
    let canvasW = 640,
      canvasH = 480
    return {
      XList: [],
      YList: [],
      valueUrl: '',
      CW: canvasW,
      CH: canvasH,
      IW: 0,
      IH: 0,
      IL: 0,
      IT: 0,
      flag: false,
      x: 0,
      y: 0,
      RecordImg: '',

      step: 0,
      fileName: '',
      imageOutputPath: '',
      fileFormat: '',

      scriptFile: '',

      isRecord: false,

      dialogCreateRecordVisible: false,

      scriptInfo: {
        name: '',
      },
    };
  },
  watch: {},
  computed: {},
  methods: {
    clickFunc() {
      this.$refs.file.click();
    },
    changeFunc() {
      let file = this.$refs.file.files[0];
      console.log(this.$refs.file.files[0]);
      if (!file) return;
      let fileExample = new FileReader();
      fileExample.readAsDataURL(file);
      fileExample.onload = ev => {
        console.log(ev.target.result)
        this.IMAGE = new Image();
        this.IMAGE.src = ev.target.result;
        this.IMAGE.onload = _ => {
          // this.CH = this.IMAGE.height;
          // this.CW = this.IMAGE.width;
          this.IW = this.IMAGE.width;
          this.IH = this.IMAGE.height;
          this.IL = (this.CW - this.IW) / 2;
          this.IT = (this.CH - this.IH) / 2;
          this.drawImage();
        }
      }
    },

    resetFunc() {
      this.XList = []
      this.YList = []
    },
    drawImage() {
      this.CTX = this.$refs.myCanvas.getContext('2d');
      this.CTX.clearRect(0, 0, this.CW, this.CH);
      this.CTX.drawImage(this.IMAGE, this.IL, this.IT, this.IW, this.IH);

    },
    mousedown(e) {
      this.flag = true;
      this.x = e.offsetX;
      this.y = e.offsetY;
    },
    mouseup(e) {
      this.flag = false;
    },
    mousemove(e) {
      this.drawRect(e);
    },
    drawRect(e) {
      if (this.flag) {
        let x = this.x;
        let y = this.y;
        let xdis = (this.CW - this.IW) / 2
        let ydis = (this.CH - this.IH) / 2

        this.CTX.beginPath();

        this.CTX.strokeStyle = '#00ff00';
        this.CTX.lineWidth = 1;

        this.XList.push(x - xdis)
        this.YList.push(y - ydis)
        // this.CTX2.fillText("Mouse: X-"+x+",Y-"+y,x,y);
        this.flag = false;
        // this.CTX.strokeRect(x,y,e.offsetX-x,e.offsetY-y);

      }
    },
    async existImg() {
      const res = await this.$http.get("/exist_img", {
        params: {
          step: this.step.toString()
        }
      });
      let R = res.data;
      console.log(R)
      if (R == 200) {
        await this.getImg()
        this.step += 1
      }
    },
    async getImg() {
      const res = await this.$http.get("/get_picture");
      console.log('GET PICTURE!')
      let R = res.data;
      this.RecordImg = 'data:image/jpg;base64,' + R;
      this.IMAGE = new Image();
      this.IMAGE.src = this.RecordImg;
      this.IMAGE.onload = _ => {
        // this.CH = this.IMAGE.height;
        // this.CW = this.IMAGE.width;
        this.IW = this.IMAGE.width;
        this.IH = this.IMAGE.height;
        this.IL = (this.CW - this.IW) / 2;
        this.IT = (this.CH - this.IH) / 2;
        this.drawImage();
      }
    },
    async getScriptFile() {
      const res = await this.$http.post("/get_script_file");
      this.scriptFile = res.data;
    },
    async beginRecord() {
      const res = await this.$http.post("/begin_record", {
        scriptName: this.scriptInfo.name,
      });
      let R = res.data;
      this.step = R.data.step;
      this.imageOutputPath = R.data.image_output_path;
      this.fileName = R.data.file_name;
      this.fileFormat = R.data.file_format;
      this.isRecord = true;
      this.dialogCreateRecordVisible = false;
      console.log(res)
    },
    async endRecord() {

      if (!this.isRecord) {
        this.$message({
          type: "warning",
          message: "Recording has not started yet",
        });
      } else {
        const res = await this.$http.post("/end_record");
        let R = res.data;
        console.log(res)
        this.$message({
          type: "success",
          message: "Recording has ended",
        });
        this.step = 0
        this.$router.push({name: "recordhome"});
      }

    },
    async sendControl() {

      const res = await this.$http.post("/get_control", {
        YList: this.YList,
        XList: this.XList,
        lengthX: this.IW,
        lengthY: this.IH,

      });
      let R = res.data;
      if (R.meta.status == 200) {
        this.$message({
          type: "success",
          message: "Send successfully!",
        })
      }
      this.resetFunc();
      await this.getScriptFile();
    },
    showCreateRecordDialog() {
      this.dialogCreateRecordVisible = true;
    },
    cancelDialog() {
      this.dialogCreateRecordVisible = false;
    }
  },
  created() {
    window.setInterval(() => {
      setTimeout(this.existImg(), 0);
    }, 10000);
  },
  mounted() {

  }
};
</script>

<style scoped>
.container {
  width: 640px;
  height: 480px;
  border: 1px solid #cccccc;
  margin-top: 15px
}
.container:hover {
  opacity: .9;
}
.XList:hover {
  opacity: .9;
}
.YList:hover {
  opacity: .9;
}
.Script:hover {
  opacity: .9;
}
#myCanvas {
  background-color: #e9e9e9;
  /*background-image:url('../../../static/img/bg.jpg');*/
}

.buttonBox {

}
.optBtn:hover {
  cursor: pointer;
}
</style>
