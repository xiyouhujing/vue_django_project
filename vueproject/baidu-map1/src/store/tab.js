export default {
    state: {
        isCollapse:false,
        menu:[],
        currentMenu:null
    },
    mutations: {
        selectMenu(state,val){
            if(val.name !== 'home'){
                state.currentMenu = val;
            }
            else{
                state.currentMenu = null;
            }

        },
        collapseMenu(state){
            state.isCollapse = !state.isCollapse;
        }
    },
    actions: {
    }
}