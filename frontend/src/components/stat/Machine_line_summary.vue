<template>
    <div class="important1">整體機種統計數據</div>
    <div class="important2">基本統計量</div>
    <apexchart height="150" width="500" type="bar" :options="options" :series="machine_line_amt_series"></apexchart>
    <apexchart height="150" width="500" type="bar" :options="options" :series="emp_amt_series"></apexchart>
    <apexchart height="150" width="500" type="bar" :options="options" :series="tot_work_hours_series"></apexchart>
    <hr>
    <div class="important2">機種與整體統計量比較</div>

    <div class="scroll-container">
        <apexchart  ref="chartRef1" height="300" width="1200" type="bar" :options="options1" :series="machine_line_amt_series1"></apexchart>
        <apexchart  ref="chartRef2" height="300" width="1200" type="bar" :options="options2" :series="emp_amt_series1"></apexchart>
        <apexchart  ref="chartRef3" height="300" width="1200" type="bar" :options="options3" :series="tot_work_hours_series1"></apexchart>
    </div>

    <hr>

</template>

<script>
export default {
        name:"Machine_line_summary",
    }
</script>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { nextTick } from 'vue';

const options = {
    chart:{
        type: 'bar'
    },
    plotOptions: {
        bar: {
            horizontal: true
        }
    }
}

const stat1 = ref([])

let machine_line_amt_avg = ref(0)
let machine_line_amt_median = ref(0)
let machine_line_amt_std = ref(0)

let emp_amt_avg = ref(0)
let emp_amt_median = ref(0)
let emp_amt_std = ref(0)

let tot_work_hours_avg = ref(0)
let tot_work_hours_median = ref(0)
let tot_work_hours_std = ref(0)

const machine_line_amt_series = ref(
    [
        {
            data: []
        }
    ]
) 
const emp_amt_series = ref(
    [
        {
            data: []
        }
    ]
) 
const tot_work_hours_series = ref(
    [
        {
            data: []
        }
    ]
) 

let machine_stat1 = ref({})

// 請求取得 machine_line_amt數據
async function get_machine_stat1() {
    try {
        let response = await axios.get("http://192.168.0.183:8000/machine_stat1");
        machine_stat1.value = response.data
        console.log("get machine_stat1 result:");
        console.log(response.data);

        machine_line_amt_series.value[0]["data"] = response.data['machine_line_amt']

        machine_line_amt_avg.value = response.data['machine_line_amt'][0]['y']
        machine_line_amt_median.value = response.data['machine_line_amt'][1]['y']
        machine_line_amt_std.value = response.data['machine_line_amt'][2]['y']

        emp_amt_series.value[0]["data"] = response.data['emp_amt']

        emp_amt_avg.value = response.data['emp_amt'][0]['y']
        emp_amt_median.value = response.data['emp_amt'][1]['y']
        emp_amt_std.value = response.data['emp_amt'][2]['y']

        tot_work_hours_series.value[0]["data"] = response.data['tot_work_hours']

        tot_work_hours_avg.value = response.data['tot_work_hours'][0]['y']
        tot_work_hours_median.value = response.data['tot_work_hours'][1]['y']
        tot_work_hours_std.value = response.data['tot_work_hours'][2]['y']        

        
    } catch (error) {
        console.log("Error happened when call get_machine_line_amt api =>"+error)
    }
}
////////////////////////////////////////////////////////////////////////////////////

const chartRef1 = ref(null);

const select1Refs = ref([])

let options1 = ref({
    chart: {
          height: 350,
          type: 'line',
          stacked: false
        },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [2,2,2,3,3,3]
    },
    title: {
        text: '機種分析',
        align: 'left',
        offsetX: 0
    },
    xaxis: {
        categories: [],
    },
    yaxis: [
        {
        seriesName: 'Income',
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#008FFB'
        },
        labels: {
            style: {
            colors: '#008FFB',
            }
        },
        title: {
            text: "",
            style: {
            color: '#008FFB',
            }
        },
        tooltip: {
            enabled: true
        }
        },
        {
        seriesName: 'Cashflow',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#00E396'
        },
        labels: {
            style: {
            colors: '#00E396',
            }
        },
        title: {
            text: "",
            style: {
            color: '#00E396',
            }
        },
        },
        {
        seriesName: 'Revenue',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#FEB019'
        },
        labels: {
            style: {
            colors: '#FEB019',
            },
        },
        title: {
            text: "",
            style: {
            color: '#FEB019',
            }
        }
        },
    ],
    tooltip: {
        fixed: {
        enabled: true,
        position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
        offsetY: 30,
        offsetX: 60
        },
    },
    legend: {
        horizontalAlign: 'left',
        offsetX: 40
    },

}
) 

