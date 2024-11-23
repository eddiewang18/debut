import { ref } from "vue";

export default function () {

    const rows = ref([]);
    const del_existed_rows = ref([]);
    let selectAllVal = ref(false)
    const addRow = () => {
        rows.value.push({
            selected: false,
            machine_line_id: null,
            machine_line_name: "",
            // machine_line_amt: 0,
            emp_default_amt: 0,
        });
    };
    
    const delRow = () => {
        let tmp_rows = []

        for (let i = 0; i < rows.value.length; i++){
            let row = rows.value[i]
            if (!row.selected) { 
                tmp_rows.push(row)
            } else {
                if (row.machine_line_id) { 
                    del_existed_rows.value.push(row)
                }
            }
        }
        rows.value = tmp_rows
        // rows.value = rows.value.filter((row) => !row.selected);
    };
    
    const toggleSelectAll = (event) => {
        const isChecked = event.target.checked;
        rows.value.forEach((row) => {
            row.selected = isChecked;
        });
    };

    function handleCheckBox(event,index) {
        const isChecked = event.target.checked;
        rows.value[index].selected = isChecked
        if (!isChecked) { 
          selectAllVal.value = isChecked;
        }
        else
        { 
          let flag = true
          rows.value.forEach
          (
            (row) =>
            {      
              if (!row.selected)
              {       
                flag = false;          
                return
              } 
            }
          ); 
          selectAllVal.value = flag;
        }
      }

    return [rows,addRow,delRow,toggleSelectAll,del_existed_rows,handleCheckBox,selectAllVal]

}