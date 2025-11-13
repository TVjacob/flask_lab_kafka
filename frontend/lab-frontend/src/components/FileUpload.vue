<!-- src/components/FileUploader.vue -->
<template>
    <div class="upload-section">
      <h2>📂 File Upload Processor</h2>
  
      <form @submit.prevent="uploadFiles">
        <label>XML File</label>
        <input type="file" @change="onFileChange($event, 'xml')" />
  
        <label>JSON File</label>
        <input type="file" @change="onFileChange($event, 'json')" />
  
        <label>Image File</label>
        <input type="file" @change="onFileChange($event, 'image')" />
  
        <label>PDF File</label>
        <input type="file" @change="onFileChange($event, 'pdf')" />
  
        <button type="submit">Upload</button>
      </form>
  
      <div v-if="message" :class="{'error': isError, 'success': !isError}" class="mt-3">
        {{ message }}
      </div>
      <a v-if="zipUrl" :href="zipUrl" download>Download Processed ZIP</a>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    data() {
      return {
        files: {},
        message: '',
        isError: false,
        zipUrl: null
      };
    },
    methods: {
      onFileChange(event, type) {
        this.files[type] = event.target.files[0];
      },
      async uploadFiles() {
        this.message = '';
        this.isError = false;
        this.zipUrl = null;
  
        try {
          const formData = new FormData();
          Object.keys(this.files).forEach(type => {
            formData.append(type, this.files[type]);
          });
  
          const response = await api.post('/upload_files', formData, {
            responseType: 'blob'
          });
  
          // Check if response is JSON (error) or Blob (ZIP)
          const contentType = response.headers['content-type'];
          if (contentType.includes('application/json')) {
            const text = await response.data.text();
            const errorData = JSON.parse(text);
            this.message = `❌ ${errorData.error || 'Upload failed'}`;
            this.isError = true;
          } else {
            const blob = new Blob([response.data], { type: 'application/zip' });
            this.zipUrl = URL.createObjectURL(blob);
            this.message = '✅ Upload successful! You can now download the processed ZIP.';
          }
  
        } catch (err) {
          if (err.response && err.response.data) {
            try {
              const text = await err.response.data.text();
              const errorData = JSON.parse(text);
              this.message = `❌ ${errorData.error || 'Upload failed'}`;
            } catch {
              this.message = '❌ Upload failed (unexpected error)';
            }
          } else {
            this.message = '❌ Upload failed (network error)';
          }
          this.isError = true;
          console.error(err);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .upload-section {
    padding: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 12px;
    background: #050505;
    width: 400px;
    color: white;
  }
  input, button {
    margin: 0.5rem 0;
    display: block;
  }
  .error {
    color: #ff4d4f;
  }
  .success {
    color: #4caf50;
  }
  </style>
  