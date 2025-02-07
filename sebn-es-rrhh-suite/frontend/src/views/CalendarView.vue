<template>
  <main class="d-flex flex-column-reverse flex-xl-row flex-body">
    <div class="col-lg-8">
      <h1 class="text-left mt-3 mb-2 mx-2 fs-3 fw-bold col-6">My holidays</h1>

      <!-- Calendar -->
      <div class="mt-4 mb-2 mx-2 px-0">
        <div class="info-container">
          <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
          <div class="legend-container">
            
            <div class="d-flex flex-row justify-content-center gap-3 font-small">
              <div class="d-flex align-items-center font-small">
                <span class="legend-color mr-1 approved-highlight"></span> Approved
              </div>
              <div class="d-flex align-items-center font-small">
                <span class="legend-color mr-1 requested-highlight"></span> Requested
              </div>
              <div class="d-flex align-items-center font-small">
                <span class="legend-color mr-1 rejected-highlight"></span> Rejected
              </div>
            </div>

            <div class="d-flex flex-row justify-content-center gap-3 font-small">
              <div class="d-flex align-items-center font-small">
                <span class="legend-color mr-1 homeAux"></span> Home Office
              </div>
              <div class="d-flex align-items-center font-small">
                <span class="legend-color mr-1 tripAux"></span> Travels
              </div>
            </div>
          </div>
        </div>
        <VDatePicker ref="datePicker" class="w-100 my-calendar" v-model.range.number="range" :attributes="attrs"
          :select-attribute="selectAttribute" :columns="cols" :rows="rows" id="calendar" :max-date="maxDate"
          :min-date="minDate">
          <template #day-popover="{ attributes }">
            <div v-for="{ key, popover } in attributes" :key="key">
              <div>
                <!-- Aquí lo que se hace lo primero es comprobar que tenga la variable .class si no la tiene comprueba que empiece por H para poner la clase homeAux, definida abajo y así con los demás. -->
                <span :class="[
                  popover.color && popover.color.class ? popover.color.class :
                    (popover.label && (popover.label.startsWith('Fu') || popover.label.startsWith('O') || popover.label.startsWith('P')) ? 'homeAux' :
                      (popover.label && popover.label.startsWith('(') ? 'tripAux' :
                        (popover.label && popover.label.startsWith('Fe') ? 'festivityAux' : 'blue'))),
                  popover.color && popover.color.class ? popover.color.class.replace('-highlight', '') : ''
                ]"></span>
                <span class="small">
                  {{ popover.label === 'Holiday created' ? 'Holiday requested' : popover.label === 'Holiday signed' ?
                    'Holiday approved' : popover.label }}
                </span>
              </div>
            </div>
          </template>
        </VDatePicker>
      </div>

      <!-- Vacation request form -->
      <div class="border px-4 py-3 rounded-3 mx-2">
        <div class="card-body">
          <form @submit.prevent="submitForm" id="form">
            <div class="row mb-4">
              <div class="col-md-3">
                <label for="start" class="form-label ">Start Date</label>
                <input type="text" class="form-control" id="start" :value="startDate" placeholder="Start date"
                  readonly />
              </div>
              <div class="col-md-4">
                <label for="finish" class="form-label">Finish Date</label>
                <input type="text" class="form-control" id="finish" :value="endDate" placeholder="End date" readonly />
              </div>

              <div class="col-md-4">
                <label for="finish" class="form-label">Bucket</label>
                <select class="form-control" id="bucketStart" v-model="bucketStart">
                  <option value="" disabled hidden selected>Select...</option>
                  <option v-for="bucket in buckets" :value="bucket.bucket">
                    {{ bucket.bucket }}
                  </option>
                </select>
              </div>

              <div class="col-md-2 d-flex align-items-center mt-2">
                <div class="form-check w-100 d-flex align-items-center">
                  <input type="checkbox" class="form-check-input mt-4" id="partialDay" value="partialDay"
                    @change="disableHours" />
                  <label for="partialDay" class="form-check-label ms-2 mt-4">Partial day</label>
                </div>
              </div>

              <div class="col-md-3 mt-2">
                <label for="hourCount" class="form-label">Hours</label>
                <select name="hourCount" class="form-control" id="hourCount" disabled>
                  <option v-if="userWorkingHours > 1" v-for="hour in (userWorkingHours - 1)" :key="hour"
                    :value="userWorkingHours - hour">
                    {{ userWorkingHours - hour }}
                  </option>
                  <option v-if="userWorkingHours <= 1" disabled>No options available</option>
                </select>
              </div>
            </div>
            <button type="submit" class="btn btn-primary mx-auto">
              Submit
            </button>
          </form>
        </div>
      </div>
    </div>

    <div class="col col-xl-4 mt-1">
      <div class="card me-4 border-0">
        <div class="card-body">

          <!-- Download vacations excel -->
          <div class="mb-2 d-flex">
            <button type="button" class="btn btn-primary mr-4" @click="createExcel">
              Download in Excel <i class="fa-solid fa-file-excel ms-2"></i>
            </button>
            <button class="btn btn-secondary bg-main dropdown-toggle" type="button" id="btn_filterTravels"
              data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fa-solid fa-filter mr-2"></i> Filter
            </button>
            <div class="dropdown-menu dropdown-menu-end p-4 shadow" aria-labelledby="btn_filterVacations"
              style="min-width: 300px; position: absolute; top: 100%; right: 0; z-index: 1000;">
              <form>
                <!-- Filtro por Mes -->
                <div class="mb-3">
                  <label for="monthFilter" class="form-label">Month</label>
                  <select class="form-select" id="monthFilter" v-model="selectedMonthFilter"
                    @change="updateFilteredVacations">
                    <option value="" selected>All</option>
                    <option value="January">January</option>
                    <option value="February">February</option>
                    <option value="March">March</option>
                    <option value="April">April</option>
                    <option value="May">May</option>
                    <option value="June">June</option>
                    <option value="July">July</option>
                    <option value="August">August</option>
                    <option value="September">September</option>
                    <option value="October">October</option>
                    <option value="November">November</option>
                    <option value="December">December</option>
                  </select>
                </div>

                <!-- Filtro por Estado -->
                <div class="mb-3">
                  <label for="statusFilter" class="form-label">Status</label>
                  <select class="form-select" id="statusFilter" v-model="selectedStatusFilter"
                    @change="updateFilteredVacations">
                    <option value="All" selected>All</option>
                    <option value="CREATED">Requested</option>
                    <option value="SIGNED">Signed</option>
                    <option value="REJECTED">Rejected</option>
                  </select>
                </div>

                <!-- Botón de limpiar filtros -->
                <div class="d-grid">
                  <button type="button" class="btn btn-secondary mt-3" @click="resetFilters()">Clean all
                    filters</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Vacations list (cards) -->
          <div id="holidaysContainer">
            <div v-if="filteredVacations.length" class="mt-2">
              <div
                v-for="vacation in filteredVacations.sort((a, b) => new Date(b.startingDay) - new Date(a.startingDay))"
                :key="vacation.id" class="card mb-3">
                <div class="card-body">
                  <h6 class="card-subtitle mb-1 fs-5 titleVacation fw-bold"
                    :style="{ color: color[vacation.status.toLowerCase()] }">
                    {{ vacation.status === 'CREATED' ? 'REQUESTED' : vacation.status === 'SIGNED' ? 'APPROVED' :
                      vacation.status }}
                  </h6>
                  <p class="card-text fs-6 fw-medium" v-if="!vacation.partialDay">
                    {{ formatDate(vacation.startingDay) }} - {{ formatDate(vacation.finishingDay) }}
                  </p>
                  <p class="card-text fs-6 fw-medium" v-if="vacation.partialDay">
                    {{ formatDate(vacation.startingDay) }}
                    ({{ Math.floor((vacation.totalQuantity / (hourConversionValue / 60)) / 60) }} h)
                  </p>
                </div>
                <div class="flex-body position-absolute top-0 end-0 translate-middle p-2 border rounded-circle"
                  :class="color[vacation.status.toLowerCase()]"
                  :style="{ backgroundColor: color[vacation.status.toLowerCase()] }"
                  :title="vacation.status === 'CREATED' ? 'REQUESTED' : vacation.status === 'SIGNED' ? 'APPROVED' : vacation.status">
                </div>

                <!-- Delete vacation -->
                <button :id="vacation.id" type="button" title="Delete" data-bs-target="#modalConfirm"
                  data-bs-toggle="modal" alt="Delete icon"
                  class="position-absolute top-50 end-0 translate-middle-y p-2 btn-unstyled"
                  @click="selectedID = vacation.id">
                  <svg class="trashIcon" width="40" height="40" fill="none" viewBox="0 0 149 139"
                    xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="m40.548 35h22.172m46.281 0h-22.281m-24 0v-6.5c0-1.933 1.567-3.5 3.5-3.5h17v0c1.933 0 3.5 1.567 3.5 3.5v6.5m-24 0h24"
                      stroke="#535353" stroke-linecap="round" stroke-width="6" />
                    <path
                      d="m47.511 38v-3h-6v3h6zm-3 70.5h-3v0.05l0.0017 0.051 2.9983-0.101zm4.5 5-0.2431 2.99 0.1214 0.01h0.1217v-3zm52 0v3h0.05l0.05-2e-3 -0.1-2.998zm4-5h-3v0.078l4e-3 0.078 2.996-0.156zm3-70.5v-3h-6v3h6zm-42.5 11c0-1.6569-1.3431-3-3-3-1.6568 0-3 1.3431-3 3h6zm-6 51c0 1.657 1.3432 3 3 3 1.6569 0 3-1.343 3-3h-6zm18-51c0-1.6569-1.3431-3-3-3-1.6568 0-3 1.3431-3 3h6zm-6 51c0 1.657 1.3432 3 3 3 1.6569 0 3-1.343 3-3h-6zm18-51c0-1.6569-1.3431-3-3-3-1.6568 0-3 1.3431-3 3h6zm-6 51c0 1.657 1.3432 3 3 3 1.6569 0 3-1.343 3-3h-6zm-42-62v70.5h6v-70.5h-6zm0.0017 70.601c0.0627 1.865 0.3251 4.014 1.7651 5.634 1.4954 1.682 3.6238 2.103 5.4901 2.255l0.4863-5.98c-1.5638-0.127-1.6251-0.411-1.492-0.261 0.0548 0.061-1e-3 0.042-0.0756-0.245-0.0808-0.312-0.1505-0.809-0.1772-1.605l-5.9967 0.202zm7.4983 7.899h52v-6h-52v6zm52.1-2e-3c1.759-0.059 4.05-0.361 5.554-2.233 1.389-1.728 1.441-4.025 1.342-5.921l-5.992 0.312c0.045 0.857 0.016 1.391-0.039 1.72-0.052 0.312-0.102 0.272 0.012 0.131 0.136-0.169 0.263-0.191 0.149-0.154-0.164 0.053-0.524 0.125-1.227 0.149l0.201 5.996zm3.9-7.998h3v-70.5h-6v70.5h3zm-45.5-59.5v51h6v-51h-6zm12 0v51h6v-51h-6zm12 0v51h6v-51h-6z"
                      fill="#535353" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Modal delete holiday-->
          <div class="modal fade" id="modalConfirm" tabindex="-1" role="dialog"
            aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLongTitle">
                    Delete holiday
                  </h5>
                </div>
                <div class="modal-body">
                  Are you sure you want to delete the holiday?
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">
                    Cancel
                  </button>
                  <button type="button" class="btn btn-primary" @click="deleteVacation(selectedID)"
                    data-bs-dismiss="modal">
                    Accept
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from "vue";
import { notifyError, notifySuccess, capitalizeWords, loadingMessage, stopLoadingMessage, getUsername } from "@/assets/globalFunctions";
import { BACKEND_HOST } from "../config";

