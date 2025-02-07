<template>
  <main>
    <h1 class="fs-3 fw-bold pt-2">Home Office</h1>
    <div class="w-100 text-center d-flex justify-content-center align-items-center flex-column mt-5">
      <h3 class="fs-5 fw-medium">My calendar</h3>

      <div class="calendar-container d-flex flex-column justify-content-center align-items-center w-100">
        <div class="mb-3 mt-4 w-100 d-flex justify-content-center">
          <div class="info-container">
            <div class="info-container w-100">
              <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
              <div class="legend-container">
                <div class="d-flex flex-row justify-content-center gap-3 font-small mb-2">
                  <span>Home-Office:</span>
                  <div class="d-flex align-items-center font-small">
                    <span class="legend-color mr-1 darkBlue"></span> Office
                  </div>
                  <div class="d-flex align-items-center font-small">
                    <span class="legend-color mr-1 lightBlue"></span> Partial
                  </div>
                  <div class="d-flex align-items-center font-small">
                    <span class="legend-color mr-1 blue"></span> Full
                  </div>
                </div>
                <div class="d-flex flex-row justify-content-center gap-3 font-small">
                  <span>Amount of people working remotely:</span>
                  <div class="d-flex align-items-center gap-2">
                    <span class="legend-line brand-30 mr-1"></span> {{ "<33%" }}
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <span class="legend-line brand-60 mr-1"></span> 33%-66%
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <span class="legend-line bg-main mr-1"></span> >66%
                  </div>
                </div>
              </div>
            </div>
            <v-date-picker v-model="selectedDay" :attributes="combinedAttrs" class="custom-date-picker"
              v-model.range.number="range" show-weeknumbers="right"
              style="font-size: 1.5rem; width: 100%; max-width: 500px;">
              <template #day-popover="{ day, format, masks, attributes }">
                <div class="small ho-user text-capitalize">
                  {{ format(day.date, masks.dayPopover) }}
                </div>
                <!-- Código para sacar también tu nombre, comentado porque en este momento no es necesario, pero si se quisiera para el futuro está hecho -->
                <!-- <div v-if="attributes && attributes.length">
                  <div v-for="{ key, customData } in attributes" :key="key">
                    <div v-if="customData && customData.Type">
                      <span :class="customData.Type.toLowerCase()"></span>
                      <span class="small">
                        {{ customData.Type[0] + customData.Type.substring(1).toLowerCase() }} (You)
                      </span>
                    </div>
                  </div>
                </div> -->
                <div v-if="attributes && attributes.length">
                  <div v-for="{ key, customData } in attributes" :key="key">
                    <div v-if="customData.FULL">
                      <div>
                        <span class="dot full"></span>
                        <span class="small">Full Office</span>
                      </div>
                      <ul class="list-unstyled mb-0">
                        <li v-for="user in customData.FULL" :key="user.FullName" class="ho-user">
                          {{ user.FullName }}
                        </li>
                      </ul>
                    </div>
                    <div v-if="customData.PARTIAL">
                      <div>
                        <span class="dot partial"></span>
                        <span class="small">Partial Office</span>
                      </div>
                      <ul class="list-unstyled mb-0">
                        <li v-for="user in customData.PARTIAL" :key="user.FullName" class="ho-user">
                          {{ user.FullName }}
                        </li>
                      </ul>
                    </div>
                    <div v-if="customData.OFFICE">
                      <div>
                        <span class="dot office"></span>
                        <span class="small">Office</span>
                      </div>
                      <ul class="list-unstyled mb-0">
                        <li v-for="user in customData.OFFICE" :key="user.FullName" class="ho-user">
                          {{ user.FullName }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </template>
            </v-date-picker>
          </div>
        </div>

        <!-- Agrupación de los radio buttons en una fila -->
        <form class="text-center w-100" id="homeOfficeForm">
          <div class="form-group mb-2 d-flex justify-content-center gap-4">
            <div class="form-check">
              <input class="form-check-input" type="radio" name="option" id="partial" value="PARTIAL" v-model="selectedOption" />
              <label class="form-check-label" for="partial">Partial Remote</label>
            </div>

            <div class="form-check">
              <input class="form-check-input" type="radio" name="option" id="full" value="FULL" v-model="selectedOption" />
              <label class="form-check-label" for="full">Full Remote</label>
            </div>

            <div class="form-check">
              <input class="form-check-input" type="radio" name="option" id="office" value="OFFICE" v-model="selectedOption" />
              <label class="form-check-label" for="office">Office</label>
            </div>
          </div>

          <div class="d-flex justify-content-center gap-2 mt-3">
            <button type="button" class="btn btn-primary bg-main" @click="sendForm">Send</button>
            <button type="button" title="Delete" class="btn btn-secondary" @click="removeHomeOffice">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>




<script>
import { loadingMessage, notifyError, notifySuccess, stopLoadingMessage } from '@/assets/globalFunctions';
import { BACKEND_HOST } from '../config';
import { ref, computed } from 'vue';


export default {
  data() {
    return {
      range: {
        start: new Date(),
        end: new Date(),
      },
      selectedDay: null,
      selectedOption: null,
      userDays: [],
      attrs: [],
      attrs2: [],
      departmentDays: [],
      users: [],
      eventColor: ""
    };
  },
  created() {
    this.fetchDays();
  },
  computed: {
    combinedAttrs() {
      // Fusionar los atributos de ambos calendarios
      return [...this.attrs, ...this.attrs2];
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      return `${day}/${month}/${year}`;
    },
    async sendForm() {
      if (!this.selectedDay || !this.selectedOption) {
        notifyError("Select a day and option.");
        return;
      }

      loadingMessage();

      let { start, end } = this.selectedDay;
      const weekdays = [];
      const startDate = new Date(start);
      const endDate = new Date(end);
      const currentDate = new Date(startDate);

      const SUNDAY = 0;
      const SATURDAY = 6;

      while (currentDate <= endDate) {
        const dayOfWeek = currentDate.getDay();
        if (dayOfWeek !== SATURDAY && dayOfWeek !== SUNDAY) {
          weekdays.push(new Date(currentDate));
        }
        currentDate.setDate(currentDate.getDate() + 1);
      }

      let reqs = weekdays.map(day => {
        const formattedDate = this.formatDate(day);

        const data = {
          day: formattedDate,
          type: this.selectedOption
        };

        return fetch(`${BACKEND_HOST}home-office/add-home-office`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
      });

      Promise.all(reqs)
        .then(async responses => {
          responses.forEach(async response => {
            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.state);
            }
          });
          await this.fetchDays();
          this.selectedDay = {};
        })
        .catch(error => {
          console.error("Error occurred during requests:", error);
        })
        .finally(() => {
          stopLoadingMessage();
        });
    },

    async removeHomeOffice() {
      if (!this.selectedDay) {
        notifyError("Select a day to delete");
        return;
      }

      loadingMessage();

      let { start, end } = this.selectedDay;
      const weekdays = [];
      const startDate = new Date(start);
      const endDate = new Date(end);
      const currentDate = new Date(startDate);

      const SUNDAY = 0;
      const SATURDAY = 6;

      while (currentDate <= endDate) {
        const dayOfWeek = currentDate.getDay();
        if (dayOfWeek !== SATURDAY && dayOfWeek !== SUNDAY) {
          weekdays.push(new Date(currentDate));
        }
        currentDate.setDate(currentDate.getDate() + 1);
      }

      let reqs = weekdays.map(day => {
        const formattedDate = this.formatDate(day);

        const data = {
          day: formattedDate,
        };

        return fetch(`${BACKEND_HOST}home-office/delete-home-office`, {
          method: 'DELETE',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
      });

      Promise.all(reqs)
        .then(async responses => {
          responses.forEach(async response => {
            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.state);
            }
          });
          await this.fetchDays();
          notifySuccess('Selected days have been deleted successfully');
          this.selectedDay = {};
        })
        .catch(error => {
          console.error("Error occurred during delete requests:", error);
          notifyError(error.message);
        })
        .finally(() => {
          stopLoadingMessage();
        });
    },

    async fetchDays() {
      loadingMessage();
      try {
        const response = await fetch(`${BACKEND_HOST}home-office/get-home-office`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error);
        }

        const data = await response.json();
        this.userDays = data;


        await this.fetchDepartmentDays();

        await this.printUserDays();

      } catch (error) {
        notifyError(error.message);
        stopLoadingMessage();

      }
    },
    async fetchDepartmentDays() {
      try {
        const response = await fetch(`${BACKEND_HOST}home-office/get-department-home-office`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.state);
        }

        const data = await response.json();
        this.departmentDays = data;

        await this.fetchUsers();
        
        stopLoadingMessage();
      } catch (error) {
        notifyError(error.message);
        stopLoadingMessage();

      }
    },
    //ESTO ES SOLO PARA SABER CUANTA MÁS GENTE HAY EN EL DEPATAMENTO (calcular porcentajes)
    async fetchUsers() {
      try {
        const response = await fetch(`${BACKEND_HOST}user/get-department-partners`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.state);
        }

        const data = await response.json();
        this.users = data;

        await this.printDepartmentDays();
      } catch (error) {
        notifyError(error.message);
        stopLoadingMessage();
      }
    },
    async printUserDays() {
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

      this.userDays.forEach(day => {
        let highlightColor;
        switch (day.Type) {
          case 'PARTIAL':
            highlightColor = 'lightBlue';
            break;
          case 'FULL':
            highlightColor = 'blue';
            break;
          case 'OFFICE':
            highlightColor = 'purple';
            break;
          default:
            highlightColor = 'gray';
        }
        this.attrs.push({
          key: day.Date,
          highlight: {
            class: highlightColor
          },
          popover: { visibility: 'hover' },
          customData: day,
          dates: day.Date
        });
      });
    },
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },

    printDepartmentDays() {
      this.attrs2.splice(0);


      const weekends = ref([
        {
          description: 'weekend',
          isComplete: false,
          dates: { repeat: { weekdays: [1, 7] } }, // Every Saturday and Sunday
        },
      ]);

      this.attrs2 = computed(() => [
        ...weekends.value.map(day => ({
          dates: day.dates,
          content: {
            color: 'weekend',
            class: 'weekend',
          },
        })),
      ]);

      const daysGroupedByDate = this.departmentDays.reduce((acc, curr) => {
        const date = new Date(curr.Date).toDateString();
        if (!acc[date]) {
          acc[date] = [];
        }
        acc[date].push(curr);
        return acc;
      }, {});

      for (const dateKey in daysGroupedByDate) {
        let date = new Date(dateKey);
        let usersInDate = daysGroupedByDate[dateKey];
        let groupedUsersByType = Object.groupBy(usersInDate, ({ Type }) => Type);

        const nonOfficeCount = usersInDate.filter(user => user.Type !== 'OFFICE').length;
        const totalDayCount = this.users.length;
        const nonOfficePercentage = (nonOfficeCount / totalDayCount) * 100;

        let highlightColor;

        if (nonOfficePercentage < 33) {
          highlightColor = 'brand-30';
        } else if (nonOfficePercentage >= 33 && nonOfficePercentage <= 66) {
          highlightColor = 'brand-60';
        } else {
          highlightColor = 'bg-main';
        }

        this.attrs2.push({
          bar: {
            show: true,
            class: highlightColor,
          },
          popover: { visibility: 'hover' },
          customData: groupedUsersByType,
          dates: date
        });
      }
    },
  }
};
</script>

