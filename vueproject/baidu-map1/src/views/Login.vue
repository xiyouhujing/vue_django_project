<template>
    <div class="login_container">
        <vue-particles
                color="#fff"
                :particleOpacity="0.7"
                :particlesNumber="60"
                shapeType="circle"
                :particleSize="4"
                linesColor="#fff"
                :linesWidth="1"
                :lineLinked="true"
                :lineOpacity="0.4"
                :linesDistance="150"
                :moveSpeed="2"
                :hoverEffect="true"
                hoverMode="grab"
                :clickEffect="true"
                clickMode="push"
                class="lizi"
        >
        </vue-particles>
        <el-form :model="form" ref="form" label-width="60" >
            <h2 style="color: #505458" align="center">湖北联通网络平台</h2>
            <el-form-item align="center">
                <el-col >
                    <el-input type="text"
                              v-model="form.username"
                              placeholder="请输入用户名"
                              auto-complete="off">
                     <i slot="prefix" class = "el-icon-user"></i>
                    </el-input>
                </el-col>
            </el-form-item>
            <el-form-item>
                <el-col>
                    <el-input type="text"
                              v-model="form.password"
                              @keyup.enter.native="login"
                              placeholder="请输入密码"
                              style="align-items: center"
                              show-password = false
                              auto-complete="off">
                        <i slot="prefix" class = "el-icon-lock"></i>
                    </el-input>
                </el-col>
            </el-form-item>
            <el-form-item align="center">
                <el-button type="primary" @click="login('form')">登录</el-button>
            </el-form-item>
        </el-form>
    </div>
    <!--<div style="padding:20px">
    </div>-->
</template>

<script>
    import axios from 'axios';
    import qs from 'qs';
    export default {
        data(){
            return{
                form:{
                    username:'',
                    password:''
                }
            }
        },
        methods:{
            login(formName){
                // 检查是否拿到了正确的需要验证的form
                this.$refs[formName].validate((valid) =>{
                    if (valid){
                        const _this = this
                        // 进行post 请求体的封装 在上面提到过
                        var data = qs.stringify({"username":this.form.username,"password":this.form.password})
                        // axios 发送请求
                        axios.post('/api/login/',data).then(
                            function (resp) {
                                const flag = resp.data.request['flag']
                                if (flag == 'yes'){
                                    // console.log(resp.data.request['flag'])
                                    // 请求成功后进行跳转 由于this 指向问题 加上了_this
                                    _this.$router.push({name:'home'})
                                }else {
                                    alert("错误登录")
                                }
                            }
                        )
                        // 开始用的 axios 发送请求
                        // console.log(this.ruleForm)
                    }else {
                        alert("验证错误")
                    }
                })
                // this.$router.push({name:'home'})
            }
        }
    }
</script>

<style lang="scss" scoped>
    .el-form {
        width: 15%;
        margin: auto;
        padding-top: 120px;
        /*background-color: #fab6b6;*/
        position: relative;
    }
    .login_container {
        background-image: linear-gradient(-180deg, #ccc 0%, #000 100%);
        /*background-image: linear-gradient(-180deg, #c0c0c0 0%, #0e81a5 100%);*/
        /*background-image: url("../images/bg_login.png");*/
        background-repeat: no-repeat;
        background-size: cover;
        height: 100%;
    }
    #particles-js{
        width:100%;
        height: calc(100% - 100px);
        position: absolute;
    }
</style>
