<!-- src/App.vue -->
<template>
  <div>
    <h1>Lab Workflow Frontend</h1>
    <CreateBatch />
    <UpdateStatus />
  </div>
</template>

<script>
import CreateBatch from './components/CreateBatch.vue';
import UpdateStatus from './components/UpdateStatus.vue';

export default {
  components: {
    CreateBatch,
    UpdateStatus
  }
};
</script>
