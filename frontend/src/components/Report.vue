<template>
    <h1>報表</h1>
    
    <!-- <apexchart width="500" type="bar" :options="options" :series="series"></apexchart> -->
    <Machine_line_summary></Machine_line_summary>
</template>


<script>
import Machine_line_summary from './stat/Machine_line_summary.vue';

export default {
    name: "Report",
    components: {
        Machine_line_summary
    }
    }
</script>

<script setup>
import axios from 'axios';
import {  ref } from 'vue';

// const series = [{
//     name: 'series-1',
//     data: [30, 40, 45, 50, 49, 60, 70, 91]
// }]

// const options = {
//     chart: {
//         id: 'vuechart-example'
//     },
//     xaxis: {
//         categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
//     }
// }









</script>

<style scoped>

</style>
