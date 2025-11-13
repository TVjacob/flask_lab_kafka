<!-- src/App.vue -->
<template>
  <div>
    <h1>Lab Workflow Frontend</h1>
    <dashboard />
    <!-- <CreateBatch /> -->
    <!-- <UpdateStatus /> -->
  </div>
</template>

<script>
import CreateBatch from './components/CreateBatch.vue';
import UpdateStatus from './components/UpdateStatus.vue';
import Dashboard from './components/Dashboard.vue';
// export default { components: { Dashboard } };
export default {
  components: {
    Dashboard,
    CreateBatch,
    UpdateStatus
  }
};
</script>
