<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline" >
            <el-col style="float: left;width: 20%;">
                <el-form-item label="监控区域" >
                    <el-select v-model="formInline.area"  placeholder="监控区域">
                      <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                          </el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col style="float: left;width: 10%;">
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">查询</el-button>
                </el-form-item>
            </el-col>
            <el-col style="float: right;width: 10%;">
                <el-upload
                        class="upload-demo"
                        :auto-upload= 'true'
                        action="http://127.0.0.1:8000/api/uploadMonitor"
                        accept=".xls,.xlsx"
                        :show-file-list="false"
                        :multiple= 'false'
                        :limit="1"
                        :http-request="uploadFile">
                    <el-button type="primary">文件上传</el-button>
                </el-upload>
            </el-col>
            <el-col style="float: right;width: 10%;">
                <el-upload
                        class="upload-demo"
                        :auto-upload= 'true'
                        action="http://127.0.0.1:8000/api/uploadImage"
                        accept=".png,.jpg,.jpge"
                        :show-file-list="false"
                        :multiple= 'true'
                        :http-request="uploadImage">
                    <el-button type="primary">图片上传</el-button>
                </el-upload>
            </el-col>
        </el-form>
        <baidu-map class="map"
                   :center="{lng: 114.02919,lat: 30.58203,}"
                   :zoom="12"
                   :scroll-wheel-zoom = "true">
            <div v-for = "marker of markers" >
                <bm-marker
                        :position="{lat: marker.lat, lng: marker.lng}"
                        :dragging="false"
                        :height="marker.height"
                        :width="marker.width"
                        @click="infoWindowOpen(marker)">
                        <bm-info-window
                            :show="marker.showFlag"
                            :position="{lng: marker.lng, lat: marker.lat}"
                            @close="infoWindowClose(marker)">
                        <p class = "text">{{'监控点：'+marker.Monitor_points}}</p>
                        <el-image :src = "marker.Image_path" fit="cover"></el-image>
                    </bm-info-window>
                </bm-marker>
            </div>
        </baidu-map>
    </div>
</template>

<script>
    import axios from 'axios';
    import qs from 'qs';
    export default {
        data() {
            return {
                formInline: {
                    area: ''
                },
                options: [{
                  value: '江岸区',
                  label: '江岸区'
                }, {
                  value: '江汉区',
                  label: '江汉区'
                }, {
                  value: '洪山区',
                  label: '洪山区'
                }, {
                  value: '青山区',
                  label: '青山区'
                }, {
                  value: '东西湖区',
                  label: '东西湖区'
                }],
                markers: [],
                showMarker: "true"
            }
        },
        mounted(){
            this.getDate();
        },
        methods: {
            getDate(){
                axios.post('/api/showMonitor/').then(res=>{
                    this.markers = res.data;
                },error=>{
                    console.log(error)
                })
            },
            onSubmit() {
                var params = {
                    area: this.formInline.area
                };
                axios.post('/api/showMonitor/',qs.stringify(params)).then(res=>{
                    this.markers = res.data;
                },error=>{
                    console.log(error)
                })
            },
            infoWindowClose (marker) {
                marker.showFlag= false
            },
            infoWindowOpen (marker) {
                marker.showFlag = true
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
                    url:"/api/uploadMonitor/",
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
            },
            uploadImage (item) {
                console.log(item);
                let form = new FormData();
                form.append('file',item.file);
                let config={
                    headers:{'Content-type':'multipart/form-data'}
                }
                axios({
                    method:"post",
                    url:"/api/uploadImage/",
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
    .map{
        width:100%;
        height:760px;
        overflow:hidden;
    }
    .BMap_cpyCtrl {
        display: none;
    }
    .anchorBL {
        display: none;
    }
    .el-form-item{
        displsy: flex;
    }
</style>
