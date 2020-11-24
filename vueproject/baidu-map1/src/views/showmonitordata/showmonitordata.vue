<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline" >
            <el-col style="float: left;width: 25%;">
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
        </el-form>
        <baidu-map class="map"
                   :center="{lng: 114.02919,lat: 30.58203,}"
                   :zoom="10"
                   :scroll-wheel-zoom = "true">
            <div v-for = "marker of markers" >
                <bm-marker
                        :position="{lat: marker.lat, lng: marker.lng}"
                        :dragging="true"
                        v-show:false
                        :icon = "{url: require('../../assets/images/red.png'), size: {width: 32, height: 32}}"
                        @click="infoWindowOpen(marker)">
                        <bm-info-window
                            :show="marker.showFlag"
                            :position="{lng: marker.lng, lat: marker.lat}"
                            @close="infoWindowClose(marker)">
                        <p class = "text">{{'地址：'+marker.address}}</p>
                        <p class = "text">{{'产品名称：'+marker.prodect_name}}</p>
                        <p class = "text">{{'完工状态：'+marker.status}}</p>
                        <p class = "text">{{'项目经理：'+marker.customer_manager}}</p>
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
                axios.post('/api/showMap/').then(res=>{
                    this.markers = res.data;
                },error=>{
                    console.log(error)
                })
            },
            onSubmit() {
                var params = {
                    userName: this.formInline.user,
                    projectStatus: this.formInline.status,
                    beginDate: this.formInline.date1,
                    endDate: this.formInline.date2
                };
                axios.post('/api/showMap/',qs.stringify(params)).then(res=>{
                    this.markers = res.data;
                    console.log(this.markers);
                },error=>{
                    console.log(error)
                })
            },
            infoWindowClose (marker) {
                marker.showFlag= false
            },
            infoWindowOpen (marker) {
                marker.showFlag = true
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
