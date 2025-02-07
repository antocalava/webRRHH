<template>
  <main class="d-flex flex-fill">
    <div class="col-lg-5 mx-3">
      <h1 class="text-left mt-3 mb-2 fs-3 fw-bold col-6">Management</h1>

      <div class="d-flex position-sticky" style="top: 0; z-index: 1020; background-color: white;">
        <!-- Search employees -->
        <div id="searchContainer" class="col-md-6 pe-4 mt-1">
          <div class="input-group"> 
            <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
            <div class="flex-fill position-relative">
              <input type="search" class="form-control rounded-0" v-model="searchQuery" placeholder="Search employee..."
                @focusin="shouldShowSearchList = true" @focusout="shouldShowSearchList = false">
              <ul v-show="shouldShowSearchList" class="list">
                <li tabindex="0" class="list-group-item" v-for="employee in filteredEmployees" :key="employee.Email">
                  {{ employee.FullName }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Filter by department -->

        <div class="dropdown position-relative">
          <button class="btn btn-secondary bg-main dropdown-toggle" type="button" id="btn_filterTravels"
            data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fa-solid fa-filter mr-2"></i> Filter
          </button>

          <!-- Dropdown flotante -->
          <div class="dropdown-menu dropdown-menu-end p-3 shadow" aria-labelledby="btn_filterTravels"
            style="min-width: 300px; position: absolute; top: 100%; right: 0; z-index: 1000;">
            <div class="offcanvas-header">
              </div>
              <div class="offcanvas-body">
                <form>
                  <label class="mt-3">Department</label>
                  <select class="form-select mt-2 mb-2" id="city" v-model="selectedDepartmentFilter">
                    <option value="all" selected>All</option>
                    <option v-for="department in departments" :value="department.name">{{ department.name }}</option>
                  </select>
                </form>

                <button type="button" class="btn btn-secondary mt-4" @click="resetFilters()">Clean all filters</button>
              </div>
          </div>
        </div>
      </div>

      <!-- List employees -->
      <div class="d-flex flex-column gap-2 mt-3" style="overflow-y: auto; max-height: 750px">
        <div v-for="(employee, index) in filteredEmployees" :key="index" class="card mt-2">
          <div :id="employee.Email"></div>
          <div class="card-header titleHoliday mb-2 fs-5 d-flex justify-content-between align-items-center">
            <div>
              <i class="fa-solid fa-user"></i>
              <span class="ml-3">{{ employee.FullName }}</span>
            </div>
            <span>
              <i :id="'iconToggleCard_' + employee.Email" class="fa-solid fa-angle-down cursor-pointer"
                @click="toggleEmployeeCardDetails('employeeCard_' + employee.Email, 'iconToggleCard_' + employee.Email)"></i>
            </span>
          </div>
          <div :id="'employeeCard_' + employee.Email" class="card-body" style="display: none;">
            <h5 class="card-title"><i class="fa-solid fa-envelope"></i> {{ employee.Email }}</h5>

            <!-- CARDS EMPLOYEES -->
            <div class="mt-3 mb-2"
              v-if="employee.Travels && employee.Travels.length > 0 && filterTravels(employee.Travels).length > 0">
              <p class="card-subtitle mt-4 ml-2 text-muted">Travels requested</p>
              <div class="card-body" style="flex-flow: 1;overflow: auto;max-height: 300px;">

                <div v-for="(travel, vIndex) in filterTravels(employee.Travels)" :key="vIndex"
                  class="position-relative">
                  <div class="card card-body mt-3 mb-4">
                    <div id="cardContent" class="cursor-pointer"
                      @click="showTravelDetailsModal(employee.FullName, travel)" data-bs-target="#modalTravelDetails"
                      data-bs-toggle="modal">
                      <h6 class="card-subtitle mb-2 fs-5 titleHoliday col-10">{{ travel.reason }}</h6>

                      <div class="flex">
                        <div class="col-6">
                          <p class="card-text fs-6 fw-medium">
                            <i class="fa-solid fa-plane w-7"></i> {{ travel.destination }}
                          </p>
                          <p class="card-text fs-6 fw-medium">
                            <i class="fa-solid fa-calendar w-7"></i>
                            {{ dateFormat(travel.dateFrom) }} - {{ dateFormat(travel.dateTo) }}
                          </p>
                        </div>

                        <div class="col-6 text-end">
                          <button type="button" data-bs-target="#modalSignTravel" data-bs-toggle="modal"
                            class="btn btn-primary me-2" @click="actionStatus = 'SIGNED'; selectedTravel = travel">
                            Accept
                          </button>
                          <button type="button" data-bs-target="#modalRejectTravel" data-bs-toggle="modal"
                            class="btn btn-secondary" @click="actionStatus = 'REJECTED'; selectedTravel = travel">
                            Deny
                          </button>
                        </div>
                      </div>

                    </div>
                  </div>

                  <div class="position-absolute top-0 end-0 translate-middle p-1.5 px-4 rounded mt-1"
                    :style="{ backgroundColor: 'purple' }">
                    <i class="fa-solid fa-plane" style="color:white"></i>
                  </div>

                </div>
              </div>
            </div>

          </div>

        </div>
      </div>

    </div>

    <!-- CALENDAR + LEGEND -->
    <div class="col-lg-8 mt-1">
      <!-- calendar -->
      <div class="px-5 d-flex justify-content-center w-100">
        <div class="calendarContainer">
          <!-- legend -->
          <div class="info-container">
            <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
            <div class="legend-container">
              <div class="d-flex flex-row justify-content-center gap-3 font-small">
                <span class="ml-3">Travels:</span>
                <div class="d-flex align-items-center font-small">
                  <span class="legend-color mr-1 travels-signed"></span> Approved
                </div>
                <div class="d-flex align-items-center font-small">
                  <span class="legend-color mr-1 travels-semiSigned"></span> In process
                </div>
                <div class="d-flex align-items-center font-small">
                  <span class="legend-color mr-1 travels-notSigned"></span> Requested
                </div>
              </div>
            </div>
          </div>
          <v-calendar ref="datePicker" class="w-80" :attributes="attrs" :columns="3" :rows="3" id="calendar" />
        </div>
      </div>
    </div>

    <!-- Modal reject travel -->
    <div class="modal fade" id="modalRejectTravel" tabindex="-1" role="dialog"
      aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Reject travel</h5>
          </div>
          <div class="modal-body">
            Are you sure you want to reject this travel request?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="rejectTravel(selectedTravel.id, selectedTravel.userEmail)">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal sign travel -->
    <div class="modal fade" id="modalSignTravel" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Sign travel</h5>
          </div>
          <div class="modal-body">
            Are you sure you want to sign this travel request?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="signTravel(selectedTravel.id, selectedTravel.userEmail)">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal travel details -->
    <div class="modal fade" id="modalTravelDetails" tabindex="-1" role="dialog"
      aria-labelledby="modalTravelDetailsCenterTitle" aria-hidden="true">
      <div id="travelDetailsModal" class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-bold fs-4" id="modalTravelDetailsLongTitle">Travel details</h5>
            <div id="formButtonsContainer" class="ms-auto">
              <button id="btnCloseForm" class="btn btn-secondary w-fit" data-bs-dismiss="modal" aria-label="Close">
                <i class="fa-solid fa-x"></i>
              </button>
            </div>
          </div>
          <ModalTravelDetails v-if="selectedTravel" ref="travelDetails" />
        </div>
      </div>
    </div>

  </main>
</template>


<script>
import { notifyError, formatDate, notifySuccess, loadingMessage, stopLoadingMessage, hasUpdateManagement, updateManagement } from '@/assets/globalFunctions';
import { BACKEND_HOST } from '../config';
import ModalTravelDetails from '@/components/ModalTravelDetails.vue';
import { ref, computed } from 'vue';

export default {
  components: {
    ModalTravelDetails
  },
  data() {
    return {
      employees: [],
      attrs: [],
      departments: [],

      selectedDepartmentFilter: 'all',
      searchQuery: '',
      shouldShowSearchList: false,
     
      actionStatus: '',
      selectedTravel: null,
    }
  },
  created() {
    this.reload()
  },
  computed: {
    filteredEmployees() {
      let filtered = this.employees;
      filtered = this.employees.filter(user =>
        user.FullName && user.FullName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      if (this.selectedDepartmentFilter != 'all') {
        console.log(this.selectedDepartmentFilter)
        filtered = this.employees.filter(user =>
          user.Department == this.selectedDepartmentFilter
        );
      }
      return filtered;
    }
  },
  methods: {
    async reload() {
      loadingMessage();
      await this.fetchEmployees();
      await this.showNotification();
      this.printCalendar();
      stopLoadingMessage();
      if (this.departments.length == 0) this.fetchDepartments();
    },
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },
    filterTravels(employeeTravels) {
      let travels = []
      employeeTravels.forEach(travel => travels.push(travel))
      return travels.filter(travel =>
        travel.status == 'CREATED' && travel.managementSignature == null && travel.responsibleSignature != null
      );
    },
    resetFilters() {
      this.selectedDepartmentFilter = 'all';
    },
    dateFormat(date) {
      return formatDate(date);
    },

    /* Enseña las notificaciones en las cards **/
    async showNotification() {
      const unsignedEmployees = await this.fetchUnsignedEmployees();
      unsignedEmployees.forEach(employeeEmail => {
        updateManagement(true);
        let element = document.getElementById(employeeEmail);

        if (element) {
          element.classList.add('notification-dot');
        } else {
          console.error(`Element with ID '${employeeEmail}' not found`);
        }
      });
    },
    async fetchUnsignedEmployees() {
      try {
        const response = await fetch(`${BACKEND_HOST}travel/get-manager-has-unsigned`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Failed to load unsigned employees: ' + (error.message || error.state));
        }

        const data = await response.json();
        return data;
      } catch (error) {
        notifyError(error.message);
      }
    },

    /* Hide or expand the body of each employee's card */
    toggleEmployeeCardDetails(selectedCardBody_id, arrowIcon_id) {
      let card = document.getElementById(selectedCardBody_id)
      let icon = document.getElementById(arrowIcon_id)

      let cleanedString = selectedCardBody_id.replace('employeeCard_', '');

      if (document.getElementById(cleanedString).classList.contains('notification-dot')) {
        document.getElementById(cleanedString).classList.remove('notification-dot');
      }

      if (card.style.display == 'none') {
        icon.classList.remove('fa-angle-down')
        icon.classList.add('fa-angle-up')
        card.style.display = 'block'
      } else {
        icon.classList.remove('fa-angle-up')
        icon.classList.add('fa-angle-down')
        card.style.display = 'none'
      }
    },
    showTravelDetailsModal(userFullName, selectedTravel) {
      this.selectedTravel = selectedTravel;
      this.$nextTick(() => {
        this.$refs.travelDetails.openSelectedTravel(userFullName, selectedTravel)
      });
    },
    printCalendar() {
      this.attrs.splice(0);

      const weekends = ref([
        {
          description: 'weekend',
          isComplete: false,
          dates: { repeat: { weekdays: [1, 7] } }, // Every Saturday and Sunday
        },
      ]);

      this.attrs = computed(() => [
        ...weekends.value.map(day => ({
          dates: day.dates,
          content: {
            color: 'weekend',
            class: 'weekend',
          },
        })),
      ]);

      this.employees.forEach(employee => {
        employee.Travels.forEach(travel => {

          if (travel.status != "DELETED" && travel.status != "REJECTED") {
            const startDate = new Date(travel.dateFrom);
            const endDate = new Date(travel.dateTo);
            let highlightValue = { color: 'purple', fillMode: 'solid' }; //by default, solid purple for SIGNED

            if (travel.status == "CREATED") {
              if (travel.managementSignature != null || travel.responsibleSignature != null) {
                highlightValue = { color: 'purple', fillMode: 'light' }
              } else {
                highlightValue = { color: 'purple', fillMode: 'outline' }
              }
            }

            this.attrs.push({
              highlight: highlightValue,
              popover: {
                label: employee.FullName + ": " + travel.reason + " (" + travel.id + ")"
              },
              dates: [[startDate, endDate]],
            });
          }

        });
      });
    },

    async signTravel() {
      loadingMessage();
      await fetch(`${BACKEND_HOST}travel/sign-request-management`, {
        method: 'PUT',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          travel_id: this.selectedTravel.id,
          user_email: this.selectedTravel.userEmail
        })
      }).then(async response => {
        if (response.ok) {
          stopLoadingMessage();
          notifySuccess('Travel' + this.actionStatus.toLowerCase() + ' successfully!');
          this.reload()
        } else {
          const error = await response.json();
          throw new Error('Failed to sign travel: ' + (error.message || error.state));
        }
      }).catch(error => {
        stopLoadingMessage();
        notifyError(error.message);
      })
    },
    async rejectTravel() {
      loadingMessage();
      await fetch(`${BACKEND_HOST}travel/update-request-status`, {
        method: 'PUT',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          travel_id: this.selectedTravel.id,
          user_email: this.selectedTravel.userEmail,
          status: this.actionStatus
        })

      }).then(async response => {
        if (response.ok) {
          stopLoadingMessage();
          notifySuccess('Travel ' + this.actionStatus.toLowerCase() + ' successfully!');
          this.reload()
        } else {
          const error = await response.json();
          throw new Error('Failed to deny travel: ' + (error.message || error.state));
        }
      }).catch(error => {
        stopLoadingMessage();
        notifyError(error.message);
      })
    },
    async fetchEmployees() {
      await fetch(`${BACKEND_HOST}travel/get-manager-users-travels`, {
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        }
      })
        .then(async response => {
          if (!response.ok) {
            const error = await response.json();
            throw new Error('The employees could not be loaded: ' + (error.message || error.state));
          }
          return response.json();
        })
        .then(data => {
          this.employees = data;
        })
        .catch(error => {
          notifyError(error.message)
        });
    },
    async fetchDepartments() {
      loadingMessage();
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-departments`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Departments could not be load');
        }

        const data = await response.json();
        this.departments = data;
        stopLoadingMessage();
      } catch (error) {
        notifyError(error.message)
        stopLoadingMessage();
      }
    }
  }
}
</script>

<style scoped>
#travelDetailsModal {
  max-width: 1000px;
}

.legend-container {
  width: 90%;
  margin: 0 auto;
}

.legend-color {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: currentColor;
  /* Cambia esto según el color deseado */
}

.input-group {
  flex-wrap: nowrap !important;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.w-80 {
  width: 80%;
}

.notification-dot {
  position: absolute;
  top: -5px;
  right: -1px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: red;
}

.vc-light.vc-attr,
.vc-light .vc-attr {
  --vc-content-color: white;
  --vc-highlight-light-content-color: white;
}
</style>