<template>
  <main class="mt-3 mx-2 px-0 flex-body">
    <h1 class="text-left mb-2 fs-3 fw-bold col-6">Head Count</h1>
    <!-- <input type="file" @change="onFileChange" /> -->
    <div class="custom-file-input ps-1">
      <button type="button" @click="triggerFileInput" class="btn btn-primary">Choose File</button>
      <label for="fileInput" class="visually-hidden">Choose File</label>
      <input type="file" ref="fileInput" @change="onFileChange" class="d-none" id="fileInput" name="fileInput" />
      <span class="ms-2">{{ fileName ? fileName : 'No file chosen' }}</span>
    </div>
    <div class="d-flex flex-column align-items-start gap-1 mt-2 ps-1">
      <label for="month">Month:</label>
      <select v-model="month" id="month" name="month" required class="form-select w-25">
        <option disabled value="">Select a month</option>
        <option v-for="n in monthsListed" :key="n" :value="n">{{ n }}</option>
      </select>
      
      <label for="year">Year:</label>
      <select v-model="year" id="year" name="year" required class="form-select w-25">
        <option disabled value="">Select a year</option>
        <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
      </select>
      
      <button type="submit" class="btn btn-primary btn-block bg-main mt-2" @click="submitForm">Process</button>
    </div>
  </main>
</template>

<script>
  import { notifyError } from '@/assets/globalFunctions';
  import { BACKEND_HOST } from '../config';

  export default {
    data() {
      return {
        month: '',
        year: '',
        selectedFile: null,
        fileName: '',
        monthsListed: this.generateMonths(),
        years: this.generateYears()
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      onFileChange(event) {
        this.selectedFile = event.target.files[0];
        this.fileName = this.selectedFile ? this.selectedFile.name : 'No file chosen';
      },
      async submitForm() {
        if (!this.selectedFile) {
          notifyError('Please select a file first');
          return;
        }else if (!this.month || !this.year){
          notifyError('Please select a month/year pair.');
          return;
        }

        const formData = new FormData();
        formData.append('file', this.selectedFile);
        formData.append('month', this.month);
        formData.append('year', this.year);

        try {
          const response = await fetch(`${BACKEND_HOST}hr/get-hr-head-count-CUE-report`, {
            method: 'POST',
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
            },
            body: formData,
          });

          if (!response.ok) {
            //const error = await response.json();
            throw new Error("Error processing the file");
          }

          const blob = await response.blob();
          const url = window.URL.createObjectURL(new Blob([blob]));
          const link = document.createElement('a');
          link.href = url;

          // Get today's date
          const today = new Date();
          const year = today.getFullYear();
          const month = String(today.getMonth() + 1).padStart(2, '0');
          const day = String(today.getDate()).padStart(2, '0');
          const formattedDate = `${year}${month}${day}`;

          const filename = `RecruitingPlanningSpain_24-25_ForecastVSReal_${formattedDate}.xlsx`;
          link.setAttribute('download', filename);
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
        } catch (error) {
          notifyError(error.message);
        }
      },
      generateYears() {
        const limitYear = 2028;
        const startYear = 2024;
        const years = [];
        for (let year = startYear; year <= limitYear; year++) {
          years.push(year);
        }
        return years;
      },
      generateMonths() {
        return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      }
    },
  };
</script>
