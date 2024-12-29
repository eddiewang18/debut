import modal from "@/components/modal.vue";
import axios from "axios";
import { ref } from "vue";
import useUtils from "../useUtils";


// export function (rows,del_existed_rows,machine,successFlag,dynamicStatusClass) {
export default function (rows,del_existed_rows,machine,query,msgModal,delShow,dynamicStatusClass,successFlag) {
    
    let [isInteger] = useUtils()

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
      
        let machine_req_data = machine.value       
        if (machine_req_data.connecting_plate != 0 && !isInteger(machine_req_data.connecting_plate)) { 
          successFlag.value = false;
          dynamicStatusClass.value = false
          msg.value = "連版數量 須為整數";
          msgModal.value.myModal_show();
          return;
        }
        
        if (machine_req_data.machine_amt !=0 && !isInteger(machine_req_data.machine_amt)) { 
          successFlag.value = false;
          dynamicStatusClass.value = false
          msg.value = "機種台數 須為整數";
          msgModal.value.myModal_show();
          return;
        }      
      
        let machine_line_create_update = []
        let machine_line_del = []
        for (let i = 0; i < rows.value.length; i++) { 
          let row = rows.value[i]
          delete row['selected']

          if (!row['machine_line_name']) { 
            successFlag.value = false;
            dynamicStatusClass.value = "fail"
            msg.value = `第${i+1}列 線名 不可空白`;
            msgModal.value.myModal_show();
            return;
          }

          if (row['emp_default_amt'] != 0 && !row['emp_default_amt']) { 
            successFlag.value = false;
            dynamicStatusClass.value = "fail"
            msg.value = `第${i+1}列 員工數 不可空白`;
            msgModal.value.myModal_show();
            return;
          }

          if (row['emp_default_amt'] != 0 && !isInteger(row['emp_default_amt'])) { 
            successFlag.value = false;
            dynamicStatusClass.value = "fail"
            msg.value = `第${i+1}列 員工數 須為整數`;
            msgModal.value.myModal_show();
            return;            
          }
            machine_line_create_update.push(row) 
        }
      
        for (let i = 0; i < del_existed_rows.value.length; i++) { 
          let row = del_existed_rows.value[i]
          delete row['selected']
          machine_line_del.push(row)
        }
      
        let req_data = {
          "machine": machine_req_data,
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
          dynamicStatusClass.value = "fail"
          msg.value = "錯誤";
        }
        msgModal.value.myModal_show();
      }
      
    return [msg,save]
}