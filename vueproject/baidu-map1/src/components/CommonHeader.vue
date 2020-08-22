<template>
    <header>
        <div class = "l-content">
            <el-button plain icon="el-icon-menu" size="mini" @click="collapseMenu"></el-button>
            <el-breadcrumb separator="/">
                <!--<el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item :to="current.path" v-if = "current && flag">
                    {{current.label}}
                </el-breadcrumb-item>-->
                <el-breadcrumb-item >首页</el-breadcrumb-item>
                <el-breadcrumb-item  v-if = "current && flag">
                    {{current.label}}
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class = "r-content">
            <h3>湖北联通网络平台</h3>
        </div>

    </header>
</template>

<script>
    import {mapState} from 'vuex'
    export default {
        data(){
            return{
                levelList:[],
                flag:true
            }
        },
        computed:{
            ...mapState({
                current:state=>state.tab.currentMenu
            })
        },
        watch: {
            $route(to,from){
                let matched = this.$route.matched.filter(item => item.name)  // this.$route.matched 可以获取到一个数组，包含当前路由的所有嵌套路径片段的路由记录
                const first = matched[0]
                if(first.name === 'home')
                    this.flag = false
                else
                    this.flag = true
            }
        },
        methods:{
            collapseMenu(){
                this.$store.commit('collapseMenu');
            }
        }
    }
</script>

<style lang="scss" scoped="">
    header{
        display: flex;
        height: 100%;
        align-items: center;
        justify-content: space-between;
        .el-button{
            margin-right: 20px;
        }
        h3{
            color: #f4f4f4;
            line-height: 48px;
        }
        .l-content{
            display: flex;
            align-items: center;
        }
    }

</style>

<style lang="scss">
    .el-breadcrumb__item{
        .el-breadcrumb__inner{
            color:#fff;
        }
        &:last-child{
            .el-breadcrumb__inner {
                color: #f4f4f4;
            }
        }
    }
</style>