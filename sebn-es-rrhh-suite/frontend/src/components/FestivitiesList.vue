<!-- <template>
  <div>
    <h2>Add festivity day</h2>
    <form @submit.prevent="submitForm">
      <input type="date" class="form-control" v-model="date" required>
      <div class="form-check form-check-inline" v-for="(city, index) in cities" :key="index">
        <input class="form-check-input" type="checkbox" :value="city.value" v-model="selectedCitiesToAdd">
        <label class="form-check-label">{{ city.name }}</label>
      </div>
      <button type="submit" class="btn btn-primary btn-block mt-3">Submit</button>
    </form>

    <div class="container mt-3">


      <div class="row mt-3">

        <div class="col-lg-6">
          <h3>Filter Cities</h3>
          <div class="btn-group" role="group">
            <button v-for="(city, index) in cities" :key="index" type="button" class="btn"
                    :style="{ 'background-color': selectedCities.includes(city.value) ? city.color : 'gray' }"
                    @click="toggleCity(city.value)">
              {{ city.name }}
            </button>
          </div>
          <div class="mt-3" style="max-height: 400px; overflow-y: auto;">
            <div class="d-flex flex-column flex-wrap">
              <div v-for="festivity in filteredFestivities" :key="festivity.ID" class="card mb-3">
                <div class="card-body d-flex justify-content-between">
                  <div>
                    <h5 class="card-title">{{ formatDate(festivity.Date) }} | {{ festivity.City }}</h5>
                  </div>
                  <button type="button" class="btn btn-danger" @click="deleteFestivity(festivity.ID)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <v-calendar v-model="selectedDate" :attributes="attrs" :rows="2" :columns="2"></v-calendar>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Calendar, DatePicker} from 'v-calendar';
import 'v-calendar/style.css';
import {notifySuccess, notifyError} from '../assets/globalFunctions';
import {BACKEND_HOST} from '../config';


export default {
  components: {
    Calendar,
    DatePicker,
  },
  data() {
    return {
      date: '',
      cities: [
        {name: 'Pamplona', value: 'PAM', color: '#fbb1ad'},
        {name: 'Cuenca', value: 'CUE', color: '#b7f1ac'},
        {name: 'Martorell', value: 'MAR', color: '#b7b7ff'}
      ],
      selectedCities: [],
      selectedCitiesToAdd: [],
      festividades: [],
      selectedDate: null,
      attrs: [],
    };
  },
  methods: {
    async submitForm() {
      if (this.selectedCitiesToAdd.length === 0) {
        notifyError('Please select at least one city.');
        return;
      }

      const data = {
        date: this.date,
        cities: this.selectedCitiesToAdd
      };

      try {
        const response = await fetch(`${BACKEND_HOST}festivity/create-festivity`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const errorResponse = await response.json();
          throw new Error(errorResponse.state);
        }

        notifySuccess('Festivity added correctly!');
        this.fetchFestivities();
      } catch (error) {
        notifyError(error.message);
      }
    },

    toggleCity(cityValue) {
      if (this.selectedCities.includes(cityValue)) {
        this.selectedCities = this.selectedCities.filter(selectedCity => selectedCity !== cityValue);
      } else {
        this.selectedCities.push(cityValue);
      }
    },
    deleteFestivity(id) {
      fetch(`${BACKEND_HOST}festivity/delete-festivity`, {
        method: 'DELETE',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({id: id})
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Error when deleting the holiday');
            }
            return response.json();
          })
          .then(data => {
            this.fetchFestivities();
            notifySuccess('Festivity successfully eliminated!');
          })
          .catch(error => {
            notifyError('Error deleting the holiday. Please try again.');
          });
    },
    fetchFestivities() {
      fetch(`${BACKEND_HOST}festivity/get-all-festivities`, {
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        }
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('The festivities could not be obtained.');
            }
            return response.json();
          })
          .then(data => {
            this.festividades = data;
            this.printCalendar();
          })
          .catch(error => {
            console.error(error);
            notifyError('The festivities could not be obtained.');
          });
    },
    printCalendar() {
      this.attrs.splice(0);
      this.festividades.forEach(festivity => {
        const cityColor = this.cities.find(city => city.value === festivity.City)?.color || 'red';
        this.attrs.push({
          key: festivity.ID,
          dot: cityColor,
          dates: festivity.Date,
        });
      });
    },
    formatDate(date) {
      const options = {day: '2-digit', month: '2-digit', year: 'numeric'};
      return new Date(date).toLocaleDateString('es-ES', options);
    },
  },
  computed: {
    filteredFestivities() {
      return this.selectedCities.length === 0 ? this.festividades :
          this.festividades.filter(festivity => this.selectedCities.includes(festivity.City));
    }
  },
  created() {
    this.fetchFestivities();
  }
}
</script>

<style scoped>
.btn-group .btn {
  margin-right: 5px;
}

.btn-group {
  margin-bottom: 10px;
}

.card {
  flex: 1 1 0;
}
</style> -->
