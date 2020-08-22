module.exports={
    // 输出目录
    assetsDir: 'static',
    devServer:{
        port:8080,
        open:true,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/api/',  // target host
                ws: true,  // proxy websockets
                changeOrigin: true,  // needed for virtual hosted sites
                pathRewrite: {
                    '^/api': ''  // rewrite path
                }
            },
        }
    },
    css:{
        loaderOptions:{
            sass:{
                prependData:'@import "./src/assets/scss/_variabale.scss";'
            }
        }
    }
}
