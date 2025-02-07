<template>
  <main class="d-flex flex-column px-2 flex-body">
    <h1 class="text-left mt-3 mb-4 fs-3 fw-bold col-6">City vacation days</h1>

    <div class="d-flex flex-wrap justify-between w-100 gap-4">
      <!-- Contenedor de Filtros y Tabla de días de vacaciones -->
      <div class="w-full lg:w-5/12">
        <div id="containerFilters" class="mb-4">
          <!-- Filtros de ciudades -->
          <h3 class="mb-2">Filters:</h3>
          <div class="btn-group flex flex-wrap justify-around" role="group">
            <!-- Botones de ciudades con distribución uniforme -->
            <button v-for="(city, index) in cities" :key="index" type="button"
              class="btn btn-outline-primary w-full md:w-auto mb-2 m-1" @click="toggleCity(city.value)" :id="city.name">
              {{ city.name }}
            </button>
          </div>
        </div>

        <!-- Tabla con los días filtrados -->
        <div class="overflow-auto">
          <div class="table-responsive" id="scrollableCityDays">
            <table class="table table-striped">
              <thead class="position-sticky bg-white" style="top: 0;">
                <tr>
                  <!-- Columna Year con evento click para alternar el orden -->
                  <th @click="toggleYearSort" class="cursor-pointer">
                    Year
                    <!-- Icono de la flecha -->
                    <i v-if="sortDirection === 'asc'" class="fa-solid fa-arrow-right fa-rotate-90"></i>
                    <i v-if="sortDirection === 'desc'" class="fa-solid fa-arrow-right fa-rotate-270"></i>
                  </th>
                  <th>City</th>
                  <th>Days</th>
                </tr>
              </thead>
              <tbody>
                <!-- Días filtrados y ordenados -->
                <tr v-for="cityDay in filterCityDays()" :key="cityDay.Year + cityDay.City">
                  <td>{{ cityDay.Year }}</td>
                  <td>{{ cityDay.City }}</td>
                  <td>{{ cityDay.Days }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Formulario para añadir días de ciudad -->
      <div class="w-full lg:w-5/12">
        <form @submit.prevent="collectDataAdding()">
          <div class="overflow-auto mt-3">
            <button type="submit" class="btn btn-primary btn-block bg-main mt-3">Add city days</button>

            <div class="table-responsive">
              <table class="table table-striped w-full">
                <thead class="position-sticky bg-white" style="top: 0;">
                  <tr>
                    <th>Year</th>
                    <th>City</th>
                    <th>Days</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="city in cities" :key="new Date().getFullYear() + city.value">
                    <td>{{ new Date().getFullYear() +1 }}</td>
                    <td>{{ city.value }}</td>
                    <td>
                      <input :id="'inputAddDays'+city.value" class="form-control" type="number" placeholder="Number..." step="any">
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </form>

        <div class="d-block border my-4 p-3">
          <div class="d-flex">
            <label class="mr-3">Remove all city days registries in:</label>
            <input id="removeDaysYear" class="form-control w-fit h-fit" type="number" placeholder="Year" step="1">
          </div>

          <button type="button" class="btn btn-primary btn-block bg-main mt-3" @click="removeCityDays()">Remove</button>
        </div>

      </div>
    </div>

  </main>
</template>


<script>
import { loadingMessage, notifyError, notifySuccess, stopLoadingMessage } from '@/assets/globalFunctions';
import { BACKEND_HOST } from '../config';

export default {
  data() {
    return {
      cityDays: [], // Datos de los días de vacaciones por ciudad y año.
      selectedCities: [], // Lista de ciudades seleccionadas por el usuario.
      cities: [
        { name: 'Pamplona', value: 'PAM', color: '#fbb1ad' },
        { name: 'Cuenca', value: 'CUE', color: '#b7f1ac' },
        { name: 'Martorell', value: 'MAR', color: '#b7b7ff' },
      ],
      sortDirection: null
    };
  },
  created() {
    this.fetchCityDays(); // Cargar los datos al iniciar el componente.
  },
  methods: {
    toggleCity(cityValue) {
      let object;
      const index = this.selectedCities.indexOf(cityValue);
      if (cityValue === "PAM") {
        object = document.getElementById("Pamplona");
      } else if (cityValue === "CUE") {
        object = document.getElementById("Cuenca");
      } else {
        object = document.getElementById("Martorell");
      }
      if (index === -1) {
        object.classList.add(cityValue);
        this.selectedCities.push(cityValue); // Añado la ciudad al array
      } else {
        object.classList.remove(cityValue);
        this.selectedCities.splice(index, 1);
      }
      this.filterCityDays();
    },
    isCitySelected(cityValue) {
      return this.selectedCities.includes(cityValue); // Verifica si la ciudad está seleccionada.
    },
    filterCityDays() {
      let filteredCityDays = [...this.cityDays];

      if (this.sortDirection === 'asc') {
        // Ordena de menor a mayor
        filteredCityDays.sort((a, b) => a.Year - b.Year);
      } else if (this.sortDirection === 'desc') {
        // Ordena de mayor a menor
        filteredCityDays.sort((a, b) => b.Year - a.Year);
      }
      // Filtra los datos según las ciudades seleccionadas.
      if (this.selectedCities.length !== 0) {
        return filteredCityDays.filter(day => this.selectedCities.includes(day.City));
      }
      return filteredCityDays;
    },
    // Método para alternar la ordenación del año
    toggleYearSort() {
      if (this.sortDirection === null) {
        this.sortDirection = 'asc';  // Primer clic: ordenar ascendentemente
      } else if (this.sortDirection === 'asc') {
        this.sortDirection = 'desc'; // Segundo clic: ordenar descendentemente
      } else {
        this.sortDirection = null;   // Tercer clic: desactivar la ordenación
      }
    },
    async fetchCityDays() {
      try {
        loadingMessage();
        const response = await fetch(`${BACKEND_HOST}/hr/get-city-days`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('City days could not be obtained');
        }

        const data = await response.json();
        this.cityDays = data;
        stopLoadingMessage();
      } catch (error) {
        stopLoadingMessage();
        notifyError(error.message);
      }
    },
    collectDataAdding(){      
      try {
        let newCityDays = new Map([])
        this.cities.forEach(city => {
          let id = 'inputAddDays' + city.value
          let days = document.getElementById(id).value

          //validate each field
          if (!days || days == '') throw new Error("All fields are required")

          newCityDays.set(city.value, days)
        })
        
        this.addCityDays(newCityDays)
      } catch (error) {
        notifyError(error.message);
      }
    },
    async addCityDays(newCityDays) {      
      let data = { cityDays: Object.fromEntries(newCityDays)}

      loadingMessage();
      try {
        const response = await fetch(`${BACKEND_HOST}hr/add-city-days`, {
          method: 'PUT',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Failed to add city days: " + (error.message || error.state));
        }

        notifySuccess("City vacation days added succesfully!")
        this.fetchCityDays()

        //reset the fields
        this.cities.forEach(city => {
          let id = 'inputAddDays' + city.value
          document.getElementById(id).value = null
        })
        stopLoadingMessage();
      } catch (error) {
        notifyError(error.message);
        console.error(error.message);
        stopLoadingMessage();
      }
    },
    async removeCityDays(){
      let yearDelete = document.getElementById('removeDaysYear').value
      if (yearDelete && yearDelete != '' && yearDelete != 0){
        let data = {year: yearDelete}

        loadingMessage()
        try {
          const response = await fetch(`${BACKEND_HOST}hr/remove-city-days`, {
            method: 'DELETE',
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error("Failed to remove city days: " + (error.message || error.state));
          }

          notifySuccess("City vacation days removed succesfully!")
          this.fetchCityDays()
          document.getElementById('removeDaysYear').value = null
          stopLoadingMessage();
        } catch (error) {
          notifyError(error.message);
          console.error(error.message);
          stopLoadingMessage();
        }
      } else {
        notifyError("Year field is required");
      }
    },
  },
};
</script>

<style scoped>
#scrollableCityDays {
  max-height: 800px;
  overflow-y: auto;
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
</style>