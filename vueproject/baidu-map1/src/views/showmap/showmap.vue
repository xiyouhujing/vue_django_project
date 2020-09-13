<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline" >
            <el-col style="float: left;width: 25%;">
                <el-form-item label="项目经理" >
                    <el-input v-model="formInline.user" placeholder="项目经理" resize="horizontal"></el-input>
                </el-form-item>
            </el-col>
            <el-col style="float: left;width: 25%;">
                <el-form-item label="完工状态" prop="region">
                    <el-select v-model="formInline.status" placeholder="完工状态">
                        <el-option label="已完工" value="已完工"></el-option>
                        <el-option label="未完工" value="未完工"></el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col style="float: left;width: 40%;">
                <el-form-item label="下单时间" >
                    <el-col :span="11">
                        <el-form-item prop="date1">
                            <el-date-picker type="date" value-format="yyyy-MM-dd" placeholder="选择开始日期" v-model="formInline.date1" style="width: 100%;"></el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col class="line" :span="1" style="">-</el-col>
                    <el-col :span="11">
                        <el-form-item prop="date2">
                            <el-date-picker type="date" value-format="yyyy-MM-dd" placeholder="选择结束日期" v-model="formInline.date2" style="width: 100%;"></el-date-picker>
                        </el-form-item>
                    </el-col>
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
                <div v-if = "marker.status === '未完工'">
                    <bm-marker
                            :position="{lat: marker.lat, lng: marker.lng}"
                            :dragging="true"
                            v-show:false
                            :icon = "{url: require('../../assets/images/black.png'), size: {width: 32, height: 32}}"
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
                <div v-else>
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
                    user: '',
                    status: '',
                    date1: '',
                    date2: ''
                },
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
