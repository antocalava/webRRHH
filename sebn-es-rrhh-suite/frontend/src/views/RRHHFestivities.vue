<template>
  <main class="d-flex flex-column mt-3 mx-2 overflow-x-hidden festivities flex-body">
    <h1 class="text-left mt-3 mb-2 fs-3 fw-bold col-6">Festivities</h1>
    <form @submit.prevent="submitForm">
      <label class="w-50">
        <span class="sr-only">Date</span>
        <input type="date" class="form-control" v-model="date" required>
      </label>
      <div class="d-flex align-items-center gap-3 mt-2 ms-1">
        <label class="form-check form-check-inline py-1" v-for="(city, index) in cities" :key="index">
          <input class="form-check-input" type="checkbox" :value="city.value" v-model="selectedCitiesToAdd">
          <span class="form-check-label">{{ city.name }}</span>
        </label>
        <button type="submit" class="btn btn-primary btn-block bg-main ms-3">Add festivity</button>
      </div>
    </form>

    <div class="d-flex flex-grow-1 mt-3 overflow-hidden">
      <div class="col-lg-6 d-flex flex-column overflow-auto">
        <h3>Filter Cities</h3>
        <div class="btn-group" role="group">
          <button v-for="(city, index) in cities" :key="index" type="button" class="btn btn-secondary" :id="city.name"
            @click="toggleCity(city.value)">
            {{ city.name }}
          </button>
        </div>
        
        <div class="d-flex flex-column flex-grow-1 mt-3 overflow-auto" id="scrollableSites">
          <div class="d-flex flex-column flex-wrap">
            <div v-for="festivity in filteredFestivities" :key="festivity.ID" class="card mb-3">
              <div class="card-body d-flex justify-content-between">
                <div>
                  <h5 class="card-title"><time :datetime="festivity.Date">{{ formatDate(festivity.Date) }}</time> | {{
                    cityCodes[festivity.City] }}</h5>
                </div>
                <button type="button" class="btn btn-primary bg-main"
                  @click="deleteFestivity(festivity.ID)">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-6 d-flex justify-content-center">
        <div class="d-flex flex-column calendar-container">
          <!-- Legend -->
          <div class="info-container">
                <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
                <div class="legend-container">
                  <div class="d-flex flex-row justify-content-center gap-3 font-small ml-3">
                    <div class="d-flex align-items-center font-small">
                      <span class="legend-color mr-1 PAM"></span> Pamplona
                    </div>
                    <div class="d-flex align-items-center font-small">
                      <span class="legend-color mr-1 CUE"></span> Cuenca 
                    </div>
                    <div class="d-flex align-items-center font-small">
                      <span class="legend-color mr-1 MAR"></span> Martorell
                    </div>
                  </div>
                </div>
              </div>
          <v-calendar v-model="selectedDate" :attributes="attrs" :rows="rows" :columns="cols"></v-calendar>
        </div>
      </div>

    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { notifySuccess, notifyError, loadingMessage, stopLoadingMessage } from '../assets/globalFunctions';
import { BACKEND_HOST } from '../config';

const date = ref('');
const cities = ref([
  { name: 'Pamplona', value: 'PAM', color: '#fbb1ad' },
  { name: 'Cuenca', value: 'CUE', color: '#b7f1ac' },
  { name: 'Martorell', value: 'MAR', color: '#b7b7ff' },
]);
const cityCodes = { PAM: "Pamplona", CUE: "Cuenca", MAR: "Martorell" };
const selectedCities = ref([]);
const selectedCitiesToAdd = ref([]);
const festividades = ref([]);
const selectedDate = ref(null);
const attrs = ref([]);
const rows = ref(window.innerWidth > 1800 ? 2 : 3);
const cols = ref(window.innerWidth > 1800 ? 3 : 2);

function formatDate(date) {
  const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
  return new Date(date).toLocaleDateString('es-ES', options);
};

