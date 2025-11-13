<!-- src/components/UpdateStatus.vue -->
<template>
    <div class="update-status">
      <h2>Update Batch Status</h2>
      <form @submit.prevent="updateBatch">
        <input v-model="batch_id" placeholder="Batch ID" required />
        <select v-model="status">
          <option value="Requested">Requested</option>
          <option value="In Progress">In Progress</option>
          <option value="Completed">Completed</option>
        </select>
        <input v-model="customer_id" placeholder="Customer ID (optional)" />
        <button type="submit">Update Status</button>
      </form>
      <div v-if="message">{{ message }}</div>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    data() {
      return {
        batch_id: '',
        status: 'Requested',
        customer_id: '',
        message: ''
      };
    },
    methods: {
      async updateBatch() {
        try {
          const response = await api.post(`/update_status/${this.batch_id}`, {
            status: this.status,
            customer_id: this.customer_id
          });
          this.message = response.data.message;
          this.batch_id = '';
          this.customer_id = '';
        } catch (error) {
          this.message = 'Error updating status';
          console.error(error);
        }
      }
    }
  };
  </script>
  