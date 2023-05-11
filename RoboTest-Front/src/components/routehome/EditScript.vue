<template>
  <div>
    <el-upload
      class="upload-demo"
      ref="upload"
      action=""
      :on-change="readFile"
      :file-list="fileList"
      :auto-upload="false"
      :show-file-list="false"
    >
      <el-button size="small" type="primary">Choose Script</el-button>
    </el-upload>
    <div><br></div>

    <el-card class="box-card" >
      <el-col :span="12">
        <div class="container" style="background-color: burlywood;"
             @mousedown="mousedown" @mouseup="mouseup" @mousemove="mousemove">
          <canvas id="myCanvas" ref="myCanvas"
                  :width="CW2" :height="CH2" >
            <!--        @mousedown="mousedown" @mouseup="mouseup" @mousemove="mousemove"-->
          </canvas>
        </div>
        <div><br></div>
        <div class = "buttonBox" >
          <input type="file" ref="file" style="position:absolute; clip:rect(0 0 0 0);"
                 @change="changeFunc()" />
          <el-button size="small" @click="clickFunc()" type="primary"
          >Choose Picture</el-button
          >

        </div>

        <div><br></div>
        <el-button size="small" @click="saveFile()" type="primary"
        >Save File</el-button
        >
        <div><br /></div>
        <el-input
          type="textarea"
          autosize
          placeholder="Please enter content"
          v-model="textarea"
        >
        </el-input>

      </el-col>
      <el-col :span="12">
        <div class="container" style="background-color: burlywood;">
          <canvas id="myCanvas2" ref="myCanvas2"
                  :width="CW" :height="CH" >
          </canvas>
        </div>
        <div><br></div>
        <el-button size="small" @click="showSavePictureDialog()" type="primary"
        >Save Picture</el-button
        >

        <div>
          <h2>
            script
          </h2>
          <div v-for="line of this.script_data">
            {{line[0]}}(

            <img
              class="base64Img"
              :src="'data:image/jpg;base64,' + line[1]"
              alt=""
            />
            )
          </div>

        </div>
      </el-col>
    </el-card>



    <el-dialog title="Save Picture" :visible.sync="this.dialogSavePictureVisible">
      <el-form :model="shotInfo">
        <el-form-item label="Picture Name" :label-width="formLabelWidth">
          <el-input v-model="shotInfo.name" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelDialog()">Cancel</el-button>
        <el-button type="primary" @click="savePicture()">OK</el-button>
      </div>
    </el-dialog>

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
      CW2: canvasW,
      CH2: canvasH,
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
    async getScriptData(){
      let scriptName = this.fileName.split('.')[0]
      const res = await this.$http.post("/get_script_data",{
        scriptName : scriptName,
      });
      this.script_data = res.data;
      console.log(this.script_data)
      },
    async saveFile() {
      const res = await this.$http.post("/editscript_save",{
        fileName : this.fileName,
        content: this.textarea,
      });
      this.$message({
        type: "success",
        message: "Saved successfully!",
      })
      this.getScriptData()
    },
    clickFunc(){
      this.$refs.file.click();
    },
    changeFunc(){
      let file = this.$refs.file.files[0];
      console.log(this.$refs.file.files[0]);
      if(!file) return;
      let fileExample = new FileReader();
      fileExample.readAsDataURL(file);
      fileExample.onload=ev=>{
        console.log(ev.target.result)
        this.IMAGE = new Image();
        this.IMAGE.src = ev.target.result;
        this.IMAGE.onload = _ =>{
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
    endEdit(){

    },
    showSavePictureDialog(){
      this.dialogSavePictureVisible = true;
    },
    cancelDialog(){
      this.dialogSavePictureVisible = false;
    },
    async savePicture(){
      const res = await this.$http.post("/save_screenshot",{
        imgName : this.shotInfo.name,
        screenshotURI : this.screenshotURI,
        width : this.shotInfo.width,
        height : this.shotInfo.height
      });
      let R = res.data;
      console.log(R)
      if(R==200){
        this.$message({
          type: "success",
          message: "Saved successfully!",
        })
        this.dialogSavePictureVisible = false;
      }
      else{
        this.$message({
          type: "warning",
          message: "Save failed!",
        })
      }
    }
  },
  // created() {
  //   window.setInterval(() => {
  //     setTimeout(this.existImg(), 0);
  //   }, 10000);
  // },
  mounted() {

  }
};
</script>

<style scoped>
.container{
  width:640px;height:480px;border: 1px solid red;

}
#myCanvas{
  background-color: antiquewhite;
  /*background-image:url('../../../static/img/bg.jpg');*/
}

.buttonBox{

}
</style>
