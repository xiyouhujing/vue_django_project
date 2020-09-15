<template>
    <div>
        <div>
            <el-form :inline="true" style="margin-bottom: 10px">
                    <el-button class = "addbutton1" type="primary"  @click="handleAdd()">添加</el-button>
            </el-form>
        </div>
        <div>
            <el-table
                    :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)"
                    :cell-style="cellStyle"
                    :header-cell-style="rowClass"
                    align="center"
                    border
                    tooltip-effect="dark"
                    :row-style="{height:'48px'}"
                    style="width: 100%;margin:auto auto">
                <!--<el-table-column prop="Serial_number" label="序号">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" :disabled = "true"  v-model="scope.row.Serial_number"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Serial_number}}</span>
                    </template>
                </el-table-column>-->
                <el-table-column prop="Product_category" label="产品类别">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Product_category"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Product_category}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Product_name" label="产品名称">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Product_name"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Product_name}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Address" label="地址">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Address"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Address}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Customer_name" label="客户名称">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Customer_name"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Customer_name}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Development_unit" label="发展营服">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Development_unit"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Development_unit}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Customer_manager" label="客户经理">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Customer_manager"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Customer_manager}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Opening_status" label="完工状态">
                    <template slot-scope="scope">
                        <el-select size="mini" v-show="scope.row.show" v-model="scope.row.Opening_status" placeholder="完工状态">
                            <el-option label="已完工" value="已完工"></el-option>
                            <el-option label="未完工" value="未完工"></el-option>
                        </el-select>
                        <span v-show="!scope.row.show">{{scope.row.Opening_status}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Order_time" label="订单日期">
                    <template slot-scope="scope">
                        <el-date-picker size = "mini" type="date" value-format="yyyy-MM-dd" placeholder="订单日期" v-show="scope.row.show" v-model="scope.row.Order_time" style="width: 100%;"></el-date-picker>
                        <span v-show="!scope.row.show">{{scope.row.Order_time}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Completion_time" label="完工日期">
                    <template slot-scope="scope">
                        <el-date-picker size = "mini" type="date" value-format="yyyy-MM-dd" placeholder="完工日期" v-show="scope.row.show" v-model="scope.row.Completion_time" style="width: 100%;"></el-date-picker>
                        <span v-show="!scope.row.show">{{scope.row.Completion_time}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="Quantity_ordered" label="订单数量">
                    <template slot-scope="scope">
                        <el-input size="mini" v-show="scope.row.show" v-model="scope.row.Quantity_ordered"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.Quantity_ordered}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="" label="操作">
                    <template slot-scope="scope">
                        <el-dropdown trigger="click">
                            <el-button type="text" size="mini">操作
                                <i class="el-icon-arrow-down el-icon--right"></i>
                            </el-button>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item>
                                    <el-button @click="handleDelete(scope.$index)" class="btn-text-red" type="text" size="mini"
                                               icon="el-icon-delete">删除
                                    </el-button>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-button @click="handleModfiy(scope.row,scope.$index)" type="text" size="mini" icon="el-icon-edit">编辑</el-button>
                                </el-dropdown-item>
                                <el-dropdown-item>
                                    <el-button @click="save1(scope.row,scope.$index)" type="text" size="mini" icon="el-icon-success">保存</el-button>
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </template>
                </el-table-column>
            </el-table>

            <!--分页显示功能-->
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[5, 10, 20, 30, 40]"
                    :page-size="10"
                    :background="true"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="tableData.length">
            </el-pagination>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import qs from 'qs';
    export default {
        data() {
            return {
                tableData: [],
                tempIndex:[],
                // 默认显示第一条
                currentPage: 1,
                PageSize: 10,
            }
        },
        methods: {
            save1(row,index){
                if(this.tableData[index].Serial_number == 0)  //初次保存
                {
                    //每次保存需要更新数据库中的数据
                    let param = Object.assign({}, this.tableData[index]);
                    axios.post('/api/addData/', qs.stringify(param))
                        .then(res => {
                            console.log(param)
                            if (res.data.success) {
                                this.$message({
                                    type: 'info',
                                    message: res.data.msg,
                                });
                                row.show = false
                                this.tableData[index].Serial_number = res.data.id;
                            } else {
                                this.$message({
                                    type: 'info',
                                    message: res.data.msg,
                                });
                            }
                        });
                }
                else{   //非初次保存
                    let param = Object.assign({}, this.tableData[index]);
                    axios.post('/api/addData/', qs.stringify(param))
                        .then(res => {
                            console.log(param)
                            if (res.data.success) {
                                this.$message({
                                    type: 'info',
                                    message: res.data.msg,
                                });
                                row.show = false
                            } else {
                                this.$message({
                                    type: 'info',
                                    message: res.data.msg,
                                });
                            }
                        });
                }

            },
            handleAdd(){
                this.tableData.push({
                    Serial_number:0,
                    Product_category: '',
                    Product_name: '',
                    Address:'',
                    Customer_name: '',
                    Development_unit: '',
                    Customer_manager: '',
                    Opening_status: '',
                    Order_time: '',
                    Completion_time: '',
                    Quantity_ordered:'',
                    show:true
                    }
                )
                //this.tempIndex.push(0)
            },
            handleDelete(index){
                if(this.tableData[index].Serial_number == 0)
                {
                    this.tableData.splice(index,1)
                    this.$message({
                        type: 'info',
                        message: '删除成功',
                    });
                    //this.tempIndex.splice(index,1)
                }
                else
                {
                    let param = this.tableData[index].Serial_number;
                    axios.post('/api/delData/', qs.stringify(param))
                        .then(res => {
                            console.log(param)
                            if (res.data.success) {
                                this.tableData.splice(index,1)
                                this.$message({
                                    type: 'info',
                                    message: '删除成功',
                                });
                                this.tempIndex.splice(index,1)
                            } else {
                                this.$message({
                                    type: 'info',
                                    message: '删除失败',
                                });
                            }
                        });
                }
            },
            handleModfiy(row,index)
            {
                row.show =true
            },
            handleSizeChange(val) {
                // 改变每页显示的条数
                this.PageSize = val
                // 注意：在改变每页显示的条数时，要将页码显示到第一页
                this.currentPage = 1
            },

            // 显示第几页
            handleCurrentChange(val) {
                // 改变默认的页数
                this.currentPage = val
            },

            //设置表格内容居中
            cellStyle({row, column, rowIndex, columnIndex}) {
                return "text-align:center"
            },
            rowClass({row, rowIndex}) {
                return "text-align:center"
            }
        }
    }
</script>

<style scoped>
.el-main{
    align:center;
    text-align: center;
    line-height: 30px;
    width: 100%;
}
.el-pagination{
    align:center;
    text-align: center;
}
</style>
