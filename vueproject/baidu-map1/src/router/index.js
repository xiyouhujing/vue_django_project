import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)



const router = new VueRouter({
  routes:[
    {
      path:'/',
      redirect:'login'
    },
    {
      path:'/login',
      name:'login',
      component:()=>import('@/views/Login.vue')
    },
    {
      path:'/',
      component:() => import('@/views/Main.vue'),
      children:[
        {
          path:'/home',
          name:'home',
          component:()=>import('@/views/home/home')
        },
        {
          path:'/showmap',
          name:'showmap',
          component:()=>import('@/views/showmap/showmap')
        },
        {
          path:'/uploadfile',
          name:'uploadfile',
          component:()=>import('@/views/uploadfile/uploadfile')
        },
        {
          path:'/showdata',
          name:'uploadfile',
          component:()=>import('@/views/uploadfile/uploadfile')
        }
      ]
    }
  ],
  mode:"history"
})

export default router
