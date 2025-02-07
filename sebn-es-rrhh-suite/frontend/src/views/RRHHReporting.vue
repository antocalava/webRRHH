<template>
  <main class="d-flex flex-column mt-3 mx-2 overflow-x-hidden reporting-home-office flex-body">
    <h1 class="text-left mt-3 mb-4 fs-3 fw-bold" >Customize your report</h1>

    <!-- HOME OFFICE -->
    <div id="homeOfficeContainer" class="p-4 border mb-4">
      <h2 class="mb-3 fs-5">Home Office</h2>
      <form :id="formHomeoffice" @submit.prevent="createHomeOfficeReport()">
        <label class="w-50">
          <span class="sr-only">Starting date</span>
          <input type="date" class="form-control" v-model="formHomeoffice.startDate" required>
        </label>
        <label class="w-50">
          <span class="sr-only">Finishing date</span>
          <input type="date" class="form-control" v-model="formHomeoffice.endDate" required>
        </label>
        <div class="d-flex align-items-center gap-3 mt-2 ms-1">
          <button type="submit" class="btn btn-primary btn-block bg-main ms-3">
            <a  download="HomeOfficeReport.xlsx">Generate</a>
          </button>
          <!-- <a v-if="excelFile" :href="excelFile" download="HomeOfficeReport.xlsx" class="btn btn-success btn-block bg-main ms-3">Download Report</a> -->
        </div>
      </form>
    </div>

    <!-- Vacations -->
    <div id="vacationsContainer" class="p-4 border mb-4" style="display: none;"> <!-- TODO: QUITARLE DISPLAY NONE cuando esté hecho el report-->
      <h2 class="mb-3 fs-5">Holidays</h2>
      <form :id="formVacations" @submit.prevent="createVacationReport()">
        <label class="w-50">
          <span class="sr-only">Starting date</span>
          <input type="date" class="form-control" v-model="formVacations.startDate" required>
        </label>
        <label class="w-50">
          <span class="sr-only">Finishing date</span>
          <input type="date" class="form-control" v-model="formVacations.endDate" required>
        </label>
        <div class="d-flex align-items-center gap-3 mt-2 ms-1">
          <button type="submit" class="btn btn-primary btn-block bg-main ms-3">
            <a :href="vacationsReport" download="VacationReport.xlsx">Generate</a>
          </button>
        </div>
      </form>
    </div>

    <!-- Travels -->
    <div id="travelsContainer" class="p-4 border mb-4" style="display: none;"> <!-- TODO: QUITARLE DISPLAY NONE cuando esté hecho el report-->
      <h2 class="mb-3 fs-5">Travels</h2>
      <form :id="formTravels" @submit.prevent="createTravelReport()">
        <label class="w-50">
          <span class="sr-only">Starting date</span>
          <input type="date" class="form-control" v-model="formTravels.startDate" required>
        </label>
        <label class="w-50">
          <span class="sr-only">Finishing date</span>
          <input type="date" class="form-control" v-model="formTravels.endDate" required>
        </label>
        <div class="d-flex align-items-center gap-3 mt-2 ms-1">
          <button type="submit" class="btn btn-primary btn-block bg-main ms-3">
            <a :href="travelsReport" download="TravelReport.xlsx">Generate</a>
          </button>
        </div>
      </form>
    </div>


  </main>
</template>

<script>
  import {loadingMessage, notifyError, notifySuccess, stopLoadingMessage} from '@/assets/globalFunctions';
  import {BACKEND_HOST} from '../config';

  export default {
    data() {
      return {
        homeOfficeReport: null,
        formHomeoffice: {
          startDate: '',
          endDate: ''
        },

        vacationsReport: null,
        formVacations: {
          startDate: '',
          endDate: ''
        },

        travelsReport: null,
        formTravels: {
          startDate: '',
          endDate: ''
        },
      };
    },
    methods: {
      async createHomeOfficeReport() {
        this.homeOfficeReport = null;
        loadingMessage();
        try {
          const data = {
            starting_date: this.formHomeoffice.startDate,
            finishing_date: this.formHomeoffice.endDate
          };

          const response = await fetch(`${BACKEND_HOST}hr/get-reporting-home-office`, {
            method: 'POST',
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || error.state);
          }

          const blob = await response.blob();
          const url = window.URL.createObjectURL(new Blob([blob]));
          this.homeOfficeReport = url;
          await this.createAndRemoveLink()
          stopLoadingMessage();
          notifySuccess('Report created succesfully');
          // this.resetHomeOfficeFilters();
        } catch (error) {
          stopLoadingMessage();
          console.error('Error downloading Excel file:', error.message);
          notifyError('Failed to generate report: ' + error.message);
        }
      },
      async createAndRemoveLink(userInfo) {
      const a = document.createElement('a');
      a.href = this.homeOfficeReport;
      a.download = "HomeOfficeReport.xlsx";

      document.body.appendChild(a);
      a.click();

      setTimeout(() => {
        document.body.removeChild(a);
      }, 1000);
    },
      async createVacationReport(){
        this.vacationsReport = null;
        alert("Coming soon")
        //TODO: createVacationReport()
        this.resetVacationsFilters();
      },
      async createTravelReport(){
        this.travelsReport = null;
        alert("Coming soon")
        //TODO: createTravelReport()
        this.resetTravelsFilters();
      },
      resetHomeOfficeFilters(){
        this.formHomeoffice = {
          startDate: '',
          endDate: ''
        }
      },
      resetVacationsFilters(){
        this.formVacations = {
          startDate: '',
          endDate: ''
        }
      },
      resetTravelsFilters(){
        this.formTravels = {
          startDate: '',
          endDate: ''
        }
      },
    },
  };
</script>