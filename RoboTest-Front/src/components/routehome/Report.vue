<template>
  <div>
    <el-table
    :data="tableData"
    style="width: 100%">
    <el-table-column
      label="Report serial number"
      width="360">
      <template slot-scope="scope">
        <span>{{ scope.row.order }}</span>
      </template>
    </el-table-column>
      <el-table-column
        label="Report time"
        width="360">
        <template slot-scope="scope">
          <span>{{ scope.row.time }}</span>
        </template>
      </el-table-column>
      </el-table-column>
      <el-table-column
        label="Source file name"
        width="360">
        <template slot-scope="scope">
          <span>{{ scope.row.file }}</span>
        </template>
      </el-table-column>
    <el-table-column
      label="Report type"
      width="360">
      <template slot-scope="scope">
        <span>{{ scope.row.type }}</span>
      </template>
    </el-table-column>
      </el-table-column>
      <el-table-column
        label="severity"
        width="360">
        <template slot-scope="scope">
          <span>{{ scope.row.level }}</span>
        </template>
      </el-table-column>
    <el-table-column label="operation">
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="primary"
          @click="handleEdit(scope.$index, scope.row)">show details
          </el-button>

      </template>
    </el-table-column>
  </el-table>
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
      tableData: [{
        order: '1',
        time: '2022-06-01 15:12',
        file: 'test_113',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '2',
        time: '2022-06-01 16:22',
        file: 'test_114',
        type: 'FileExistsError',
        level: 'HIGH'
      }, {
        order: '3',
        time: '2022-06-01 16:55',
        file: 'test_120',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '4',
        time: '2022-06-01 17:20',
        file: 'test_129',
        type: 'IndexError',
        level: 'HIGH'
      }, {
        order: '5',
        time: '2022-06-01 18:33',
        file: 'test_130',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '6',
        time: '2022-06-02 07:02',
        file: 'test_149',
        type: 'FileExistsError',
        level: 'HIGH'
      }, {
        order: '7',
        time: '2022-06-02 07:26',
        file: 'test_150',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '8',
        time: '2022-06-02 08:20',
        file: 'test_154',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '9',
        time: '2022-06-02 08:34',
        file: 'test_157',
        type: 'FileExistsError',
        level: 'HIGH'
      }, {
        order: '10',
        time: '2022-06-02 09:11',
        file: 'test_170',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '11',
        time: '2022-06-02 09:24',
        file: 'test_178',
        type: 'IndexError',
        level: 'HIGH'
      }, {
        order: '12',
        time: '2022-06-02 11:23',
        file: 'test_241',
        type: 'SyntaxError',
        level: 'MEDIUM'
      }, {
        order: '13',
        time: '2022-06-02 11:57',
        file: 'test_260',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '14',
        time: '2022-06-02 12:05',
        file: 'test_277',
        type: 'SyntaxError',
        level: 'MEDIUM'
      }, {
        order: '15',
        time: '2022-06-02 14:46',
        file: 'test_301',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '16',
        time: '2022-06-02 15:13',
        file: 'test_322',
        type: 'SyntaxError',
        level: 'MEDIUM'
      }, {
        order: '17',
        time: '2022-06-02 15:35',
        file: 'test_330',
        type: 'IndexError',
        level: 'HIGH'
      }, {
        order: '18',
        time: '2022-06-02 16:12',
        file: 'test_345',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '19',
        time: '2022-06-02 18:23',
        file: 'test_412',
        type: 'AttribteError',
        level: 'MEDIUM'
      }, {
        order: '20',
        time: '2022-06-01 18:42',
        file: 'test_441',
        type: 'IndexError',
        level: 'HIGH'
      }, {
        order: '21',
        time: '2022-06-01 19:09',
        file: 'test_457',
        type: 'AttribteError',
        level: 'MEDIUM'
      }],
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
        message: "Start Replaying",
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
    handleEdit(index, row) {
      this.$alert('Traceback (most recent call last):\n' +
        'File “E:/TESTS/test_113.py”, line 20, in\n' +
        'list = list.append(num)\n' +
        'AttributeError: ‘NoneType’ object has no attribute ‘append’\n', 'Report Details', {
        confirmButtonText: 'OK',
        callback: action => {
          this.$message({
            type: 'info',
            message: `action: ${ action }`
          });
        }
      });
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
