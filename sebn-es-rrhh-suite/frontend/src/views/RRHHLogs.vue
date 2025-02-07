<template>
  <main class="d-flex flex-column px-2 flex-body">
    <h1 class="text-left mt-3 mb-1 fs-3 fw-bold col-6">Vacation request logs</h1>

    <!-- Search employees -->
    <div id="searchContainer" class="col-md-6 pe-4 position-relative mb-3 mt-1">
      <div class="input-group">
        <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
        <div class="flex-fill position-relative">
          <input type="search" class="form-control rounded-0" v-model="searchQuery"
              placeholder="Search user...">
        </div>
      </div>
    </div>

    <div class="d-flex flex-column overflow-auto">
    <div class="table-responsive" id="scrollableLogs">
        <table class="table table-striped">
            <thead class="position-sticky" style="top: 0; z-index: 1020; background-color: white;">
                <tr>
                    <th>Email</th>
                    <th>Entry date</th>
                    <th>Start day</th>
                    <th>End day</th>
                    <th>Quantity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="log in filteredLogs" :key="log.id">
                    <td>{{ log.UserEmail }}</td>
                    <td>{{ formatDate(log.EntryDate) }}</td>
                    <td>{{ formatDate(log.StartingDay) }}</td>
                    <td>{{ formatDate(log.FinishingDay) }}</td>
                    <td>{{ log.Quantity }}</td>
                    <td>{{ log.Status }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
  </main>
</template>

<script>
  import {formatDate, loadingMessage, notifyError, stopLoadingMessage} from '@/assets/globalFunctions';
  import {BACKEND_HOST} from '../config';


  export default {
    data() {
      return {
        logs: [],
        searchQuery: '',
      };
    },
    created() {
      this.fetchLogs();
    },
    computed: {
      filteredLogs() {
        return this.logs.filter(log =>
          log.UserEmail && log.UserEmail.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    },
    methods: {
      async fetchLogs() {
        try {
          loadingMessage();
          const response = await fetch(`${BACKEND_HOST}user/get-user-logs`, {
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
          });

          if (!response.ok) {
            throw new Error('Logs could not be obtained');
          }

          const data = await response.json();
          this.logs = data;
          stopLoadingMessage();
        } catch (error) {
          stopLoadingMessage();
          notifyError(error.message);
        }
      },
      formatDate(date) {
        return formatDate(date);
      }
    },
  };
</script>
<style scoped>
#scrollableLogs {
  max-height: 720px;
  overflow-y: auto;
}
</style>