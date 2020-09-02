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
            <!--            <el-table-column prop="movieId" label="ID"></el-table-column>-->
            <el-table-column prop="movieName" label="电影名称"></el-table-column>
            <el-table-column prop="directors" label="导演"></el-table-column>
            <el-table-column prop="releaseInfo" label="上映天数"></el-table-column>
            <el-table-column prop="boxInfo" label="当日票房"></el-table-column>
            <el-table-column prop="sumBoxInfo" label="总票房"></el-table-column>
            <el-table-column prop="boxRate" label="票房占比"></el-table-column>
            <el-table-column prop="showInfo" label="排片场次"></el-table-column>
            <el-table-column prop="showRate" label="排片占比"></el-table-column>
            <el-table-column prop="createtime" label="日期"></el-table-column>
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