const machine_line_amt_series1 = ref([
    {
        name: '平均數',
        type: 'column',
        data: []
    },
    {
        name: '中位數',
        type: 'column',
        data: []
    },
    {
        name: '標準差',
        type: 'column',
        data: []
    },
    {
        name: '整體平均數',
        type: 'line',
        data: []
    },
    {
        name: '整體中位數',
        type: 'line',
        data: []
    },    
    {
        name: '整體標準差',
        type: 'line',
        data: []
    }, 
])
////////////////////////////////////////////////////////////////////////////////////

const chartRef2 = ref(null);

let options2 = ref({
    chart: {
          height: 350,
          type: 'line',
          stacked: false
        },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [2,2,2,3,3,3]
    },
    title: {
        text: '員工數量分析',
        align: 'left',
        offsetX: 0
    },
    xaxis: {
        categories: [],
    },
    yaxis: [
        {
        seriesName: '',
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#008FFB'
        },
        labels: {
            style: {
            colors: '#008FFB',
            }
        },
        title: {
            text: "",
            style: {
            color: '#008FFB',
            }
        },
        tooltip: {
            enabled: true
        }
        },
        {
        seriesName: '',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#00E396'
        },
        labels: {
            style: {
            colors: '#00E396',
            }
        },
        title: {
            text: "",
            style: {
            color: '#00E396',
            }
        },
        },
        {
        seriesName: '',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#FEB019'
        },
        labels: {
            style: {
            colors: '#FEB019',
            },
        },
        title: {
            text: "",
            style: {
            color: '#FEB019',
            }
        }
        },
    ],
    tooltip: {
        fixed: {
        enabled: true,
        position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
        offsetY: 30,
        offsetX: 60
        },
    },
    legend: {
        horizontalAlign: 'left',
        offsetX: 40
    },

}
) 

const emp_amt_series1 = ref([
    {
        name: '平均數',
        type: 'column',
        data: []
    },
    {
        name: '中位數',
        type: 'column',
        data: []
    },
    {
        name: '標準差',
        type: 'column',
        data: []
    },
    {
        name: '整體平均數',
        type: 'line',
        data: []
    },
    {
        name: '整體中位數',
        type: 'line',
        data: []
    },    
    {
        name: '整體標準差',
        type: 'line',
        data: []
    }, 
])

////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////

const chartRef3 = ref(null);

let options3 = ref({
    chart: {
          height: 350,
          type: 'line',
          stacked: false
        },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: [2,2,2,3,3,3]
    },
    title: {
        text: '總工時分析',
        align: 'left',
        offsetX: 0
    },
    xaxis: {
        categories: [],
    },
    yaxis: [
        {
        seriesName: '',
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#008FFB'
        },
        labels: {
            style: {
            colors: '#008FFB',
            }
        },
        title: {
            text: "",
            style: {
            color: '#008FFB',
            }
        },
        tooltip: {
            enabled: true
        }
        },
        {
        seriesName: '',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#00E396'
        },
        labels: {
            style: {
            colors: '#00E396',
            }
        },
        title: {
            text: "",
            style: {
            color: '#00E396',
            }
        },
        },
        {
        seriesName: '',
        opposite: true,
        axisTicks: {
            show: true,
        },
        axisBorder: {
            show: true,
            color: '#FEB019'
        },
        labels: {
            style: {
            colors: '#FEB019',
            },
        },
        title: {
            text: "",
            style: {
            color: '#FEB019',
            }
        }
        },
    ],
    tooltip: {
        fixed: {
        enabled: true,
        position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
        offsetY: 30,
        offsetX: 60
        },
    },
    legend: {
        horizontalAlign: 'left',
        offsetX: 40
    },

}
) 