let range = ref({
  start: new Date(),
  end: new Date()
});
let startDate = formatDate(range.value.start);
let endDate = formatDate(range.value.end);
let date = ref(new Date());
let checkboxFlag = false; //Si está o no checkeado el checkbox de Partial day
let userWorkingHours = ref(0)
let hourConversionValue = ref(0)
let bucketStart = ref("").value;
let buckets = ref([]);

const festivities = ref([]);
const vacations = ref([]);
const homeOfficeDays = ref([]);
const travelDays = ref([])
const attrs = ref([]);
const reason = ref("");
const color = reactive({ created: "#e7ad41", signed: "#7ab870", rejected: "#c75353" });
const year = new Date().getFullYear();
const minDate = new Date(new Date().getFullYear(), 0, 1);
const rows = ref(window.innerWidth > 1470 ? 2 : 3);
const cols = ref(window.innerWidth > 1470 ? 3 : 2);
const selectedID = ref(0);
const selectAttribute = ref({
  highlight: {
    start: { fillMode: 'outline', color: "blue" },
    base: { fillMode: 'light', color: "blue" },
    end: { fillMode: 'outline', color: "blue" },
  }
});
const selectedMonthFilter = ref('');
const selectedStatusFilter = ref('All');

// Computed property para las vacaciones filtradas
const filteredVacations = computed(() => {
  return vacations.value.filter(vacation => {
    const vacationMonth = new Date(vacation.startingDay).toLocaleString('eng-us', { month: 'long' });
    const matchesMonth = selectedMonthFilter.value === '' || vacationMonth === selectedMonthFilter.value;
    const matchesStatus = selectedStatusFilter.value === 'All' || vacation.status === selectedStatusFilter.value;
    return matchesMonth && matchesStatus;
  });
});

