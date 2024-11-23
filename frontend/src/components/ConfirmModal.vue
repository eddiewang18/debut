<template>
    <div class="modal" tabindex="-1" ref="modal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">詢問</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="msg">{{message}}</div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="myModal_hide()"
            >
              取消
            </button>
            <button type="button" class="btn btn-primary" @click="sure">
              確定
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref , defineEmits } from 'vue';
  import Modal from 'bootstrap/js/dist/modal';
  const modal = ref(null);
  const myModal = ref(null);
  
  onMounted(() => {
    myModal.value = new Modal(modal.value);
  });
  
  const myModal_show = () => {
    myModal.value.show();
  };
  
  const myModal_hide = () => {
    myModal.value.hide();
  };
  
  defineExpose({
    myModal_show,
    myModal_hide,
  });

  const props = defineProps({
    message: String,
});

const emit = defineEmits(['sure']);

function sure() {
    emit('sure')
}

  </script>

<style scoped>
.msg{
    font-size: 20px;
    font-weight: 700;
}

</style>