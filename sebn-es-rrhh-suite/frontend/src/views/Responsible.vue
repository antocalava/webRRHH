<template>
  <main class="d-flex flex-fill">
    <div class="col-lg-5 mt-4 d-flex flex-column gap-3 px-1" style=" overflow-y: auto;">
      <h1 class="text-left fs-3 fw-bold col-6">Responsible</h1>

      <!-- Search employees -->
      <div id="searchContainer" class="col-md-7 pe-4 position-relative">
        <div class="input-group"> 
          <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
          <div class="flex-fill position-relative lessWidth">
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

      <!-- List employees -->
      <div v-for="(employee, index) in filteredEmployees" :key="index" class="card">
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
          <h5 class="card-title ml-2"><i class="fa-solid fa-envelope"></i> {{ employee.Email }}</h5>

          <!-- CARDS HOLIDAYS -->
          <div class="mt-3 mb-3"
            v-if="employee.Vacations && employee.Vacations.length > 0 && filterVacations(employee.Vacations).length > 0">
            <p class="card-subtitle mt-4 ml-2 text-muted">Holidays requested</p>
            <div class="card-body" style="flex-flow: 1;overflow: auto;max-height: 300px;">

              <div id="holidaysCards" v-for="(vacation, vIndex) in filterVacations(employee.Vacations)" :key="vIndex"
                class="position-relative">

                <div class="card card-body mt-3 mb-1">
                  <h6 class="card-subtitle mb-2 fs-5 titleHoliday">Holiday</h6>

                  <div class="d-flex">
                    <div class="col-6">
                      <p class="card-text fs-6 fw-medium" v-if="!vacation.partialDay">
                        <i class="fa-solid fa-calendar-days"></i>
                        {{ dateFormat(vacation.startingDay) }} - {{ dateFormat(vacation.finishingDay) }}
                      </p>
                      <p class="card-text fs-6 fw-medium" v-if="vacation.partialDay">
                        <i class="fa-solid fa-calendar-days"></i>
                        {{ dateFormat(vacation.startingDay) }}
                        ({{ Math.floor((vacation.totalQuantity / (hourConversionValue / 60)) / 60) }} h)
                      </p>
                    </div>

                    <div class="col-6 text-end">
                      <button type="button" data-bs-target="#modalSignHoliday" data-bs-toggle="modal"
                        class="btn btn-primary me-3" @click="selected.item = vacation; selected.employee = employee">
                        Sign
                      </button>
                      <button type="button" data-bs-target="#modalRejectHoliday" data-bs-toggle="modal"
                        class="btn btn-secondary" @click="selected.item = vacation; selected.employee = employee">
                        Deny
                      </button>
                    </div>

                  </div>
                </div>

                <div class="position-absolute top-0 end-0 translate-middle p-2 px-4 rounded mt-2"
                  :style="{ backgroundColor: this.color[vacation.status.toLowerCase()] }">
                  <i class="fa-solid fa-umbrella-beach" style="color:white"></i>
                </div>

              </div>
            </div>
          </div>


          <!-- CARDS TRAVELS -->
          <div class="mt-3 mb-2"
            v-if="employee.Travels && employee.Travels.length > 0 && filterTravels(employee.Travels).length > 0">
            <p class="card-subtitle mt-4 ml-2 text-muted">Travels requested</p>
            <div class="card-body" style="flex-flow: 1;overflow: auto;max-height: 300px;">

              <div id="travelsCards" v-for="(travel, vIndex) in filterTravels(employee.Travels)" :key="vIndex"
                class="position-relative">
                <div class="card card-body mt-3 mb-1">
                  <div id="cardContent" class="cursor-pointer"
                    @click="showTravelDetailsModal(employee.FullName, travel)" data-bs-target="#modalTravelDetails"
                    data-bs-toggle="modal">
                    <h6 class="card-subtitle mb-2 fs-5 titleHoliday col-10">{{ travel.reason }}</h6>

                    <div class="d-flex">
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
                         class="btn btn-primary me-2" @click="selected.item = travel; selected.employee = employee">
                          Sign
                        </button>
                        <button type="button" data-bs-target="#modalRejectTravel" data-bs-toggle="modal" 
                        class="btn btn-secondary" @click="selected.item = travel; selected.employee = employee">
                          Deny
                        </button>
                      </div>
                    </div>

                  </div>
                </div>

                <div class="position-absolute top-0 end-0 translate-middle p-2 px-4 rounded mt-2"
                  :style="{ backgroundColor: 'purple' }">
                  <i class="fa-solid fa-plane" style="color:white"></i>
                </div>

              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- CALENDAR -->
    <div class="col-lg-8 mt-1">
      <!-- calendar -->
      <div class="px-5 d-flex justify-content-center w-100">
        <div class="calendarContainer">
          <!-- legend -->
          <div class="info-container">
            <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
            <div class="legend-container">
              <div class="d-flex flex-row justify-content-center gap-3 mb-2 font-small">
                <span>Holidays:</span>
                <div class="d-flex align-items-center font-small">
                  <span class="legend-color mr-1 vacations-signed"></span> Signed
                </div>
                <div class="d-flex align-items-center font-small">
                  <span class="legend-color mr-1 vacations-notSigned"></span> Requested
                </div>
              </div>

              <div class="d-flex flex-row justify-content-center gap-3 font-small">
                <span>Travels:</span>
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


    <!-- Modal Sign holidays -->
    <div class="modal fade" id="modalSignHoliday" tabindex="-1" role="dialog" 
      aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Sign holiday
            </h5>
          </div>
          <div class="modal-body">
            Are you sure you want to sign this holiday?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="actionStatus = 'SIGNED'; changeStatusHoliday()">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Reject holidays -->
    <div class="modal fade" id="modalRejectHoliday" tabindex="-1" role="dialog"
      aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Reject holiday
            </h5>
          </div>
          <div class="modal-body">
            Are you sure you want to reject this holiday?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="actionStatus = 'REJECTED'; changeStatusHoliday()">
              Accept 
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal sign travels -->
    <div class="modal fade" id="modalSignTravel" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
    aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Sign travel
            </h5>
          </div>
          <div class="modal-body">
            Are you sure you want to sign this travel?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="actionStatus = 'SIGNED'; updateTravelStatus()">
              Accept 
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal reject travels -->
    <div class="modal fade" id="modalRejectTravel" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Reject travel
            </h5>
          </div>
          <div class="modal-body">
            Are you sure you want to reject this travel?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="actionStatus = 'REJECTED'; updateTravelStatus()">
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
import { notifyError, formatDate, notifySuccess, loadingMessage, stopLoadingMessage, hasUpdateResponsible, updateResponsible } from '@/assets/globalFunctions';
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
      selectedTravel: null,
      color: { 'created': 'orange', 'signed': 'green' },
      attrs: [],

      searchQuery: '',
      shouldShowSearchList: false,

      userWorkingHours: 0,
      hourConversionValue: 0,

      actionStatus: '',
      selected: {
        employee: {},
        item: {}
      }
    }
  },
  created() {
    this.fetchUserWorkingHours();
    this.reload()
  },
  computed: {
    filteredEmployees() {
      return this.employees.filter(user =>
        user.FullName && user.FullName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async reload() {
      this.selected = {}
      loadingMessage();
      await this.fetchEmployees();
      await this.showNotification();
      await this.printCalendar();
      stopLoadingMessage();
    },
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },
    filterVacations(employeeVacations) {
      let vacations = []
      employeeVacations.forEach(vacation => vacations.push(vacation))
      return employeeVacations.filter(vacation =>
        vacation.status == 'CREATED'
      );
    },
    filterTravels(employeeTravels) {
      let travels = []
      employeeTravels.forEach(travel => travels.push(travel))
      return travels.filter(travel =>
        travel.status == 'CREATED' && travel.responsibleSignature == null
      );
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
    async showNotification() {
      const unsignedEmployees = await this.fetchUnsignedEmployees();
      if (unsignedEmployees.length > 0) {
        updateResponsible(true);
        unsignedEmployees.forEach(employeeEmail => {
          let element = document.getElementById(employeeEmail);

          if (element) {
            element.classList.add('notification-dot');
          } else {
            console.error(`Element with ID '${employeeEmail}' not found`);
          }
        });
      }
    },
    async fetchUnsignedEmployees() {
      try {
        const response = await fetch(`${BACKEND_HOST}user/get-responsible-has-unsigned`, {
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
    showTravelDetailsModal(userFullName, selectedTravel) {
      this.selectedTravel = selectedTravel;
      this.$nextTick(() => {
        this.$refs.travelDetails.openSelectedTravel(userFullName, selectedTravel)
      });
    },
    async fetchEmployees() {
      await fetch(`${BACKEND_HOST}user/get-bellow-employees`, {
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
          this.employees = data.Employees;
        })
        .catch(error => {
          notifyError(error.message)
        });
    },
    dateFormat(date) {
      return formatDate(date);
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
        if (employee.Vacations) {
          employee.Vacations.forEach(vacation => {
            if (vacation.status != "DELETED" && vacation.status != "REJECTED") {
              const startDate = new Date(vacation.startingDay);
              const endDate = new Date(vacation.finishingDay);
              let highlightValue = 'yellow' //by default, yellow solid for SIGNED

              if (vacation.status == "CREATED") highlightValue = { color: 'yellow', fillMode: 'outline' }

              this.attrs.push({
                highlight: highlightValue,
                popover: {
                  label: employee.FullName + ": Holiday"
                },
                dates: [[startDate, endDate]],
              });
            }
          });
        }
      });

      this.employees.forEach(employee => {
        if (employee.Travels) {
          employee.Travels.forEach(travel => {
            if (travel.status != "DELETED" && travel.status != "REJECTED") {
              const startDate = new Date(travel.dateFrom);
              const endDate = new Date(travel.dateTo);
              let highlightValue = { color: 'purple', fillMode: 'solid' }; //by default, solid purple for SIGNED

              if (travel.status == "CREATED") {
                if (travel.responsibleSignature != null || travel.managementSignature != null) {
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
        }
      });
    },
    async changeStatusHoliday() {
      loadingMessage();
      await fetch(`${BACKEND_HOST}holiday/change-request-status`, {
        method: 'POST',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: this.selected.item.id,
          status: this.actionStatus,
          email: this.selected.employee.Email,
          start: this.selected.item.startingDay,
          finish: this.selected.item.finishingDay
        })

      }).then(async response => {
        if (response.ok) {
          stopLoadingMessage();
          notifySuccess('Holiday ' + this.actionStatus.toLocaleLowerCase() + ' successfully!');
          this.reload()
        } else {
          const error = await response.json();
          throw new Error("Failed to change status of selected holiday: " + (error.message || error.state));
        }
      }).catch(error => {
        stopLoadingMessage();
        notifyError(error.message);
      })
    },
    updateTravelStatus() {
      loadingMessage();
      switch (this.actionStatus) {
        case 'REJECTED':
          this.rejectTravel(this.selected.item.id, this.selected.employee.Email)
          break;
        case 'SIGNED':
          this.signTravel(this.selected.item.id, this.selected.employee.Email)
          break;
      }
      stopLoadingMessage();
    },
    async signTravel(id, email) {
      await fetch(`${BACKEND_HOST}travel/sign-request-responsible`, {
        method: 'PUT',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          travel_id: id,
          user_email: email
        })

      }).then(async response => {
        if (response.ok) {
          notifySuccess('Travel ' + this.actionStatus.toLocaleLowerCase() + ' successfully!');
          this.reload()
        } else {
          const error = await response.json();
          throw new Error('Failed to sign travel: ' + (error.message || error.state));
        }
      }).catch(error => {
        notifyError(error.message);
      })
    },
    async rejectTravel(id, email) {
      await fetch(`${BACKEND_HOST}travel/update-request-status`, {
        method: 'PUT',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          travel_id: id,
          user_email: email,
          status: this.actionStatus
        })

      }).then(async response => {
        if (response.ok) {
          notifySuccess('Travel ' + this.actionStatus.toLocaleLowerCase() + ' successfully!');
          this.reload()
        } else {
          const error = await response.json();
          throw new Error('Failed to deny travel: ' + (error.message || error.state));
        }
      }).catch(error => {
        notifyError(error.message);
      })
    },
    async fetchUserWorkingHours() {
      try {
        loadingMessage();
        const response = await fetch(`${BACKEND_HOST}user/get-user-working-hours`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Unable to load user city: ' + (error.message || error.state));
        }

        const data = await response.json();
        this.userWorkingHours = data[0];
        this.hourConversionValue = (1 / this.userWorkingHours).toFixed(3)
        stopLoadingMessage();
      } catch (error) {
        console.error(error);
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

.mb-4 {
  margin-bottom: 1.5rem;
}

.w-80 {
  width: 80%;
}

.legend-color {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: currentColor;
}

.notification-dot {
  position: absolute;
  top: -4px;
  right: -4px;
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