<template>
  <div>
    <el-card class="box-card" style="border: 1px solid #cccccc; box-shadow: 0 0 0 black; border-radius: 0; display: flex; flex-direction: column; width: 400px">
      <div style="display: flex; flex-direction: row;">
        <el-upload
          class="upload-demo"
          ref="upload"
          action=""
          :on-change="readFile"
          :file-list="fileList"
          :auto-upload="false"
          :show-file-list="false"
        >
          <div style="width: 180px; height: 40px; background: dodgerblue; text-align: center; line-height: 38px; font-size: 15px; font-weight: bold; color: white">
            <i class="el-icon-folder-opened" style="margin-right: 5px;"></i>Choose Script
          </div>
        </el-upload>
        <div class="runScript" @click="runReplay()" style="width: 180px; height: 40px; background: lightseagreen; text-align: center; line-height: 38px; margin-left: 10px; font-size: 15px; font-weight: bold; color: white">
          <i class="el-icon-document-checked" style="margin-right: 5px;"></i>Execute Script
        </div>
      </div>
    </el-card>
    <div><br></div>

    <el-card class="box-card" style="border: 1px solid #cccccc; box-shadow: 0 0 0 black; border-radius: 0">
      <el-col :span="12">
        <div>
          <h2>
            Script
          </h2>
          <div class="ScriptContent" style="width: 640px; height: 480px; background: #e9e9e9; border: 1px solid #cccccc; overflow: auto">
            <div v-for="(line, index) of this.script_data" style="padding-left: 20px; height: 100px; width: 100%; display: flex; flex-direction: row; align-items: center;">
            {{index}}:&nbsp;&nbsp;&nbsp;{{line[0]}}(&nbsp;&nbsp;
            <img
              class="base64Img"
              :src="'data:image/jpg;base64,' + line[1]"
              alt=""
              style="width: 100px"
            />
              &nbsp;&nbsp;)
            </div>
          </div>
        </div>
        <div><br></div>


      </el-col>
      <el-col :span="12">
        <h2>
          Screenshot
        </h2>
        <div class="container" style="background-color: burlywood;"
             @mousedown="mousedown" @mouseup="mouseup" @mousemove="mousemove">
          <canvas id="myCanvas" ref="myCanvas"
                  :width="CW" :height="CH" >
          </canvas>
        </div>
        <div><br></div>

      </el-col>
    </el-card>

  </div>


</template>

<script>
let inputElement = null
export default {
  name:"hello-world",
  data() {
    let canvasW = 640,
      canvasH = 480
    return {
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
      RecordImg:'',

      screenshotURI:'',
      textarea: "",
      fileList: [],

      step: 0,
      fileName:'',
      imageOutputPath:'',
      fileFormat:'',

      scriptFile:'',

      isRecord:false,

      dialogSavePictureVisible:false,

      script_data:[],

      shotInfo:{
        name:'',
        imgdata:'',
        width:"",
        height:""
      },
    };
  },
  watch: {},
  computed: {},
  methods: {
    readFile(file) {
      let reader = new FileReader();
      if (typeof FileReader === "undefined") {
        this.$message({
          type: "info",
          message: "Your browser does not support file reading",
        });
        return;
      }
      let _this = this;
      reader.readAsText(file.raw, "gb2312");
      this.fileName = file.raw.name;
      this.getScriptData()
      reader.onload = function (e) {
        //console.log(e.target.result);
        _this.textarea = e.target.result;
      };

    },
    async runReplay(){
      const res = await this.$http.post("/run_replay");
      this.$message({
        type: "success",
        message: "Start replaying",
      });
    },
    async getScriptData(){
      let scriptName = this.fileName.split('.')[0]
      const res = await this.$http.post("/get_script_data",{
        scriptName : scriptName,
      });
      this.script_data = res.data;
      console.log(this.script_data)
      this.step = 1
    },
    drawImage(){
      this.CTX = this.$refs.myCanvas.getContext('2d');
      this.CTX.clearRect(0,0,this.CW,this.CH);
      this.CTX.drawImage(this.IMAGE,this.IL,this.IT,this.IW,this.IH);

    },
    mousedown(e){
      this.flag = true;
      this.x = e.offsetX;
      this.y = e.offsetY;
    },
    mouseup(e){
      this.flag = false;
    },
    mousemove(e){
      this.drawRect(e);
    },
    drawRect(e){
      if(this.flag){
        let x = this.x;
        let y = this.y;

        this.CTX.beginPath();

        this.CTX.strokeStyle = '#00ff00';
        this.CTX.lineWidth = 1;
        // this.CTX2.fillText("Mouse: X-"+x+",Y-"+y,x,y);
        //this.CTX.strokeRect(x,y,e.offsetX-x,e.offsetY-y);
        let imageData = this.CTX.getImageData(x,y,e.offsetX-x,e.offsetY-y);
        this.CTX2 = this.$refs.myCanvas2.getContext('2d');
        this.CTX2.clearRect(0,0,this.CW2,this.CH2);
        this.CTX2.putImageData(imageData,0,0,0,0,this.CW2,this.CH2);
        this.screenshotURI = this.$refs.myCanvas2.toDataURL("image/jpg")
        this.shotInfo.width = e.offsetX-x;
        this.shotInfo.height = e.offsetY-y;
      }
    },
    showSavePictureDialog(){
      this.dialogSavePictureVisible = true;
    },
    cancelDialog(){
      this.dialogSavePictureVisible = false;
    },
    async existImg(){
      const res = await this.$http.get("/exist_replay_img",{
        params:{
          step : this.step.toString()
        }
      });
      let R = res.data;
      console.log(R)
      if(R==200){
        await this.getImg()
        this.step += 1
      }
    },
    async getImg(){
      const res = await this.$http.get("/get_picture");

      let R = res.data;
      this.RecordImg = 'data:image/jpg;base64,' + R;
      this.IMAGE = new Image();
      this.IMAGE.src = this.RecordImg;
      this.IMAGE.onload = _ =>{
        // this.CH = this.IMAGE.height;
        // this.CW = this.IMAGE.width;
        this.IW = this.IMAGE.width;
        this.IH = this.IMAGE.height;
        this.IL = (this.CW - this.IW) / 2;
        this.IT = (this.CH - this.IH) / 2;
        this.drawImage();
      }
    },
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
.container{
  width:640px;
  height:480px;
  border: 1px solid #cccccc;
}
.container:hover {
  opacity: .9;
}
.runScript:hover {
  cursor: pointer;
}
#myCanvas{
  background-color: #e9e9e9;
  /*background-image:url('../../../static/img/bg.jpg');*/
}
.ScriptContent:hover {
  opacity: .9;
}
.buttonBox{

}
</style>
