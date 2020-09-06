<template>
    <div>
        <el-table
                :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)"
                :cell-style="cellStyle"
                :header-cell-style="rowClass"
                align="center"
                tooltip-effect="dark"
                :row-style="{height:'90px'}"
                style="width: 90%;margin:auto auto">
            <el-table-column prop="Product_category" label="产品类别"></el-table-column>
            <el-table-column prop="Product_name" label="产品名称"></el-table-column>
            <el-table-column prop="Address" label="地址"></el-table-column>
            <el-table-column prop="Customer_name" label="客户名称"></el-table-column>
            <el-table-column prop="Development_unit" label="发展营服"></el-table-column>
            <el-table-column prop="Customer_manager" label="客户经理"></el-table-column>
            <el-table-column prop="Opening_status" label="完工状态"></el-table-column>
            <el-table-column prop="Order_time" label="订单日期"></el-table-column>
            <el-table-column prop="Completion_time" label="完工日期"></el-table-column>
            <el-table-column prop="Quantity_ordered" label="订单数量"></el-table-column>
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
</template>

<script>
    export default {
        data() {
            return {
                tableData: [],
                // 默认显示第一条
                currentPage: 1,
                PageSize: 10,
            }
        },
        mounted() {
            this.getDate();
        },
        methods: {
            getDate() {
                axios.post('http://localhost:8090//movie/movielist').then(res => {
                    console.log(res)
                    this.tableData = res.data;
                    this.currentPage = 1;
                }, error => {
                    console.log(error)
                })
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