function resizeCalendar() {
  rows.value = window.innerWidth > 1800 ? 2 : 3;
  cols.value = window.innerWidth > 1800 ? 3 : 2;
};

async function fetchFestivities() {
  loadingMessage();
  try {
    const response = await fetch(`${BACKEND_HOST}festivity/get-all-festivities`, {
      headers: {
        'Authorization': localStorage.getItem('Authorization'),
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      stopLoadingMessage();
      throw new Error('The festivities could not be obtained.');
    }

    const data = await response.json();
    festividades.value = data;
    printCalendar();
  } catch (error) {
    console.error(error);
    stopLoadingMessage();
    notifyError('The festivities could not be obtained.');
  }
};

function printCalendar() {
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

  attrs.value = computedAttrs.value; // Se añaden los fines de semana

  festividades.value.forEach(festivity => {
    const cityColor = cities.value.find(city => city.value === festivity.City)?.color || 'red';
    attrs.value.push({
      key: festivity.ID,
      dot: cityColor,
      popover: {
        label: festivity.City,
      },
      dates: festivity.Date,
    });
  });
  stopLoadingMessage();
};

async function submitForm() {
  if (selectedCitiesToAdd.value.length === 0) {
    notifyError('Please select at least one city.');
    return;
  }

  const data = {
    date: date.value,
    cities: selectedCitiesToAdd.value,
  };

  try {
    const response = await fetch(`${BACKEND_HOST}festivity/create-festivity`, {
      method: 'POST',
      headers: {
        'Authorization': localStorage.getItem('Authorization'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.state);
    }

    notifySuccess('Festivity added correctly!');
    fetchFestivities();
  } catch (error) {
    notifyError(error.message);
  }
};

function toggleCity(cityValue) {
  let object;
  if (cityValue === "PAM") {
    object = document.getElementById("Pamplona");
  } else if (cityValue === "CUE") {
    object = document.getElementById("Cuenca");
  } else {
    object = document.getElementById("Martorell");
  }
  if (selectedCities.value.includes(cityValue)) {
    object.classList.remove(cityValue);
    selectedCities.value = selectedCities.value.filter(selectedCity => selectedCity !== cityValue);
  } else {
    object.classList.add(cityValue);
    selectedCities.value.push(cityValue);
  }
};

async function deleteFestivity(id) {
  try {
    const response = await fetch(`${BACKEND_HOST}festivity/delete-festivity`, {
      method: 'DELETE',
      headers: {
        'Authorization': localStorage.getItem('Authorization'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: id }),
    });

    if (!response.ok) {
      throw new Error('Error when deleting the holiday');
    }

    await response.json();
    fetchFestivities();
    notifySuccess('Festivity successfully eliminated!');
  } catch (error) {
    notifyError('Error deleting the holiday. Please try again.');
  }
};

const filteredFestivities = computed(() => {
  return selectedCities.value.length === 0 ? festividades.value :
    festividades.value.filter(festivity => selectedCities.value.includes(festivity.City));
});

function toggleLegend() {
  const legend = document.querySelector('.legend-container');
  legend.classList.toggle('show');
};

onMounted(() => {
  fetchFestivities();
  window.addEventListener('resize', resizeCalendar);
});
</script>

<style>
main.festivities .btn-group .btn {
  margin-right: 5px;
}

main.festivities .btn-group {
  margin-bottom: 10px;
}

main.festivities .card {
  flex: 1 1 0;
  max-width: initial;
}

.vc-\#b7f1ac {
  background-color: #5bc448 !important;
}

.vc-\#fbb1ad {
  background-color: #e54b43 !important;
}

.vc-\#b7b7ff {
  background-color: #6b6be9 !important;
}

.PAM {
  background: #e54b43 !important;
}

.MAR {
  background: #6b6be9 !important;
}

.CUE {
  background: #5bc448 !important;
}

#scrollableSites {
  max-height: 600px;
  overflow-y: auto;
}
</style>