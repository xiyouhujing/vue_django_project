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
                    <el-button type="primary" @click="handleAdd">添加</el-button>
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

        <!--新增设备信息界面-->
        <el-dialog title="新增设备信息" :visible.sync="dialogAddVisible" :before-close="handleClose">
            <el-form :model="FormData"  :rules="rules1" ref="FormData" label-width = "120px">
                <el-form-item label="产品类别" :label-width="formLabelWidth">
                    <el-input v-model.number ="FormData.Product_category" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="产品名称" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Product_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="地址" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Address" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户名称" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Customer_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="发展营服" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Development_unit" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户经理" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Customer_manager" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="完工状态" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Opening_status" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="订单日期" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Order_time" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="完工日期" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Completion_time" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="订单数量" :label-width="formLabelWidth">
                    <el-input v-model="FormData.Quantity_ordered" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogAddVisible = false">取 消</el-button>
                <el-button type="primary" @click="addMovie()">提 交</el-button>
            </div>
        </el-dialog>
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
                    date1:'',
                    date2:''
                },
                markers:[],
                showMarker:"true",
                formLabelWidth: '100px',
                dialogAddVisible:false,
                FormData: {
                    Product_category: '',
                    Product_name: '',
                    Address:'',
                    Customer_name: '',
                    Development_unit: '',
                    Customer_manager: '',
                    Opening_status: '',
                    Order_time: '',
                    Completion_time: '',
                    Quantity_ordered:''
                },
                rules1: {
                    movieName: [{required: true, message: '电影名不能为空', trigger: 'blur'}],
                    movieId: [
                        {required: true, message: '电影ID不能为空', trigger: 'blur'},
                        { type: 'number', message: '电影ID必须为数字' }
                    ]
                }
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
            },
            //新增电影信息按钮消息响应函数
            handleAdd(){
                this.dialogAddVisible = true;
                this.FormData = [];
            },
            addMovie(){
                this.$refs.FormData.validate((valid) => {
                    if (valid)
                    {
                        let param = Object.assign({}, this.FormData);
                        console.log(param)
                        axios.post('http://localhost:8090//movie/addmovie', qs.stringify(param))
                            .then(res => {
                                console.log(param)
                                if (res.data.success) {
                                    this.$message({
                                        type: 'info',
                                        message: '添加成功',
                                    });
                                } else {
                                    this.$message({
                                        type: 'info',
                                        message: '添加失败',
                                    });
                                }
                                this.getDate();
                                this.dialogAddVisible = false;
                            });
                    }
                })
            },
            handleClose(done) {
                this.$confirm('确认关闭？')
                    .then(_ => {
                        done();
                    })
                    .catch(_ => {});
            },
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
