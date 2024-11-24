<template>
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" ref="queryModal">
  <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">查詢</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form>
                    <div v-for="(queryField,index) in queryFields" class="mb-3">
                        <label for="recipient-name" class="col-form-label">{{ queryField.field_name }}</label>
                        <input v-model="queryFields[index].field_value" @keyup="q_instantly(queryField.unique,index)" :type="queryField.input_type" class="form-control" id="recipient-name">
                        <br/>
                        <div @click="setOption2Qfield(result.name,index,result.id)" class="q_options" v-for="result in q_result" v-if="queryField.unique && sure">
                            <div class="q_options_inner"  :pk="result.id" :key="result.id">
                                {{ result.name }}
                            </div>
                            <hr/>
                        </div>
                    </div>

                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">關閉</button>
                <button type="button" class="btn btn-primary">查詢</button>
            </div>
        </div>
    </div>
</div>


</template>


<script setup>
import { ref, onMounted, watch, defineExpose } from 'vue';
import Modal from 'bootstrap/js/dist/modal';

const queryModal = ref(null);
const myQueryModal = ref(null);
const sure = ref(true);

const props = defineProps({
    queryFields: Array,
    q_result: Array,
});


const emit = defineEmits(['query2backend', 'query2backend4data', 'updateQueryField']);

onMounted(() => {
    myQueryModal.value = new Modal(queryModal.value, {
        backdrop: 'static',
        focus: true,
    });
});

const myModal_show = () => {
    myQueryModal.value.show();
};

const myModal_hide = () => {
    myQueryModal.value.hide();
};

defineExpose({
    myModal_show,
    myModal_hide,
});

function q_instantly(unique, index) {
    if (unique) {
        sure.value = true;
        emit('query2backend', props.queryFields[index]);
    }
}

function setOption2Qfield(val, q_field_index,id) {
    emit('query2backend4data',{ index: q_field_index, value: val,id:id });
    sure.value = false;

}

watch(() => props.q_result, (newVal) => {
    if (newVal.length === 1) {
        props.queryFields[0].field_value = newVal[0].name;
        sure.value = false;
        // 清空輸入框
        emit('query2backend4data', newVal[0]);

    }
});

</script>


<style  scoped>

    .q_options_inner{
        margin: 10px;
    }

    .q_options{
        margin: 10px;
    }


    .q_options:hover{
        background-color: skyblue;
        color: white;
        /* font-weight: 700; */
    }

    .q_options:active{
        font-weight: 700; 
    }

</style>