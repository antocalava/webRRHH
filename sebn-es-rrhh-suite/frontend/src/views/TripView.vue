<template>
  <main class="container d-block mt-3 mx-4">

    <div id="topControlsContainer" class="col d-flex">
      <!-- Título y botones -->
      <h1 class="text-left mb-2 mt-3 fs-3 fw-bold col-6">My travels</h1>
    </div>

    <div id="listAndFormContainer" clasS="row d-flex gap-4">

      <!-- LEFT SIDE: LIST OF TRAVELS + top buttons -->
      <div class="card-body" style="width: 45%;">

        <!-- list actions buttons -->
        <div class="d-flex mt-1" style="top: 0; background-color: white;">
          <!-- Search employees -->
          <div id="searchContainer" class="col-md-6 pe-4 position-relative lessWidth">
            <div class="input-group">
              <span class="input-group-text iconDissapear-md"><i class="fa-solid fa-magnifying-glass"></i></span>
              <div class="flex-fill position-relative lessWidth">
                <input type="search" id="searchTravel" class="form-control rounded-0 lessWidth" v-model="searchQuery"
                  placeholder="Search travel title..." @focusin="shouldShowSearchList = true"
                  @focusout="shouldShowSearchList = false">
                <ul v-show="shouldShowSearchList" class="list">
                  <li tabindex="0" class="list-group-item" v-for="travel in filteredTravels" :key="travel.id">
                    {{ travel.reason }}
                  </li>
                </ul>
              </div>

            </div>
          </div>

          <!-- Filter by destination, date range and status -->
          <div class="d-flex justify-content-between align-items-center">
            <div class="dropdown position-relative">
              <button class="btn btn-secondary bg-main dropdown-toggle" type="button" id="btn_filterTravels"
                data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa-solid fa-filter mr-2"></i> Filter
              </button>

              <!-- Dropdown flotante -->
              <div class="dropdown-menu dropdown-menu-end p-4 shadow" aria-labelledby="btn_filterTravels"
                style="min-width: 300px; position: absolute; top: 100%; right: 0; z-index: 1000;">
                <form>
                  <!-- Filtro por Estado -->
                  <div class="mb-3">
                    <label for="statusFilter" class="form-label">Status</label>
                    <select class="form-select" id="statusFilter" v-model="selectedStatusFilter">
                      <option value="All" selected>All</option>
                      <option value="CREATED">Requested</option>
                      <option value="SIGNED">Signed</option>
                      <option value="REJECTED">Rejected</option>
                    </select>
                  </div>

                  <!-- Filtro por Destino -->
                  <div class="mb-3">
                    <label for="destinationFilterContainer" class="form-label">Destination</label>
                    <select id="destinationFilterContainer" class="form-select" v-model="selectedDestinationFilter">
                      <option value="All" selected>All</option>
                      <CountryOptions />
                    </select>
                  </div>

                  <!-- Filtro por Rango de Fechas -->
                  <div class="mb-3">
                    <label for="dateRangeFilter" class="form-label">Date range</label>
                    <div class="row">
                      <div class="col-6">
                        <input type="date" class="form-control" id="dateFromFilter"
                          v-model="selectedDateRangeFilter[0]" />
                      </div>
                      <div class="col-6">
                        <input type="date" class="form-control" id="dateToFilter"
                          v-model="selectedDateRangeFilter[1]" />
                      </div>
                    </div>
                  </div>

                  <!-- Botón de limpiar filtros -->
                  <div class="d-grid">
                    <button type="button" class="btn btn-secondary mt-3" @click="resetFilters()">Clean all
                      filters</button>
                  </div>
                </form>
              </div>
            </div>
            <button id="btn_OpenReqForm" class="btn btn-primary bg-main" @click="openTravelRequest()" disabled>
              <i class="fa-solid fa-plus-circle mr-3"></i>Create request
            </button>
          </div>
        </div>


        <!-- Travels list -->
        <div id="travelListContainer" class="mt-2 py-2 pr-1">
          <div v-for="(travel, vIndex) in filteredTravels.sort((a, b) => new Date(b.dateFrom) - new Date(a.dateFrom))"
            :key="vIndex" class="position-relative">
            <div>
              <div class="card card-body mt-2 mb-4">
                <h6 class="card-subtitle mb-2 fs-5 travlTitle fw-bolder">{{ travel.reason }}</h6>
                <div class="flex">
                  <!-- LEFT HALF OF CARD -->
                  <div class="col-5">
                    <p class="card-text fs-6 fw-medium">
                      <i class="fa-solid fa-plane w-7"></i> {{ travel.destination }}
                    </p>
                    <p class="card-text fs-6 fw-medium">
                      <i class="fa-solid fa-calendar w-7"></i>
                      {{ formatDate(travel.dateFrom) }} - {{ formatDate(travel.dateTo) }}
                    </p>
                  </div>

                  <!-- RIGHT HALF OF CARD -->
                  <div class="col-7">
                    <!-- signatures -->
                    <div class="row mb-2 mx-2" style="border-bottom: solid lightgray 2px;">
                      <div class="form-check align-items-center gap-2 col-6">
                        <input class="form-check-input" type="checkbox" :id="'managementSign_' + travel.id"
                          :checked="travel.managementSignature !== null" disabled />
                        <label class="form-check-label" :for="'managementSign_' + travel.id">Management</label>
                      </div>

                      <div class="form-check align-items-center gap-2 col-6">
                        <input class="form-check-input" type="checkbox" :id="'responsibleSign_' + travel.id"
                          :checked="travel.responsibleSignature !== null" disabled />
                        <label class="form-check-label" :for="'responsibleSign_' + travel.id">Responsible</label>
                      </div>
                    </div>

                    <!-- button open details-->
                    <div class="row mx-2">
                      <button id="btn_OpenDetailsForm" class="btn btn-primary h-10"
                        @click="openTravelDetails(travel, true)">Open details</button>
                    </div>

                  </div>
                </div>
              </div>

              <div class="position-absolute top-0 end-0 translate-middle p-0.5 border rounded"
                :style="{ backgroundColor: statusColor[travel.status] }" :title="travel.status"
                style="color: white; font-weight: 500; width:20%; text-align: center; font-size: small">
                ID: {{ travel.id }}
              </div>

            </div>
          </div>
        </div>
      </div>


      <!-- RIGHT SIDE: CONTENT DISPLAY SPACE-->
      <div id="contentDisplayContainer" class="card-body" style="width: 50%;">

        <!-- Travel form -->
        <div id="travelForm" class="px-10 pb-10" style="display: none;">
          <form @submit.prevent="">

            <!-- Buttons at the top -->
            <div id="formButtonsContainer" class="d-flex">
              <button id="btnEditForm" class="btn btn-primary bg-main mx-2" @click="editTravelDetails()"
                v-show="isViewingTravelDetails && !isEditingDetails">
                <i class="fa-solid fa-pencil mr-3"></i>Edit
              </button>

              <button type="submit" v-show="isEditingDetails" id="btnSaveChangesForm"
                class="btn btn-primary bg-main mx-2" @click.prevent="validateForm">
                <i class="fa-solid fa-check mr-3"></i>Save
              </button>

              <button id="btnDeleteForm" class="btn btn-secondary bg-main mx-2"
                v-show="isViewingTravelDetails && !isEditingDetails" data-bs-target="#modalDeleteTravel"
                data-bs-toggle="modal">
                <i class="fa-solid fa-trash mr-3"></i>Delete
              </button>

              <button v-show="isCreatingRequest && isEditingDetails == false" id="btnSubmitForm" type="submit"
                class="btn btn-primary" @click.prevent="validateForm">
                <i class="fa-solid fa-paper-plane mr-3"></i>Submit request
              </button>

              <button id="btnCloseForm" class="btn btn-secondary bg-main mx-2" @click="closeForm()">
                <i class="fa-solid fa-x mr-3"></i>Cancel
              </button>
            </div>

            <h1 id="formTitle" class="text-center mt-4 mb-3 fs-4"></h1>

            <div id="formFieldsContainer">
              <!-- name & cost center -->
              <div class="mb-3 row">
                <div class="col-md-6">
                  <label for="userFullName" class="form-label required">Employee's name</label>
                  <input type="text" class="form-control" id="userFullName" v-model="form.userFullName" readonly
                    disabled required />
                </div>
                <div class="col-md-6">
                  <label for="costCenter" class="form-label required">Cost center</label>
                  <input type="number" step="1" min="0" class="form-control formEditableField" id="costCenter" disabled
                    v-model="form.costCenter" required>
                </div>
              </div>

              <!-- dates & duration -->
              <div class="row mb-3" id="datesContainer">
                <div class="col-md-4">
                  <label for="dateFrom" class="form-label required">Date from</label>
                  <input type="date" class="form-control formEditableField" id="dateFrom"  v-model="form.dateFrom"
                    required @change="calcDayAmount" />
                </div>
                <div class="col-md-4">
                  <label for="dateTo" class="form-label required">Date to</label>
                  <input type="date" class="form-control formEditableField" id="dateTo" v-model="form.dateTo" required
                    @change="calcDayAmount" />
                </div>
                <div class="col-md-4">
                  <label for="dayAmount" class="form-label">Day amount</label>
                  <input type="number" class="form-control" id="dayAmount" v-model="form.dayAmount" min="0" readonly
                    disabled>
                </div>
              </div>

              <!-- destination -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="destination" class="form-label required">Destination country</label>
                  <select id="destination" class="form-control formEditableField" v-model="form.destination" required>
                    <option value="" selcted disabled hidden>Select a country...</option>
                    <CountryOptions />
                  </select>
                </div>

                <div class="col-md-6">
                  <label for="address" class="form-label required">Address/es</label>
                  <textarea type="text" class="form-control formEditableField" id="address" v-model="form.address"
                    style="height: 40px;" maxlength="140"></textarea>
                </div>
              </div>

              <div class="row mb-3">
                <!-- added value-->
                <div class="col-md-6">
                  <label class="form-label">Trip creates added value</label>
                  <div>
                    <div class="form-check form-check-inline d-inline-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="radio" name="addedValueRadio"
                        id="addedValueTrue" value="1" v-model="form.addedValue" />
                      <label class="form-check-label" for="addedValueTrue">Yes</label>
                    </div>
                    <div class="form-check form-check-inline d-inline-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="radio" name="addedValueRadio"
                        id="addedValueFalse" value="0" v-model="form.addedValue" />
                      <label class="form-check-label" for="addedValueFalse">No</label>
                    </div>
                  </div>
                </div>

                <!-- advance payment-->
                <div class=" col-md-6 d-block">
                  <div class="row">
                    <label class="form-check-label" for="advancePaymentCheck" style="width:fit-content">
                      Request advance payment?</label>
                    <input class="form-check-input formEditableField" type="checkbox" id="advancePaymentCheck" value="1"
                      v-model="form.advancePayment" />
                  </div>

                  <div v-if="form.advancePayment" class="row">
                    <label class="form-label required" for="advancePaymentAmount"
                      style="width:fit-content">Amount</label>
                    <input class="form-control formEditableField" type="number" id="advancePaymentAmount" disabled
                      v-model="form.advancePaymentAmount" min="0" value="0" step="any" required style="width:50%" />
                    <!-- tanto el punto como la coma te lo transforman en DECIMAL-->
                  </div>
                </div>
              </div>

              <!-- reason -->
              <div class="col-mb-12 mb-3">
                <label for="reason" class="form-label required">Travel reason</label>
                <textarea class="form-control formEditableField" id="reason" v-model="form.reason" rows="3"
                  required></textarea>
              </div>

              <!-- transport -->
              <div class="row mb-3">
                <label class="form-label">Means of transport:</label>
                <div class="row" id="transportContainer">
                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="Plane"
                        v-model="form.transport['Plane']" />
                      <label class="form-check-label" for="Plane">Plane</label>
                    </div>
                  </div>

                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="Train"
                        v-model="form.transport['Train']" />
                      <label class="form-check-label" for="Train">Train</label>
                    </div>
                  </div>

                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="RentCar"
                        v-model="form.transport['RentCar']" />
                      <label class="form-check-label" for="RentCar">Rented vehicle</label>
                    </div>
                  </div>

                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="BusinessCar"
                        v-model="form.transport['BusinessCar']" />
                      <label class="form-check-label" for="BusinessCar">Business vehicle</label>
                    </div>
                  </div>

                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="PrivateCar"
                        v-model="form.transport['PrivateCar']" />
                      <label class="form-check-label" for="PrivateCar">Private vehicle</label>
                    </div>
                  </div>

                  <div class="col-6 col-md-4 col-lg-4">
                    <div class="form-check d-flex align-items-center gap-2">
                      <input class="form-check-input formEditableField" type="checkbox" id="Taxi"
                        v-model="form.transport['Taxi']" />
                      <label class="form-check-label" for="Taxi">Taxi - pick-up</label>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </form>
        </div>

        <!-- CALENDAR + LEGEND -->
        <div v-if="isCreatingRequest == false && isViewingTravelDetails == false && isEditingDetails == false"
          id="travelCalendar">
          <div class="d-flex flex-column calendar-container">
            <!-- Legend -->
            <div class="info-container">
              <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
              <div class="legend-container">
                <div class="d-flex flex-row justify-content-center gap-3 font-small ml-3">
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
            <!-- Contenedor del calendario -->
            <div class="d-flex w-100">
              <VCalendar ref="datePicker" class="w-100" :attributes="attrs" :columns="2" :rows="3" id="calendar">
                <template #day-popover="{ day, format, masks, attributes }">
                  <div class="small ho-user text-center text-capitalize">
                    {{ format(day.date, masks.dayPopover) }}
                  </div>
                  {{ console.log(attributes) }}
                  <div v-for="{ key, highlight, popover } in attributes" :key="key">
                    <div>
                      <span
                        :class="highlight.base.class"></span>
                      <span class="small">{{ popover.label }}</span>
                    </div>
                  </div>
                </template>
              </VCalendar>
            </div>
          </div>
        </div>



      </div>
    </div>

    <!-- MODALS -->

    <!-- confirm delete travel -->
    <div class="modal fade" id="modalDeleteTravel" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Delete travel</h5>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this trip?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="deleteTravel()">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- modal to confirm IF YOU WANT TO CLOSE WITHOUT SAVING (while editing)-->
    <div class="modal fade" id="modalConfirmCancelEditTravel" tabindex="-1" role="dialog"
      aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Edit trip details</h5>
          </div>
          <div class="modal-body">
            You may have unsaved changes.
            Are you sure you want to close without saving?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="isEditingDetails = false, closeForm()">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

  </main>
