<template>

  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" ref="modal">
    <div class="main_modal modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="space msg_icon">
              <font-awesome-icon v-if="successFlag" :icon="['fas', 'circle-check']" class="fa-4x" style="color: #63E6BE;" />
              <font-awesome-icon v-else :icon="['fas', 'circle-xmark']" class="fa-4x" style="color: #f20707;" />
          </div>
          <div :class="['space','msg',dynamicStatusClass]">
              {{ msg }}
          </div>
        </div>
  
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
    name : "modal"
}
</script>

<script setup>
    import { onMounted, ref } from 'vue';
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



const props = defineProps(
  {
  msg: {
      type: String,
      default:"",
    },
  successFlag: {
      type: Boolean,
      default:false
    },
    dynamicStatusClass: {
    type: String,
    default:"fail"
  }
  }
)

</script>
  
<style scoped>

.custom-modal-dialog {
  max-width: 300px;
  max-height: 200px;
}

.msg_icon {
  display: flex;
  justify-content: center;
  align-items: center;
}

.msg {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 22px;
  font-weight: 700;
}

div.space{
    margin: 20px 0px;
}

div.main_modal{
    width: 400px;
    height: 250px;
}

.fail{
  color:red
}

.success{
  color: green;
}

</style>