import modal from "@/components/modal.vue";
import axios from "axios";
import { ref } from "vue";


// export function (rows,del_existed_rows,machine,successFlag,dynamicStatusClass) {
export default function (rows,del_existed_rows,machine,query,msgModal,delShow,dynamicStatusClass,successFlag) {
    
    let msg = ref("");

    async function save() {
        /*
        最後要發給後端的資料有:
        1.Machine:
          {
            machine_id:null
            machine_name:xxx,
            connecting_plate:xxx,
            machine_amt:xxx
          }
      
        2.Machine_line:
      
          [
            {
              machine_id:"",
              machine_line_id:""
              machine_line_name:"",
              machine_line_amt:"",
              emp_default_amt:""
            },
            {}...
          ]
      
        3. 要刪除的已存在Machine_line 資料
          [
            {
              "machine_id":"",
               machine_line_id:null
              "machine_line_name":"",
              "machine_line_amt":"",
              "emp_default_amt":""
            },
            {
              "machine_id":"",
               machine_line_id:null
              "machine_line_name":"",
              "machine_line_amt":"",
              "emp_default_amt":""
            },...
          ]
        */
      
        let machine_line_create_update = []
        let machine_line_del = []
        for (let i = 0; i < rows.value.length; i++) { 
          let row = rows.value[i]
          delete row['selected']
          if (row['machine_line_name']) { 
            machine_line_create_update.push(row)
          }
          
        }
      
        for (let i = 0; i < del_existed_rows.value.length; i++) { 
          let row = del_existed_rows.value[i]
          delete row['selected']
          machine_line_del.push(row)
        }
      
        let req_data = {
          "machine": machine.value,
          "machine_line_create_update": machine_line_create_update,
          "machine_line_del": machine_line_del,
        }
      
        let response = null
        try {
          // response = await axios.post("http://127.0.0.1:8000/machine/", req_data);
          response = await axios.post("http://192.168.0.183:8000/machine/", req_data);
          let errcode = response.data.errcode
          let msg_backend = response.data.msg
      
          msg.value = msg_backend;
          if (errcode == 0) { 
            successFlag.value = true;
            dynamicStatusClass.value = "success"
            machine.value = response.data.machine_data
            query(machine.value.machine_id)
          }
        } catch (error) {
          successFlag.value = false;
          msg.value = "錯誤";
        }
        msgModal.value.myModal_show();
      }
      
    return [msg,save]
}