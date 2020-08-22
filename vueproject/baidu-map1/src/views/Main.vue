<template>
    <el-container style="height: 100%" margin="auto">
        <el-aside width="auto"><common-aside></common-aside></el-aside>
        <el-container>
            <el-header><common-header></common-header></el-header>
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import CommonHeader from '../components/CommonHeader'
import CommonAside from '../components/CommonAside'
export default {
    components:{
        CommonHeader,
        CommonAside
    }
}
</script>

<style lang="scss"  scoped>
    .el-header{
        background: black;
    }
    .el-main{
        padding: 20px;
    }

</style>