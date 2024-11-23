import axios from "axios";


export default function (machine,rows,delShow) {
    async function query(machine_id) { 
        let response = null
        try {
          // response = await axios.get(`http://127.0.0.1:8000/machine_detail/${machine_id}`)
          response = await axios.get(`http://192.168.0.183:8000/machine_detail/${machine_id}`)
          let data = response.data
          machine.value = {
            machine_id:data.machine_id,
            machine_name: data.machine_name,
            connecting_plate: data.connecting_plate,
            machine_amt:data.machine_amt
          }
      
          rows.value = data.lines
          delShow.value = true
        } catch (error) {
          console.log('查詢request時錯誤=>'+error)
        }
    }
    return [query]
}