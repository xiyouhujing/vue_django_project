<template>
    <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            :collapse="isCollapse">
        <el-menu-item :index="item.path" v-for = "item in asideMenu" :key = "item.path" @click="clickMenu(item)">
            <i :class="'el-icon-'+item.icon"></i>
            <span slot="title">{{item.label}}</span>
        </el-menu-item>
    </el-menu>
</template>

<script>
    export default {

        computed:{
            noChildren(){
                return this.asideMenu.filter(item => !item.children);
            },
            hasChildren(){
                return this.asideMenu.filter(item => item.children);
            },
            isCollapse(){
                return this.$store.state.tab.isCollapse;
            }

        },
        data(){
            return{
                asideMenu:[
                    {
                        path:'/',
                        name:'home',
                        label:'首页',
                        icon:'s-home'
                    },
                    {
                        path:'/showmap',
                        name:'showmap',
                        label: '地图展示',
                        icon:'s-promotion'
                    },
                    {
                        path:'/uploadfile',
                        name:'uploadfile',
                        label:'上传文件',
                        icon:"upload"
                    },
                    {
                        path:'/tableshow',
                        name:'tableshow',
                        label:'数据展示',
                        icon:"s-grid"
                    }
                ]
            }
        },
        methods:{
            clickMenu(item){
                this.$router.push({name:item.name});
                this.$store.commit('selectMenu',item);
            }
        }
    }
</script>

<style lang="scss" scoped="">
    .el-menu{
        height: 100%;
        border: none;
    }
    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }
</style>
