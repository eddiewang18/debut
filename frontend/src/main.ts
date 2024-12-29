import { createApp } from 'vue'
import App from './App.vue'
import router from './router/route'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "bootstrap-icons/font/bootstrap-icons.css"
// 引入FontAwesome核心
import { library } from '@fortawesome/fontawesome-svg-core'
// 引入FontAwesome组件
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// 引入你需要的图标
import { faCircleCheck } from '@fortawesome/free-solid-svg-icons'
import { faCircleXmark } from '@fortawesome/free-solid-svg-icons'
import VueApexCharts from "vue3-apexcharts";


library.add(faCircleCheck)
library.add(faCircleXmark)

const app = createApp(App)
app.use(router)
app.use(VueApexCharts);
// 注册FontAwesome组件
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
