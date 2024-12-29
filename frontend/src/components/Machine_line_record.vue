<template>
    <div class="machine-page">
      <!-- 功能名稱 -->
      <div class="func-title">填寫日報</div>
      <hr>
      <div class="func_btn">
        <button v-if="raw" @click="handle_save_btn" class="btn-style" id="save_btn">儲存</button>
        <button v-else @click="handle_update_btn" class="btn-style" id="update_btn">更新</button>
        <button @click="handle_query_btn" class="btn-style"id="query_btn">查詢機種</button>
      </div>
      <div class="field-block">
        <span class="red" v-if="raw">
          資料庫中目前還未有{{production_day}}的資料
        </span>
        <span class="green" v-else>
          資料庫中已存在 {{production_day}} 資料，上次編輯時間: {{mdatetime}}
        </span>        
      </div>
      <!-- 機種設定輸入區 -->
      <div class="field-block machine">
        <div class="field">
          <span class="field-name">填寫日期</span>
          <span class="field-input">
            <input @change="handle_production_day" v-model="production_day" type="date" id="production_day" class="input-txt" >
          </span>
        </div>    
        <div class="field">
          <span class="field-name">機種名稱</span>
          <span class="field-input">
            <input v-model="data.machine_name" readonly type="text" id="machine_name" class="input-txt readonly" >
          </span>
        </div>
        <div class="field">
          <span class="field-name">連版數量</span>
          <span class="field-input">
            <input v-model="data.connecting_plate" readonly type="text" id="connecting_plate" class="input-txt readonly" >
          </span>
        </div>
        <div class="field">
          <span class="field-name">機種台數</span>
          <span class="field-input">
            <input v-model="data.machine_amt" readonly type="text" id="machine_amt" class="input-txt readonly" >
          </span>
        </div>
      </div>
  
      <!-- 表格區域 -->
      <div class="table-block machine-line">
        <div class="table-btn">
        </div>
        <div class="table-container">
          <table id="machine_line_table">
            <thead>
              <tr>
                <th class="table-title wide">線名</th>
                <th class="table-title">數量</th>
                <th class="table-title">員工數</th>
                <th class="table-title">工時</th>
                <th class="table-title">總工時</th>
                <th class="table-title">架線</th>
                <th class="table-title">NG</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in data.machine_lines" :key="index">
                <td><input readonly v-model="row.machine_line_name" placeholder="線名" type="text"  class="table-input readonly"></td>
                <td><input @keyup="checkIsInteger(row.machine_line_amt,index,'數量','machine_line_amt')" v-model="row.machine_line_amt" placeholder="數量" type="text"  class="table-input"></td>
                <td><input @keyup="checkIsInteger(row.emp_amt,index,'員工數','emp_amt')" v-model="row.emp_amt" placeholder="員工數" type="text"  class="table-input"></td>
                <td><input @keyup="checkIsInteger(row.work_hours,index,'工時','work_hours')" v-model="row.work_hours" placeholder="工時" type="text"  class="table-input"></td>
                <td><input readonly v-model="row.tot_work_hours" placeholder="總工時" type="text"  class="table-input"></td>
                 <td>
                  <select @change="overhead_wire_change($event,index)" v-model="row.overhead_wire">
                    <option v-for="option in overhead_wire_options" :value="option.value">
                      {{ option.text }}
                    </option>
                  </select>
                 </td>
                <td><input v-model="row.ng"  type="text"  class="table-input"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <modal :msg="msg" :dynamicStatusClass :successFlag="successFlag" ref="msgModal"></modal>

    <QueryModal @query2backend4data="query2backend4data" :q_result="q_result" @query2backend="queryByMachineName" :queryFields="queryFields" @qModalMounted="handleQModalMounted"  ref="qModal"></QueryModal>
</template>

<script>
export default {
        name:"Machine_line_record"
    }
</script>

<script setup>
import { ref,computed,watch  } from 'vue';
import QueryModal from './QueryModal.vue';
import axios from 'axios';
import modal from './modal.vue';
import useUtils from '@/hooks/useUtils';

let rows = ref([])
const qModal = ref(null);
let data = ref({})
let msgModal = ref(null);
let msg = ref("");
let raw = ref(true); // 若是既有已在資料庫中的資料 => false , 若是還未有任何紀錄在DB => true 
let dynamicStatusClass = ref("fail");
let successFlag = ref(false);
let mdatetime = ref(null)
let [isInteger] = useUtils()