<style>
.legend-color {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.full,
.partial,
.office {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

.ho-user {
  line-height: 0.9rem;
  font-size: 0.7rem;
}

.blue,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-blue,
.full {
  background-color: #0075C2 !important;
}

.lightBlue,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.partial {
  background-color: #06B4E9 !important;
}

.purple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-purple,
.office {
  background-color: #0B318F !important;
}

.brand-90 {
  background-color: #431B98;
}

.brand-70 {
  background-color: #6D4DAE;
}

.brand-60 {
  background-color: #8266BA;
}

.brand-50 {
  background-color: #9681C6;
}

.brand-40 {
  background-color: #AC99D1;
}

.brand-30 {
  background-color: #C1B2DD;
}

.brand-20 {
  background-color: #cab9f0;
}

.legend-line {
  display: inline-block;
  width: 20px;
  height: 5px;
  border-radius: 20%;
}

.vc-bars {
  justify-content: center;
}

.vc-bar {
  flex-grow: 0.4;
}

.green {
  background-color: #46B036;
}

.orange {
  background-color: #FFB54C;
}

.red {
  background-color: #EC6D74;
}

#partial:checked {
  background-color: #06B4E9;
  border: 2px solid #06B4E9;
  box-shadow: 0 0 10px #06B4E9;
}

#full:checked {
  background-color: #0075C2;
  border: 2px solid #0075C2;
  box-shadow: 0 0 10px #0075C2;
}

#office:checked {
  background-color: #7B639F;
  border: 2px solid #7B639F;
  box-shadow: 0 0 10px #7B639F;
}

#personalCalendar .vc-day-layer.vc-highlights:not(:has( :is(.lightBlue, .blue, .purple))) .vc-highlight {
  /*background-color: transparent;*/
  background-color: #f1f1f1;
  /*border: 2px solid #3f61e8;*/
  border: 2px solid #e7e7e7;
}

#personalCalendar .vc-day-layer.vc-highlights:not(:has( :is(.lightBlue, .blue, .purple)))+.vc-attr.vc-blue.vc-day-content.vc-focus.vc-focusable.vc-highlight-content-solid {
  color: black;
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

.legend {
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.info-container {
  width: 510px;
}
</style>