// Función para restablecer filtros
const resetFilters = () => {
  selectedMonthFilter.value = '';
  selectedStatusFilter.value = 'All';
};
let maxDate = new Date(year, 11, 31);

// we wait to fetch everything, then print calendar
onMounted(async () => {
  await Promise.all([fetchFestivities(), fetchTravelDays(), fetchHomeOfficeDays(), fetchVacations(), fetchUserWorkingHours(), fetchBuckets()]);
  printCalendar();
  hourConversionValue = (1 / userWorkingHours).toFixed(3)
});

async function fetchFestivities() {
  loadingMessage();
  try {
    const bodyData = {Email: null};

    const response = await fetch(`${BACKEND_HOST}festivity/get-user-festivities`, {
      method: "POST",
      headers: {
        "Authorization": localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bodyData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error("Failed to load festivities: " + (errorData.message || error.state));
    }

    const data = await response.json();

    festivities.value = [];
    for (const festivity of data) {
      try {
        festivities.value.push(festivity['Date'])
      } catch (error) {
        console.error("Failed to load festivities: " + (error.message || error.state));
      }
    }

    stopLoadingMessage();
  } catch (error) {
    stopLoadingMessage();
    notifyError("The festivities could not be obtained");
  }
};

/**
 * Esto es para observar la variable y cambiarla cada vez que se cambia, porque no se cambia sola en los valores del html
 */
watch(range, function () {
  if (checkboxFlag) { //Si es true se ponen los dos a start porque solo puede elegir horas para un día
    startDate = formatDate(range.value.start);
    endDate = formatDate(range.value.start);
  } else {
    startDate = formatDate(range.value.start);
    endDate = formatDate(range.value.end);
  }
})

async function fetchHomeOfficeDays() {
  try {
    const response = await fetch(`${BACKEND_HOST}home-office/get-home-office`, {
      headers: {
        "Authorization": localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("The home office days could not be obtained");
    }

    const data = await response.json();
    homeOfficeDays.value = data;
  } catch (error) {
    notifyError("The home office days could not be obtained");
  }
};

async function fetchTravelDays() {
  try {
    const response = await fetch(`${BACKEND_HOST}travel/get-travels`, {
      headers: {
        "Authorization": localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("The travel days could not be obtained");
    }

    const data = await response.json();
    travelDays.value = data;
  } catch (error) {
    notifyError(error.message);
  }
};

async function fetchVacations() {
  try {
    const response = await fetch(`${BACKEND_HOST}holiday/get-user-holidays`, {
      headers: {
        "Authorization": localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Holidays could not be obtained");
    }

    const data = await response.json();
    vacations.value = data;
  } catch (error) {
    notifyError("Holidays could not be obtained");
  }
};

async function printCalendar() {
  await Promise.all([fetchFestivities(), fetchTravelDays(), fetchHomeOfficeDays(), fetchVacations()]);

  //allow to request next year if festivities are already set
  canRequestNextYear();

  attrs.value.splice(0);
  const weekends = ref([
    {
      description: 'weekend',
      isComplete: false,
      dates: { repeat: { weekdays: [1, 7] } }, // Every Saturday and Sunday
    },
  ]);

  const computedAttrs = computed(() => [
    ...weekends.value.map(day => ({
      dates: day.dates,
      content: {
        color: 'weekend',
        class: 'weekend',
      },
    })),
  ]);

  attrs.value = computedAttrs.value;

  festivities.value.forEach((festivity) => {
    attrs.value.push({
      key: festivity,
      dates: festivity,
      content: {
        class: 'festivity-highlight'
      },
      popover: {
        label: "Festivity",
      },
    });
  });

  travelDays.value.forEach((travel) => {
    const startDate = new Date(travel.dateFrom);
    const endDate = new Date(travel.dateTo);

    let reason = travel.reason
    if (reason.length > 25) reason = reason.substring(0,20) + "...";

    attrs.value.push({
      dates: [[startDate, endDate]],
      dot: "purple",
      popover: {
        label: `(${travel.id}) ${capitalizeWords(reason)}`
      },
    });
  });

  homeOfficeDays.value.forEach((day) => {
    let value = day.Type 
    if(day.Type != "OFFICE") value = value + " remote";

    attrs.value.push({
      dates: new Date(day.Date),
      dot: "blue",
      popover: {
        label: `${capitalizeWords(value)}`,
      },
    });
  });

  printVacations();
};

async function printVacations() {
  vacations.value.forEach((vacation) => {
    const startDate = new Date(vacation.startingDay);
    const endDate = new Date(vacation.finishingDay);
    const status = vacation.status === 'CREATED' ? 'requested' : vacation.status === 'SIGNED' ? 'approved' : vacation.status.toString().toLowerCase();
    const highlightClass = status + "-highlight";

    attrs.value.push({
      highlight: { class: highlightClass },
      contentStyle: {
        color: 'white'
      },
      popover: {
        label: "Holiday " + vacation.status.toLowerCase(),
        color: { class: highlightClass },
      },
      dates: [[startDate, endDate]],
    });
  });
};

function toggleLegend() {
  const legend = document.querySelector('.legend-container');
  legend.classList.toggle('show');
};

function isWeekend(date) {
  const dayOfWeek = new Date(date).getDay();
  return dayOfWeek === 0 || dayOfWeek === 6;
};

async function submitForm() {
  //First we do validations
  if (isWeekend(range.value.start) || isWeekend(range.value.end)) {
    notifyError("The start and the end of the range can not be Saturday or Sunday");
    return;
  }

  if (bucketStart == "") {
    notifyError("The bucket field is required");
    return;
  }

  //If everything alright, we start collecting data
  const startingDayFormatted = formatDate(range.value.start);
  const finishingDayFormatted = formatDate(range.value.end);
  const partialDay = document.getElementById('partialDay').checked
  const hours = document.getElementById('hourCount').value
  const bucketStartSelect = document.getElementById('bucketStart').value

  //if partial day, we ignore finish day IN BACK
  const data = {
    startingDay: startingDayFormatted,
    finishingDay: finishingDayFormatted,
    partialDay: partialDay,
    hours: ((hours) * hourConversionValue).toFixed(3),
    bucketStart: bucketStartSelect
  };

  loadingMessage();
  try {
    const response = await fetch(`${BACKEND_HOST}holiday/request`, {
      method: "POST",
      headers: {
        Authorization: localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.state);
    }
    notifySuccess("Holidays requested successfully!");

    //reset form  & reload
    range.value = { start: new Date(), end: new Date() };
    reloadVacations();
  } catch (error) {
    notifyError(error.message);
  } finally {
    stopLoadingMessage();
  }
};

async function reloadVacations() {
  await fetchVacations();
  printCalendar();
};

async function deleteVacation(id) {
  try {
    const response = await fetch(`${BACKEND_HOST}holiday/delete-user-holidays`, {
      method: "DELETE",
      headers: {
        Authorization: localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    });

    if (!response.ok) {
      throw new Error("Holiday could not be deleted");
    }

    notifySuccess("Holiday has been deleted successfully!");
    reloadVacations();
  } catch (error) {
    console.error(error);
    notifyError(error.message);
  }
}

async function createExcel() {
  try {
    const response = await fetch(`${BACKEND_HOST}user/create-user-holidays-excel`, {
      method: "GET",
      headers: {
        Authorization: localStorage.getItem("Authorization"),
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Vacations_${getUsername()}_${new Date().toISOString().slice(0, 10)}.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading the file", error);
    notifyError("An error occurred while downloading the file.");
  }
};

function formatDate(date) {
  if (!date) return "";
  const d = new Date(date);
  const day = d.getDate().toString().padStart(2, "0");
  const month = (d.getMonth() + 1).toString().padStart(2, "0");
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
};

function disableHours() {
  checkboxFlag = !checkboxFlag; // Cambio la flag :D
  const date = ref(new Date());
  date.value = document.getElementById("start").value;

  // Habilito el campo y lo desabilito en cuestión de el check (Lo hago al revés porque empieza en false)
  document.getElementById("hourCount").disabled = !document.getElementById("partialDay").checked;

  const finishInput = document.getElementById("finish"); // El input de la fecha final, para que a la base de datos se le pase bien

  // En el caso de que esté checked le cambio el valor
  if (document.getElementById("partialDay").checked) {
    finishInput.value = document.getElementById("start").value;
  } else {
    finishInput.value = formatDate(range.value.end);
  }
  finishInput.disabled = document.getElementById("partialDay").checked;
};

async function fetchUserWorkingHours() {
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
    userWorkingHours = data[0];
    stopLoadingMessage();
  } catch (error) {
    console.error(error);
  }
};

async function fetchBuckets() {
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
    buckets = data;
    stopLoadingMessage();
  } catch (error) {
    notifyError(error.message);
    stopLoadingMessage();
  }
};

/**
 * By default, the holiday calendar is limited to the current year only, 
 * but if there are any festivities for next year created, 
 * user can already request holidays in it too 
 * (aka, must also enable following year calendar)
 */
function canRequestNextYear() {
  let areFestivitiesNextYear = festivities.value.some(item => new Date(item).getFullYear() === (new Date().getFullYear()) + 1);

  if (areFestivitiesNextYear) {
    maxDate = new Date(new Date().getFullYear() + 1, 11, 31);
  }
};


window.addEventListener("resize", () => {
  rows.value = window.innerWidth > 1470 ? 2 : 3;
  cols.value = window.innerWidth > 1470 ? 3 : 2;
});
</script>

<style>
.vc-weekday-7,
.vc-weekday-1 {
  color: #6366f1;
}

.trashIcon:hover> :first-child {
  transform: rotate(11deg) translate(-3px, 10px);
}

.trashIcon:active> :first-child {
  stroke: #bc0000;
}

.trashIcon:active> :last-child {
  fill: #bc0000;
}

.trashIcon> :first-child {
  transform-origin: right;
  transition: transform 300ms ease-in-out;
}

.full {
  background-color: #0075C2;
}

.partial {
  background-color: #06B4E9;
}

.office {
  background-color: #7B639F;
}

#holidaysContainer {
  max-height: 780px;
  overflow-y: auto;
  margin-top: 10px;
}

/* La clase .blue será para todo lo que no sea una vacation */
.approved,
.rejected,
.requested,
.homeAux,
.tripAux,
.festivityAux {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

.approved-highlight {
  background-color: #7ab870 !important;
}

.rejected-highlight {
  background-color: #c75353 !important;
}

.requested-highlight {
  background-color: #e7ad41 !important;
}

.approved-highlight:hover,
.rejected-highlight:hover,
.requested-highlight:hover {
  opacity: 0.8;
}

/* Clases para el texto de la derecha !IMPORTANTE DEJAR orange en los colores, o el color que sea */
.orangeText {
  color: #ffa500;
}

.greenText {
  color: #45b035;
}

.redText {
  color: #ff0000;
}

.homeAux {
  background-color: #0075c2;
}

.tripAux {
  background-color: #9333ea;
}

.festivityAux {
  background-color: #45b035;
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
}

.festivity-highlight {
  color: green;
  font-weight: bold;
}

.vc-light.vc-attr,
.vc-light .vc-attr {
  --vc-content-color: white;
  --vc-highlight-light-content-color: white;
}
</style>