let overhead_wire_options = ref(
  [
    { text: '上料', value: '1' },
    { text: '下料', value: '2' },
  ]
)

const selected = ref('')

// 關鍵字返回的選項結果，會傳至子組件QueryModal
let q_result = ref([])

// 定義查詢欄位與其表現形態，會傳給子組件 QueryModal來呈現
let queryFields = ref([
  {
    "field":"machine_name",
    "field_name": "機器名稱",
    "input_type": "text",
    "unique": true,
    "field_value":""
  },

])

function getLastWorkDay() {
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0: Sunday, 1: Monday, ..., 6: Saturday
    const result = new Date(today); // 複製當前日期

    if (dayOfWeek === 1) {
        // 如果今天是星期一，往回推三天到上星期五
        result.setDate(result.getDate() - 3);
    } else if (dayOfWeek === 0 || dayOfWeek === 6) {
        // 如果今天是星期六或星期日，往回推到最近的星期五
        result.setDate(result.getDate() - (dayOfWeek === 6 ? 1 : 2));
    } else {
        // 其餘情況，往回推一天
        result.setDate(result.getDate() - 1);
    }

    // 格式化為 YYYY-MM-DD
    const year = result.getFullYear();
    const month = String(result.getMonth() + 1).padStart(2, '0');
    const day = String(result.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

function handleQModalMounted() {
  qModal.value.myModal_show()
}

async function queryByMachineName(field_infos) {

  let field_value = field_infos.field_value
  let query_key = field_infos['field']

  try {
    // let response = await axios.get("http://127.0.0.1:8000/machine/", { params: { [query_key]:field_value } });
    let response = await axios.get("http://192.168.0.183:8000/machine/", { params: { [query_key]:field_value } });
    let res_data = response.data

    let tmp_result = []
    for (let i = 0; i < res_data.length;i++) { 
      let row = res_data[i]
      tmp_result.push(
        {
          "id": row.machine_id,
          "name":row.machine_name
        }
      )
    }
    q_result.value = tmp_result
  }
  catch (error) { 
    console.log("error:"+error)
  }
}

async function query_daily_record(machine_id) { 
  
  try {
    let response = await axios.get(`http://192.168.0.183:8000/machine_daily_record/${machine_id}`,{
    params: { production_day: production_day.value }
    
    })
    data.value = response.data.result
    raw.value = response.data.raw
    mdatetime.value = response.data.mdatetime
    
  } catch (error) {
    
  }
}

async function query2backend4data(machine_obj) {
  qModal.value.myModal_hide();
  let machine_id = machine_obj.id
  query_daily_record(machine_id)
}


watch(
  () => data.value.machine_lines,
  (newLines) => {
    console.log("newLines->")
    console.log(newLines);
    
    newLines.forEach(line => {
      line.tot_work_hours = line.emp_amt * line.work_hours;
    });
  },
  { deep: true } // 深層監聽，確保監聽到子屬性的變化
);

let production_day = ref(getLastWorkDay())

function overhead_wire_change(event,index) {
  data.value.machine_lines[index].overhead_wire = event.target.value
}

function handle_query_btn() {
  queryFields.value.forEach(field => {
  field.field_value = '';  // 清空每個欄位的 field_value
  });

  qModal.value.myModal_show()
}

async function handle_save_btn() {
  
  try {
    let machine_id = data.value.machine_id
    let payload = []
    let row = null
    for (let i = 0; i < data.value.machine_lines.length; i++) { 
      row = data.value.machine_lines[i];
      row['machine_id'] = machine_id
      row['machine_line_amt'] *= 1
      row['emp_amt'] *= 1
      row['work_hours']*=1
      const { tot_work_hours, ...newRow } = row; 
      payload.push(newRow)
    }
    let response = await axios.post("http://192.168.0.183:8000/machine_daily_record/", payload);
    if (response.status == 201) { 
      dynamicStatusClass.value = "success"
      successFlag.value = true;
      data.value = response.data.result
      raw.value = response.data.raw
      msg.value = response.data.msg
      mdatetime.value = response.data.mdatetime
    }
    msgModal.value.myModal_show()
    await new Promise(resolve => setTimeout(resolve, 1500));
    msgModal.value.myModal_hide()

  } catch (error) {
    console.log("error happened:"+error);
    msg.value = "錯誤"
    msgModal.value.myModal_show()    
  }

  
}


async function handle_update_btn() {
  let modal_status = null
  try {
    let machine_id = data.value.machine_id
    let payload = []
    let row = null
    for (let i = 0; i < data.value.machine_lines.length; i++) { 
      row = data.value.machine_lines[i];
      row['machine_id'] = machine_id
      row['machine_line_amt'] *= 1
      row['emp_amt'] *= 1
      row['work_hours']*=1
      const { tot_work_hours, ...newRow } = row; 
      payload.push(newRow)
    }

    let response = await axios.put("http://192.168.0.183:8000/machine_daily_record/", payload);
    
    
    if (response.status == 200) {
      data.value = response.data.result
      dynamicStatusClass.value = "success"
      mdatetime.value = response.data.mdatetime
      successFlag.value = true;
    }

    msg.value = response.data.msg
    msgModal.value.myModal_show()
    await new Promise(resolve => setTimeout(resolve, 1500));
    msgModal.value.myModal_hide()
  } catch (error) {
    console.log("error happened:"+error);
    msg.value = "錯誤"
    msgModal.value.myModal_show()    
  }
}


function handle_production_day() {
  if (production_day.value) { 
    let machine_id = data.value.machine_id
    query_daily_record(machine_id)
  }
  
}

function checkIsInteger(test_str,raw,field_name,field) {
  if (!isInteger(test_str)) { 
    if (test_str) { 
      data.value.machine_lines[raw][field] = ''
      msg.value = `第${raw+1}列 ${field_name} 僅能輸入整數`
      msgModal.value.myModal_show()
    }
  }
}

</script>



<style scoped>
.red{
  color: red;
}

.green{
  color: rgb(0, 177, 124);
}
  /* 頁面基本樣式 */
  .machine-page {
    padding: 20px;
    font-family: Arial, sans-serif;
    color: #333;
    background-color: #ecf0f1;
  }
  
  /* 標題樣式 */
  .func-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: #2c3e50;
  }
  
  /* 輸入區樣式 */
  .field-block {
    margin-bottom: 20px;
  }
  
  .field {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .field-name {
    /* flex: 1; */
    font-weight: bold;
    color: #34495e;
  }

  span.field-name{
    width: 100px;
  }
  
  .field-input {
    flex: 2;
  }
  
  .input-txt {
    width: 100%;
    padding: 8px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 1rem;
    color: #333;
    background-color: #fff;
    transition: border 0.3s ease;
  }
  
  .input-txt:focus {
    border-color: #3498db;
    outline: none;
  }
  
  /* 表格區域樣式 */
  .table-block {
    margin-top: 20px;
  }
  
  .table-btn {
    margin-bottom: 10px;
  }
  
  .btn-style {
    padding: 10px 20px;
    font-size: 1rem;
    color: #fff;
    background-color: #3498db;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
    transition: background 0.3s ease;
  }
  
  .btn-style:hover {
    background-color: #2980b9;
  }
  
  /* 表格樣式 */
  .table-container {
    overflow-y: auto;
    max-height: 300px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: #fff;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }
  
  thead tr {
    background-color: #34495e;
    color: #fff;
  }
  
  .table-title {
    padding: 10px;
    font-weight: bold;
  }
  
  .table-title.narrow {
    width: 50px;
    text-align: center;
  }
  
  .table-title.wide {
    width: 200px;
  }
  
  tbody tr:nth-child(odd) {
    background-color: #f9f9f9;
  }
  
  tbody tr:nth-child(even) {
    background-color: #ecf0f1;
  }
  
  tbody tr:hover {
    background-color: #dff9fb;
  }
  
  .table-input {
    width: 90%;
    padding: 5px;
    margin: 10px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: #fff;
  }

  table {
  text-align: left;
  position: relative;
}

th {
  position: sticky;
  background-color: #34495e;
  top: 0;
}

.func_btn{
    margin: 15px 0 15px 0px;
}

#save_btn{
    background-color: rgba(5, 175, 81, 0.842);
}

#save_btn:hover{
    background-color: rgba(15, 111, 58, 0.842);
}

#query_btn{
    background-color: rgba(175, 135, 5, 0.842);
}

#query_btn:hover{
    background-color: rgba(107, 83, 2, 0.842);
}

#del_btn{
    background-color: rgba(209, 4, 4, 0.842);
}

#del_btn:hover{
    background-color: rgba(144, 1, 1, 0.842);
}

.func_btn > button{
    margin: 0px 20px 0px 0px
}

div.span_row{
  display: inline-block;
  margin-left: 10px;
}

div.table_checkbox{
  display: inline-block;
  margin-left: 10px;
}

.readonly{
  background-color: rgb(224, 224, 224);
}

</style>
  