</template>

<script>
import CountryOptions from '@/components/CountrySelect.vue';
import { notifyError, notifySuccess, loadingMessage, stopLoadingMessage, formatDate, formatDate2, getUsername } from "@/assets/globalFunctions";
import { BACKEND_HOST } from '../config';
import { differenceInDays } from 'date-fns';
import { ref, computed } from 'vue';

export default {
  components: {
    CountryOptions
  },
  data() {

    return {
      selectedTravel: {},
      travels: [],
      userCostCenter: null,
      attrs: [],
      statusColor: { 'CREATED': '#e7ad41', 'SIGNED': '#7ab870', 'REJECTED': '#c75353' },
      transportNamesOrder: ['Plane', 'Train', 'RentCar', 'BusinessCar', 'PrivateCar', 'Taxi'],

      searchQuery: '',
      shouldShowSearchList: false,

      selectedStatusFilter: 'All',
      selectedDestinationFilter: 'All',
      selectedDateRangeFilter: ['', ''],
      selectedCountry: null, //default for destinations selects

      reloadCurrentForm: true,
      isCreatingRequest: false,
      isViewingTravelDetails: false,
      isEditingDetails: false,
      formIsValid: true,
      form: {
        userFullName: getUsername(),
        destination: '',
        address: '',
        costCenter: this.userCostCenter,
        dateFrom: '',
        dateTo: '',
        dayAmount: 0,
        addedValue: 0, //false
        advancePayment: 0, //false
        advancePaymentAmount: 0.00,
        reason: '',
        transport: { 'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }
        //extraDocumentation: '' //TODO: this has to be checked here?? if not here, where?
      }
    };
  },
  created() {
    this.reload()
  },
  computed: {
    filteredTravels() {
      let filtered = this.travels;
      filtered = this.travels.filter(travel =>
        travel.status != 'DELETED' && (
          travel.reason && travel.reason.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      );

      //PARA QUE SE APLIQUEN LOS FILTROS SELECCIONADOS:
      if (this.selectedStatusFilter != 'All') {
        filtered = this.travels.filter(travel =>
          travel.status == this.selectedStatusFilter
        );
      }
      if (this.selectedDestinationFilter != 'All') {
        filtered = this.travels.filter(travel =>
          travel.destination == this.selectedDestinationFilter
        );
      }
      if (this.selectedDateRangeFilter[0] != '' && this.selectedDateRangeFilter[1] != '') {
        const [startDate, endDate] = this.selectedDateRangeFilter;

        filtered = this.travels.filter(travel => {
          const travelStart = new Date(travel.dateFrom);
          const travelEnd = new Date(travel.dateTo);
          const rangeStart = new Date(startDate);
          const rangeEnd = new Date(endDate);

          return (
            (travelStart >= rangeStart && travelStart <= rangeEnd) ||
            (travelEnd >= rangeStart && travelEnd <= rangeEnd)
          );
        });
      }
      return filtered;
    }
  },
  methods: {
    async reload() {
      if (!this.isEditingDetails) this.closeForm();
      await this.fecthUserCostCenter();
      await this.fetchTravels(); //they're printed automatically
      this.printTravelsCalendar();

      //enable creating once everything is loaded
      document.getElementById("btn_OpenReqForm").disabled = false
    },
    formatDate(date) {
      return formatDate(date);
    },
    resetFilters() {
      this.selectedStatusFilter = 'All';
      this.selectedDestinationFilter = 'All';
      this.selectedDateRangeFilter = ['', ''];
    },


    /** TRAVELS LIST METHODS: **/
    async fetchTravels() {
      loadingMessage();
      await fetch(`${BACKEND_HOST}travel/get-travels`, {
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        }
      })
        .then(async response => {
          if (!response.ok) {
            const error = await response.json();
            throw new Error('The travels could not be loaded: ' + (error.message || error.state));
          }
          return response.json();
        })
        .then(data => {
          this.travels = data;
          stopLoadingMessage();
        })
        .catch(error => {
          notifyError(error.message)
          stopLoadingMessage();
        });
    },


    /** TRAVELS CALENDAR METHODS: **/
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },
    printTravelsCalendar() {
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

      this.travels.forEach(travel => {
        if (travel.status !== "DELETED" && travel.status !== "REJECTED") {
          const startDate = new Date(travel.dateFrom);
          const endDate = new Date(travel.dateTo);
          let highlightValue = { color: 'purple', fillMode: 'solid', class: 'purple' }; // Por defecto, solid purple para SIGNED

          if (travel.status === "CREATED") {
            if (travel.managementSignature != null || travel.responsibleSignature != null) {
              highlightValue = { color: 'purple', fillMode: 'light', class: 'lightPurple' };
            } else {
              highlightValue = { color: 'purple', fillMode: 'outline', class: 'borderPurple' };
            }
          }

          this.attrs.push({
            highlight: highlightValue,
            popover: {
              label: `${travel.id}: ${travel.reason}`
            },
            dates: [[startDate, endDate]],
          });
        }
      });
    },


    /** TRAVELS FORMS METHODS: **/
    async openTravelDetails(selectedTravel, reloadForm) {
      // When you're editing one travel and you want to open another or the same one
      if (this.isEditingDetails && reloadForm) {
        // To prevent discarding changes by mistake, we show modal to confirm
        const modal = new bootstrap.Modal(document.getElementById('modalConfirmCancelEditTravel'));
        modal.show();
      } else {

        //After saving changes when editing, we dont reload but we disable the fields
        if (this.isEditingDetails && !reloadForm) {
          this.isEditingDetails = false;
          this.reloadCurrentForm = reloadForm;
          this.showForm();

        } else { //For all other cases, show selected travel normally
          this.isCreatingRequest = false;
          this.isViewingTravelDetails = true;
          this.isEditingDetails = false;
          this.reloadCurrentForm = reloadForm;

          //Avoid reload form when open details of same travel
          if (selectedTravel.id != this.selectedTravel.id && reloadForm == true) {
            this.selectedTravel = selectedTravel;
            this.showForm();
          }
        }
      }

    },
    //user edits the trip they're currently viewing
    editTravelDetails() {
      this.isCreatingRequest = false;
      this.isViewingTravelDetails = true;
      this.isEditingDetails = true;
      this.showForm();
    },
    //user creates a NEW request
    async openTravelRequest() {
      this.isCreatingRequest = true;
      this.isViewingTravelDetails = false;
      this.isEditingDetails = false;
      this.showForm();
    },
    /**
     * To switch from view/edit travel details form
     * to create new travel request form
     */
    showForm() {
      let formTitle = document.getElementById("formTitle");
      let travelForm = document.getElementById("travelForm");
      let formEditableFields = document.querySelectorAll('.formEditableField');
      
      if (travelForm.style.display == "none") {
        travelForm.style.display = "block";
      }

      if (this.isCreatingRequest) {
        formTitle.textContent = "Trip request";
        this.resetForm()
        this.form.costCenter = this.userCostCenter;
      } else { //isViewing
        formTitle.textContent = "Trip details";

        if (!this.isEditingDetails) {
          if (this.reloadCurrentForm) {
            this.resetForm(); //we clean previous info when viewing a different travel
            this.loadDetailsPlaceholders(); //we keep data loaded while editing
          }
        }
      }

      if (this.isViewingTravelDetails && !this.isEditingDetails) {
        if(document.getElementById("advancePaymentCheck").checked) {
          let amountField = document.getElementById("advancePaymentAmount");
          if(amountField){ amountField.disabled = true};
        }
        formEditableFields.forEach(element => {
          element.disabled = true;
        });
      } else {
        //all fields are disabled if they cant be edited
        formEditableFields.forEach(element => {
          element.disabled = false;
        });
        if (document.getElementById("advancePaymentCheck").checked) {
          let amountField = document.getElementById("advancePaymentAmount");
          //make all fields posible to edit
          if (amountField) { amountField.disabled = false };
        }
      }
    },
    closeForm() {
      if (this.isEditingDetails) {
        const modal = new bootstrap.Modal(document.getElementById('modalConfirmCancelEditTravel'));
        modal.show();
      } else {
        this.isCreatingRequest = false;
        this.isViewingTravelDetails = false;
        this.isEditingDetails = false;
        this.selectedTravel = {};

        let formElement = document.getElementById("travelForm");
        if (formElement) formElement.style.display = "none";
      }
    },
    async loadDetailsPlaceholders() {
      this.form = {
        userFullName: this.form.userFullName,
        destination: this.selectedTravel.destination,
        address: this.selectedTravel.address,
        costCenter: this.selectedTravel.costCenter,
        dateFrom: formatDate2(this.selectedTravel.dateFrom),
        dateTo: formatDate2(this.selectedTravel.dateTo),
        dayAmount: this.selectedTravel.dayAmount,
        addedValue: this.selectedTravel.addedValue,
        advancePayment: !!this.selectedTravel.advancePayment,
        advancePaymentAmount: this.selectedTravel.advancePaymentAmount,
        reason: this.selectedTravel.reason,
        transport: this.transformTransportStringtoMap(this.selectedTravel.transport)
      }
    },
    resetForm() {
      this.form = {
        userFullName: this.form.userFullName,
        destination: '',
        address: '',
        costCenter: '',
        dateFrom: '',
        dateTo: '',
        dayAmount: 0,
        addedValue: 0, //false
        advancePayment: 0, //false
        advancePaymentAmount: 0.00,
        reason: '',
        transport: { 'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }
      }
      this.cleanFormValidationErrorFields();
    },
    calcDayAmount() {
      this.cleanFormValidationErrorFields();
      if (this.form.dateFrom && this.form.dateTo) {
        const dateFrom = new Date(this.form.dateFrom);
        const dateTo = new Date(this.form.dateTo);

        const dayAmount = differenceInDays(dateTo, dateFrom) + 1;

        this.form.dayAmount = dayAmount;
        if (dayAmount < 0) this.formValidationError("datesContainer", "Invalid date range: day amount is negative")

      } else {
        this.form.dayAmount = 0;
      }
    },
    /**
     * Indicate why is there a validation error and where is its source
     * @val message --> message to show in error
     * @val elementId --> document element to highlight (can be null)
     */
    formValidationError(elementId, message) {
      this.formIsValid = false;
      if (elementId) document.getElementById(elementId).classList.add("hasError")
      let error = new Error(message)
      notifyError(error.message);
      console.error(error.message)
    },
    /**
     * Each time the user corrects a mistake in the form, 
     * all fields would go back to normal BEFORE each reattempt at validating form
     */
    cleanFormValidationErrorFields() {
      const elements = document.querySelectorAll('.hasError');
      elements.forEach(element => {
        element.classList.remove('hasError');
      });
      this.formIsValid = true;
    },
    validateForm() {
      try {
        this.cleanFormValidationErrorFields()

        if (this.form.costCenter == null) this.formValidationError("costCenter", "Cost center can not be empty")
        if (this.form.dateFrom == '') this.formValidationError("dateFrom", "Date From can not be empty")
        if (this.form.dateTo == '') this.formValidationError("dateTo", "Date To can not be empty")
        if (this.form.destination.trim() == '') this.formValidationError("destination", "Destination country can not be empty")
        if (this.form.advancePayment && this.form.advancePaymentAmount == 0) this.formValidationError("advancePaymentAmount", "The advance payment amount can not be 0")
        if (this.form.reason.trim() == '') this.formValidationError("reason", "Reason can not be empty")

        //if form is valid, do submit request
        if (this.formIsValid) {
          if (this.isCreatingRequest) this.submitTravelRequest()
          if (this.isEditingDetails) this.updateTravel()
        }
      } catch (error) {
        console.error(error);
      }
    },
    async deleteTravel() {
      let pData = {
        'user_email': null,
        'travel_id': this.selectedTravel.id,
        'status': 'DELETED'
      }

      try {
        const response = await fetch(`${BACKEND_HOST}travel/update-request-status`, {
          method: 'PUT',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Could not delete the trip: " + error.message);
        }

        notifySuccess("Trip deleted succesfully!")
        this.reload();

      } catch (error) {
        notifyError(error.message);
        console.error(error.message)
      }
    },
    /**
     * Gets the current information in the form and 
     * packs it up in 'data' to feed it to the API
     * when submitting a new request or updating/editing an existing one
     */
    collectFormData() {
      const destination = this.form.destination;
      const address = this.form.address;
      const costCenter = this.form.costCenter;
      const dateFrom = this.form.dateFrom;
      const dateTo = this.form.dateTo;
      const dayAmount = this.form.dayAmount;
      const addedValue = this.form.addedValue;
      const advancePayment = this.form.advancePayment ? 1 : 0;
      const advancePaymentAmount = this.form.advancePaymentAmount;
      const reason = this.form.reason;
      const transport = this.transformTransportMaptoString(this.form.transport);

      return {
        travel_id: this.selectedTravel.id,
        destination: destination,
        address: address,
        date_from: dateFrom,
        date_to: dateTo,
        day_amount: dayAmount,
        cost_center: costCenter,
        added_value: addedValue,
        advance_payment: advancePayment,
        advance_payment_amount: advancePaymentAmount,
        reason: reason,
        transport: transport,
        extra_documentation: null
      };
    },
    transformTransportMaptoString(transportMap) {
      const transportArray = [
        transportMap['Plane'], transportMap['Train'],
        transportMap['RentCar'], transportMap['BusinessCar'],
        transportMap['PrivateCar'], transportMap['Taxi']
      ]

      let transportString = ""
      transportArray.forEach((isTransportOpChosen, index) => {
        if (isTransportOpChosen) {
          if (transportString.length == 0) {
            transportString += this.transportNamesOrder[index]
          } else {
            transportString += ";" + this.transportNamesOrder[index]
          }
        }
      });

      //if no transportOps are chosen, we insert it as null
      if (transportString == "") transportString = null
      return transportString;
    },
    transformTransportStringtoMap(transportString) {
      let transportMap = { 'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }

      //if string is null, all transportOps remain false
      if (transportString) {
        let transportOpsChosen = Array.from(transportString.split(";"))

        this.transportNamesOrder.forEach(transportOp => {
          if (transportOpsChosen.includes(transportOp)) transportMap[transportOp] = true;
        });
      }

      return transportMap;
    },
    async updateTravel() {
      const data = this.collectFormData();

      loadingMessage();
      try {
        const response = await fetch(`${BACKEND_HOST}travel/update-travel-details`, {
          method: "PUT",
          headers: {
            "Authorization": localStorage.getItem("Authorization"),
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Trip could not be edited: " + error.state || error.message);
        }
        stopLoadingMessage();

        notifySuccess("Trip edited successfully!");
        this.reload()
        this.openTravelDetails(this.selectedTravel, false); //go back to viewing that same travel (resets view/edit/create variables)
      } catch (error) {
        notifyError(error.message);
        console.error(error.message)
      }
    },
    async submitTravelRequest() {
      const data = this.collectFormData();

      loadingMessage();
      try {
        const response = await fetch(`${BACKEND_HOST}travel/request`, {
          method: "POST",
          headers: {
            "Authorization": localStorage.getItem("Authorization"),
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Trip request could not be submitted, try again later: " + (error.state || error.message));
        }
        stopLoadingMessage();

        notifySuccess("Trip requested successfully!");
        this.closeForm();
        this.resetForm();
        this.reload();
      } catch (error) {
        notifyError(error.message);
        console.error(error.message)
      }
    },
    async fecthUserCostCenter() {
      try {
        const response = await fetch(`${BACKEND_HOST}user/get-user-cost-center`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Could not load user Cost Center: " + (error.message || error.state));
        }

        const data = await response.json();
        this.userCostCenter = data[0];
      } catch (error) {
        notifyError(error.message);
        console.error(error.message)
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 100%;
  min-width: 600px;
}

.form-check-input:checked {
  background-color: #501eb6;
  border-color: #4c2a85;
  opacity: 100%;
}

.form-control:disabled {
  background-color: var(--bs-primary-bg);
}

.form-check-input:disabled~.form-check-label,
.form-check-input[disabled]~.form-check-label {
  opacity: 100%;
}

.form-control {
  border: solid #501eb6 0.15rem;
}

.hasError {
  border: solid #b61e1e 0.15rem;
  border-color: #b61e1e;
  background-color: #b61e1e28;
}

.purple {
  background-color: #4c2a85;
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

.lightPurple {
  background-color: #e9d5ff;
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

.borderPurple {
  border: 2px solid #4c2a85;
  background-color: transparent;
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

#travelListContainer {
  max-height: 760px;
  overflow-y: auto;
}

#topControlsContainer .d-flex {
  width: 100%;
}

#topControlsContainer h1 {
  margin: 0;
}

#btn_OpenReqForm {
  margin-left: 10px;
}

@media (max-width: 1570px) {
  .iconDissapear-md {
    display: none;
  }

  #btn_OpenReqForm {
    height: 40px;
  }

  #btn_filterTravels {
    height: 40px;
  }

  .lessWidth {
    width: 200px;
    margin-right: 10px;
  }
}

.vc-light.vc-attr,
.vc-light .vc-attr {
  --vc-content-color: white;
  --vc-highlight-light-content-color: white;
}
</style>