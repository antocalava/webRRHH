<template>
  <main class="mt-3 mx-2 px-0 flex-body">
    <h1 class="text-left mt-3 mb-2 fs-3 fw-bold col-6">User bucket inputs</h1>
    <div class="form-group">
      <div class="row">
        <div class="col-md-6">
          <div class="input-group w-100">
            <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
            <input type="text" class="form-control" v-model="searchQuery" placeholder="Search user...">
          </div>
        </div>
        <div class="col-md-6 mt-2 mt-md-0 d-flex align-items-center justify-content-md-end">
          <button class="btn btn-primary me-2 bg-main" data-bs-target="#modalConfirm" data-bs-toggle="modal" @click="fetchUsersAndBuckets">
            Add Input
          </button>

          <div class="dropdown position-relative">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="btn_filterInputs" data-bs-toggle="dropdown" aria-expanded="false">
              <span><i class="fa-solid fa-filter"></i></span> Filter
            </button>

            <div class="dropdown-menu dropdown-menu-end p-4 shadow" aria-labelledby="btn_filterInputs" style="min-width: 300px; position: absolute; top: 100%; right: 0; z-index: 2000;">
              <form>
                <label>User</label>
                <select class="form-select mt-2 mb-2" id="userFilterSelect" @change="updateSelectedUser">
                  <option value="all">All</option>
                  <option v-for="user in users" :value="user.Email">{{ user.FullName }}</option>
                </select>

                <label>Bucket</label>
                <select class="form-select mt-2 mb-2" id="bucketFilterSelect" @change="updateSelectedBucket">
                  <option value="all">All</option>
                  <option v-for="bucket in buckets" :value="bucket.bucket">{{ bucket.bucket }}</option>
                </select>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modalConfirm" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <form>
            <div class="modal-body">
              <div class="mb-3">
                <label for="userInputSelect" class="form-label required">User:</label>
                <select class="form-select" id="userInputSelect" required>
                  <option value="" selected disabled hidden>Select employee...</option>
                  <option v-for="user in users" :value="user.Email">{{ user.FullName }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="reason" class="form-label required">Reason:</label>
                <input type="text" class="form-control" id="reason" required placeholder="Provide a reason...">
              </div>
              <div class="mb-3">
                <label for="bucket" class="form-label required">Bucket:</label>
                <select class="form-select" id="bucketInputSelect" required>
                  <option value="" selected disabled hidden>Select bucket...</option>
                  <option v-for="bucket in buckets" :value="bucket.bucket">{{ bucket.bucket }}</option>
                </select>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="city" class="form-label">Quantity: (adds by default)</label>
                  <input class="form-control" type="number" name="quantity" id="quantity" required value="0">
                </div>
                <div class="col-md-6 d-flex align-items-center mt-4">
                  <div class="form-check mt-">
                    <input class="form-check-input custom-checkbox" type="checkbox" name="restar" id="restar" required>
                    <label class="form-check-label ms-2" for="restar">Subtract</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button id="btnCancelInputForm" type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetInputForm()">Cancel</button>
              <button type="button" class="btn btn-primary bg-main" @click="validateInput()">Accept</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="scroll-container mt-3" style="max-height: 750px; overflow-y: auto;">
      <table class="table mt-2 table-striped">
        <thead class="thead-dark position-sticky" style="top: 0; z-index: 1020; background-color: white;">
          <tr>
            <th scope="col">Email</th>
            <th scope="col">Entry Date</th>
            <th scope="col">Reason</th>
            <th scope="col">Bucket</th>
            <th scope="col">Quantity</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(log, index) in filteredLogs" :key="index">
            <td>{{ log.UserEmail }}</td>
            <td>{{ formatDate(log.EntryDate) }}</td>
            <td>{{ log.Reason }}</td>
            <td>{{ log.Bucket }}</td>
            <td>{{ log.Quantity }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

  
<script>
  import {loadingMessage, stopLoadingMessage, notifyError, notifySuccess} from '@/assets/globalFunctions';
  import {BACKEND_HOST} from '../config';


  export default {
    data() {
      return {
        logRrhh: [],
        searchQuery: '',
        users: [],
        buckets: [],
        selectedUser: 'all',
        selectedBucket: 'all',
        isFormValid: true
      }
    },
    created() { 
      this.fetchLogs(); //solo cargamos los logs en la primera carga
      this.fetchUsersAndBuckets();
    },
    computed: {
      filteredLogs() {
        return this.logRrhh.filter(log => {
          const userFilter = this.selectedUser === 'all' || log.UserEmail === this.selectedUser;
          const bucketFilter = this.selectedBucket === 'all' || log.Bucket === this.selectedBucket;

          return userFilter && bucketFilter && log.UserEmail && log.UserEmail.toLowerCase().includes(this.searchQuery.toLowerCase())
        });
      }

    },
    methods: {
      formValidationError(elementId, message) {
        this.formIsValid = false;
        if (elementId) document.getElementById(elementId).classList.add("hasError")
        let error = new Error(message)
        notifyError(error.message);
        console.error(error.message)
      },
      cleanFormValidationErrorFields() {
        const elements = document.querySelectorAll('.hasError');
        elements.forEach(element => {
          element.classList.remove('hasError');
        });
        this.formIsValid = true;
      },
      resetInputForm(){
        this.cleanFormValidationErrorFields();
        document.getElementById('userInputSelect').selected = "";
        document.getElementById('bucketInputSelect').selected = "";
        document.getElementById('reason').value = '';
        document.getElementById('quantity').value = 0;
        document.getElementById('restar').checked = false;
      },
      validateInput(){
        this.cleanFormValidationErrorFields();
        try {
          const vUser = document.getElementById('userInputSelect').value;
          const vBucket = document.getElementById('bucketInputSelect').value;
          const vReason = document.getElementById('reason').value;
          let vQuantity = document.getElementById('quantity').value;
          const vRestar = document.getElementById('restar').checked;

          //Required fields validations
          console.log(vUser)
          if (!vUser || vUser == "") this.formValidationError('userInputSelect', 'An employee must be chosen')
          if (!vReason || vReason.trim() == '') this.formValidationError('reason', 'A reason for the input creation must be provided')
          if (!vReason || vReason.trim() == '') this.formValidationError('reason', 'A reason for the input creation must be provided')
          if (!vBucket || vBucket == "") this.formValidationError('bucketInputSelect', 'A bucket must be chosen')
          if(vQuantity == 0)  this.formValidationError('quantity', 'Quantity can not be zero')
          if(vQuantity < 0 && !vRestar)  this.formValidationError('quantity', 'Quantity can not be negative if Subtract is unchecked')
          if(vQuantity > 0 && vRestar)  this.formValidationError('quantity', 'Quantity can not be positive if Subtract is checked')

          //if everything alright, we create the new user
          if (this.formIsValid) this.createInput()
        } catch (error) {
          console.error(error);
        }
      },
      async createInput() {
        const vUser = document.getElementById('userInputSelect').value;
        const vBucket = document.getElementById('bucketInputSelect').value;
        const vReason = document.getElementById('reason').value;
        let vQuantity = document.getElementById('quantity').value;
        const vRestar = document.getElementById('restar').checked;

        vQuantity = parseFloat(vQuantity);
        if (vRestar) {
          vQuantity *= -1;
        }

        const data = {
          email: vUser,
          type: vBucket,
          reason: vReason,
          quantity: vQuantity
        }

        try {
          const response = await fetch(`${BACKEND_HOST}user/update-user-single-day`, {
            method: 'POST',
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message);
          }

          notifySuccess('Input created succesfully');
          this.resetInputForm();
          document.getElementById(btnCancelInputForm).click();
          this.fetchLogs();
        } catch (error) {
          notifyError(error.message);
        }

      },
      async fetchLogs() {
        loadingMessage();
        try {
          const response = await fetch(`${BACKEND_HOST}hr/get-hr-logs`, {
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
          });

          if (!response.ok) {
            throw new Error('Logs could not be obtained');
          }
          const data = await response.json();
          this.logRrhh = data;

          stopLoadingMessage();
        } catch (error) {
          stopLoadingMessage();
          notifyError(error);
        }
      },
      updateSelectedUser(event) {
        this.selectedUser = event.target.value;
      },
      updateSelectedBucket(event) {
        this.selectedBucket = event.target.value;
      },
      fetchUsersAndBuckets(){ //Cuando necesitemos esos datos, hacemos las llamadas
        if(this.buckets.length <= 0 && this.users.length <= 0 ){
          this.fetchUsers()
          this.fetchBuckets()
        }
      },
      formatDate(date) {
        if (!date) return '';
        const d = new Date(date);
        const day = d.getDate().toString().padStart(2, '0');
        const month = (d.getMonth() + 1).toString().padStart(2, '0');
        const year = d.getFullYear();
        return `${day}/${month}/${year}`;
      },
      async fetchUsers() {
        loadingMessage();
        try {
          const response = await fetch(`${BACKEND_HOST}hr/get-all-users-simple-list`, {
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            }
          });
          if (!response.ok) {
            throw new Error('Users were unable to load');
          }
          const data = await response.json();
          this.users = data;
          this.fetchLogs();
        } catch (error) {
          notifyError(error);
          stopLoadingMessage();
        }
      },
    // Función necesaria para select de ADD INPUT o modal de filter
    async fetchBuckets() {
        try {
          const response = await fetch(`${BACKEND_HOST}hr/get-buckets`, {
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            }
          });

          if (!response) {
            throw new Error('Bucket could not be loaded');
          }

          const data = await response.json();
          this.buckets = data;
          stopLoadingMessage();
        } catch (error) {
          notifyError(error.message);
          stopLoadingMessage();
        }
      }, 
    }
  }
</script>

<style>
  .hasError {
    border: solid #b61e1e 0.15rem;
    border-color: #b61e1e;
    background-color: #b61e1e28;
  }
</style>