<!-- src/components/Dashboard.vue -->
<template>
    <div class="dashboard">
      <h1>🧪 Lab Workflow Dashboard</h1>
      <create-batch />
      <file-uploader />
  
      <div class="event-log">
        <h3>Kafka Event Log</h3>
        <ul>
          <li v-for="(event, i) in events" :key="i">{{ event }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import CreateBatch from './CreateBatch.vue';
  import FileUploader from './FileUpload.vue';
  
  export default {
    components: { CreateBatch, FileUploader },
    data() {
      return {
        events: []
      };
    },
    mounted() {
      // Simulate consuming Kafka events (poll every 3s)
      this.pollEvents();
    },
    methods: {
      async pollEvents() {
        // In real app, connect via websocket or Kafka REST
        setInterval(() => {
          const timestamp = new Date().toLocaleTimeString();
          this.events.unshift(`Event received at ${timestamp}`);
          if (this.events.length > 10) this.events.pop();
        }, 3000);
      }
    }
  };
  </script>
  
  <style scoped>
  .dashboard {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
  }
  .event-log {
    border: 1px solid #ccc;
    padding: 1rem;
    background: #0d0d0e;
    border-radius: 10px;
  }
  </style>
  