const tot_work_hours_series1 = ref([
    {
        name: '平均數',
        type: 'column',
        data: []
    },
    {
        name: '中位數',
        type: 'column',
        data: []
    },
    {
        name: '標準差',
        type: 'column',
        data: []
    },
    {
        name: '整體平均數',
        type: 'line',
        data: []
    },
    {
        name: '整體中位數',
        type: 'line',
        data: []
    },    
    {
        name: '整體標準差',
        type: 'line',
        data: []
    }, 
])

////////////////////////////////////////////////////////////////////////////////////

let machine_stat2 = ref({})

async function get_machine_stat2() {
    try {
        let response = await axios.get("http://192.168.0.183:8000/machine_stat2");
        machine_stat2.value = response.data
        console.log("get machine_stat2 result:");
        console.log(response.data);
        let result = response.data;
        let ary_len = result['categories'].length
        
        options1.value.xaxis.categories = result['categories']
        options2.value.xaxis.categories = result['categories']
        options3.value.xaxis.categories = result['categories']

        machine_line_amt_series1.value[0]["data"] = result['machine_line_amt']['avg']
        machine_line_amt_series1.value[1]["data"] = result['machine_line_amt']['median']
        machine_line_amt_series1.value[2]["data"] = result['machine_line_amt']['std']

        emp_amt_series1.value[0]["data"] = result['emp_amt']['avg']
        emp_amt_series1.value[1]["data"] = result['emp_amt']['median']
        emp_amt_series1.value[2]["data"] = result['emp_amt']['std']

        tot_work_hours_series1.value[0]["data"] = result['tot_work_hours']['avg']
        tot_work_hours_series1.value[1]["data"] = result['tot_work_hours']['median']
        tot_work_hours_series1.value[2]["data"] = result['tot_work_hours']['std']
        
        machine_line_amt_series1.value[3]["data"] = Array(ary_len).fill(machine_line_amt_avg.value);
        machine_line_amt_series1.value[4]["data"] = Array(ary_len).fill(machine_line_amt_median.value);
        machine_line_amt_series1.value[5]["data"] = Array(ary_len).fill(machine_line_amt_std.value);

        emp_amt_series1.value[3]["data"] = Array(ary_len).fill(emp_amt_avg.value);
        emp_amt_series1.value[4]["data"] = Array(ary_len).fill(emp_amt_median.value);
        emp_amt_series1.value[5]["data"] = Array(ary_len).fill(emp_amt_std.value);

        tot_work_hours_series1.value[3]["data"] = Array(ary_len).fill(tot_work_hours_avg.value);
        tot_work_hours_series1.value[4]["data"] = Array(ary_len).fill(tot_work_hours_median.value);
        tot_work_hours_series1.value[5]["data"] = Array(ary_len).fill(tot_work_hours_std.value);

        // 強制 ApexCharts 重新渲染
        await nextTick(); // 確保 DOM 已更新
        chartRef1.value.updateOptions({
            xaxis: {
                categories: result['categories']
            }
        }, false, true); // 第二個參數表示是否重繪，第三個參數表示是否動畫


        chartRef2.value.updateOptions({
            xaxis: {
                categories: result['categories']
            }
        }, false, true); // 第二個參數表示是否重繪，第三個參數表示是否動畫

        chartRef3.value.updateOptions({
            xaxis: {
                categories: result['categories']
            }
        }, false, true); // 第二個參數表示是否重繪，第三個參數表示是否動畫    
        
        
    } catch (error) {
        console.log("Error happened when call get_machine_line_amt api =>"+error)
    }
}

get_machine_stat1()
get_machine_stat2()

</script>

<style scoped>
    .important1{
        font-size: 20px;
        font-weight: 600;
    }

    .important2{
        font-size: 16px;
        font-weight: 600;
        margin: 10px;
    }

    .grp-checkbox{
        border: 1px solid black;
        padding: 4px;
        font-size: 14px;
        cursor: pointer;
        display: inline-block;
        margin-bottom: 12px;
    }

    .selected{
        background-color: cadetblue;
        color: white;

    }

    .scroll-container {
        width: 1200px; /* 容器的寬度 */
        overflow-x: auto; /* 啟用橫向卷軸 */
        white-space: nowrap; /* 防止內容換行 */
        border: 1px solid #ccc; /* 加上邊框方便查看 */
        padding: 10px;
    }

</style>