<template>
    <div class="machine-page">
      <!-- 功能名稱 -->
      <div class="func-title">機種設定</div>
      <hr>
      <div class="func_btn">
        <button @click="save" class="btn-style" id="save_btn">儲存/更新</button>
        <button @click="queryBtn" class="btn-style"id="query_btn">查詢機種</button>
        <button @click="del_btn" v-if="delShow" class="btn-style"id="del_btn">刪除機種</button>
        <button @click="refresh" class="btn-style" id="insert_mode_btn">設定新機種</button>
      </div>
      <!-- 機種設定輸入區 -->
      <div class="field-block machine">
        <div class="field">
          <span class="field-name">機種名稱</span>
          <span class="field-input">
            <input v-model="machine.machine_name" type="text" id="machine_name" class="input-txt" placeholder="輸入機種名稱">
          </span>
        </div>
        <div class="field">
          <span class="field-name">連版數量</span>
          <span class="field-input">
            <input v-model="machine.connecting_plate"  type="text" id="connecting_plate" class="input-txt" placeholder="輸入連版數量">
          </span>
        </div>
        <div class="field">
          <span class="field-name">機種台數</span>
          <span class="field-input">
            <input  v-model="machine.machine_amt" type="text" id="machine_amt" class="input-txt" placeholder="輸入機種台數">
          </span>
        </div>
      </div>
  
      <!-- 表格區域 -->
      <div class="table-block machine-line">
        <div class="table-btn">
          <button class="btn-style" @click="addRow">新增資料列</button>
          <button class="btn-style" @click="delRow">刪除資料列</button>
        </div>
        <div class="table-container">
          <table id="machine_line_table">
            <thead>
              <tr>
                <th class="table-title narrow"><input v-model="selectAllVal" type="checkbox" @change="toggleSelectAll"></th>
                <th class="table-title wide">線名</th>
                <th class="table-title">員工數</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in rows" :key="index">
                <td><div class="table_checkbox"><input @click="handleCheckBox($event,index)" type="checkbox" v-model="row.selected"></div><div class="span_row">{{ index+1 }}</div></td>
                <td><input placeholder="線名" type="text" v-model="row.machine_line_name" class="table-input"></td>
                <td><input placeholder="員工數" type="text" v-model="row.emp_default_amt" class="table-input"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <modal :msg="msg" :dynamicStatusClass :successFlag="successFlag" ref="msgModal"></modal>
    <QueryModal   @query2backend4data="query2backend4data"  @query2backend="queryByMachineName" @updateQueryField="updateQueryField" :q_result="q_result" :queryFields="queryFields" ref="qModal"></QueryModal>
    <ConfirmModal @sure="delMachine" ref="confirmModal" :message="confirmMsg"></ConfirmModal>
</template>

<script>
export default {
        name:"Machine"
    }
</script>

<script setup >
import { ref , watch} from "vue";
import useTable from "@/hooks/Machine/useTable";
import useSave from "@/hooks/Machine/useSave"
import useQuery from "@/hooks/Machine/useQuery";
import { useRouter } from 'vue-router';
import axios from "axios";
import modal from './modal.vue';
import QueryModal from "./QueryModal.vue";
import ConfirmModal from "./ConfirmModal.vue";
const router = useRouter();
const confirmModal = ref(null)
let confirmMsg = ref("確定要刪除該機種?")
// let msg = ref("");

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
// 關鍵字返回的選項結果，會傳至子組件QueryModal
let q_result = ref([])

let successFlag = ref(false);
let dynamicStatusClass = ref("fail");
let delShow = ref(false)
const qModal = ref(null);

let machine = ref({
    machine_id:null,
    machine_name: "",
    connecting_plate: 0,
    machine_amt:0
})

let msgModal = ref(null);
let machine_line = ref([])


function refresh() {
  window.location.reload();
}

function queryBtn() {
  // 清空所有查詢欄位的值
  queryFields.value.forEach(field => {
  field.field_value = '';  // 清空每個欄位的 field_value
  });

  // modalKey.value++;
  qModal.value.myModal_show()
}

// 操作表格的按鈕邏輯
let [rows, addRow, delRow, toggleSelectAll, del_existed_rows,handleCheckBox,selectAllVal] = useTable() 
// 操作查詢邏輯
let [query] = useQuery(machine,rows,delShow)
// 儲存資料邏輯
let [msg, save] = useSave(rows, del_existed_rows, machine, query, msgModal, delShow, dynamicStatusClass, successFlag)


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

function query2backend4data(machine_obj) {
  qModal.value.myModal_hide();
  query(machine_obj.id);
}

function updateQueryField({ index, value }) {
  queryFields[index].field_value = value;

}

watch(queryFields, (newFields) => {
  // 當 queryFields 更新時，強制觸發子組件的顯示
  qModal.value.myModal_show();
}, { deep: true });  


function del_btn() {
  confirmModal.value.myModal_show()
}

async function delMachine() {
  confirmModal.value.myModal_hide()
    try {
      let response = await axios.delete(`http://192.168.0.183:8000/machine_detail/${machine.value.machine_id}`);
      let statusCode = response.status
      if (statusCode == 204) { 
        successFlag.value = true;
        dynamicStatusClass.value = "success"
        msg.value = "刪除成功";
        msgModal.value.myModal_show()
        await new Promise(resolve => setTimeout(resolve, 1500));
        msgModal.value.myModal_hide()
        refresh()
      }
    } catch (error) {
      successFlag.value = false;
      msg.value = "錯誤";
    }
}

</script>



<style scoped>
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

</style>
  