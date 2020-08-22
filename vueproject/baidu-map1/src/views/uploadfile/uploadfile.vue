<template>
       <el-upload
               class="excel-uploader"
               drag
               :auto-upload= 'true'
               action="http://127.0.0.1:8000/api/upload"
               accept=".xls,.xlsx"
               :multiple= 'false'
               list-type="picture"
               :before-upload="beforeUpload"
               :limit= 1
               :before-remove="beforeRemove"
               :on-remove="handleRemove"
               :on-exceed="handleExceed"
               :http-request="uploadFile">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传excel文件,且不超过10M</div>
       </el-upload>
</template>

<script>
       import axios from 'axios';
       import qs from 'qs';
    export default {
           name: 'uploadfile',
           data(){
                  return{
                         upath:'',
                         result:'',
                         uping:0
                  }
           },
           methods: {
                  beforeUpload (file) {
                         console.log('beforeUpload')
                         console.log(file.type)
                         const isText = file.type === 'application/vnd.ms-excel'
                         const isTextComputer = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                         return (isText | isTextComputer)
                  },
                  handleExceed(files, fileList) {
                         this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
                  },
                  beforeRemove(file, fileList) {
                         return this.$confirm(`确定移除 ${ file.name }？`)
                  },
                  handleRemove(file, fileList) {
                         console.log(file, fileList);
                  },
                  uploadUrl:function () {
                         // 因为action参数是必填项，我们使用二次确认进行文件上传时，直接填上传文件的url会因为没有参数导致api报404，所以这里将action设置为一个返回为空的方法就行，避免抛错
                         return ""
                  },
                  uploadFile (item) {
                         console.log(item);
                         let form = new FormData();
                         form.append('file',item.file);
                         let config={
                                headers:{'Content-type':'multipart/form-data'}
                         }
                         axios({
                                method:"post",
                                url:"/api/upload/",
                                headers:{'Content-type':'multipart/form-data'},
                                data:form
                         }).then(
                                 res=>{
                                        // console(res.data)
                                        this.$message({
                                               type:'info',
                                               message: res.data.msg
                                        })
                                 },
                         );
                  }
           }
    }
</script>

<style lang="scss">
       .el-upload{
              width:100%;
       }
       .el-upload-dragger{
              width:100%;
       }
       .el-upload__tip
       {
              text-align: center;
       }
</style>
