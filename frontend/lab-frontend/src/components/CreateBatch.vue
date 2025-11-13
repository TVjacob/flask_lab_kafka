<!-- src/components/CreateBatch.vue -->
<template>
    <div class="create-batch">
      <h2>Create Lab Batch</h2>
      <form @submit.prevent="submitBatch">
        <input v-model="patient_name" placeholder="Patient Name" required />
        <input v-model="test_type" placeholder="Test Type" required />
        <select v-model="priority">
          <option value="High">High</option>
          <option value="Normal">Normal</option>
        </select>
        <button type="submit">Create Batch</button>
      </form>
      <div v-if="message">{{ message }}</div>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    data() {
      return {
        patient_name: '',
        test_type: '',
        priority: 'High',
        message: ''
      };
    },
    methods: {
      async submitBatch() {
        try {
          const response = await api.post('/create_batch', {
            patient_name: this.patient_name,
            test_type: this.test_type,
            priority: this.priority
          });
          this.message = `Batch created with ID: ${response.data.batch_id}`;
          this.patient_name = '';
          this.test_type = '';
        } catch (error) {
          this.message = 'Error creating batch';
          console.error(error);
        }
      }
    }
  };
  </script>
  