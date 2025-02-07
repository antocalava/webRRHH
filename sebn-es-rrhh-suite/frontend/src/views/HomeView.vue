<template>
  <main class="mt-3 mx-2 flex-body">
    <div class="container">
      <div class="row">
        <!-- Parte izquierda: Gráficas, Tabla en medio y otra Tabla debajo -->
        <div class="col-8">

          <!-- Gráficas y tabla en la parte superior -->
          <div class="d-flex justify-content-between mb-4 mt-3">

            <!-- HOME OFFICE GRAPH -->
            <div class="col-6">
              <h5 class="text-center fw-bold">Monthly home-office</h5>
              <!-- Texto con el nombre del mes en gris y pequeño -->
              <p class="text-center text-muted small">
                {{ currentMonthText[0].toUpperCase() + currentMonthText.substring(1).toLowerCase() }}
              </p>
              <div class="chart" id="chart-container-days-worked"></div>
              <div class="col-8 mx-auto">
                <!-- Legend for Home-office Graph -->
                <div class="legend d-flex justify-content-between mt-1">
                  <div class="d-flex align-items-center me-3 pl-5">
                    <div class="color-box" style="background-color: #0c359d;"></div>
                    <span class="legend-text">Office</span>
                  </div>
                  <div class="d-flex align-items-center">
                    <div class="color-box" style="background-color: #0080d5;"></div>
                    <span class="legend-text">Full</span>
                  </div>
                  <div class="d-flex align-items-center pr-5">
                    <div class="color-box" style="background-color: #06c6ff;"></div>
                    <span class="legend-text">Partial</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- VACATIONS GRAPH -->
            <div class="col-6">
              <h5 class="text-center fw-bold">Holidays this year</h5>
              <!-- Texto con el año actual en gris y pequeño -->
              <p class="text-center text-muted small">{{ currentYear }}</p>
              <div class="chart" id="chart-container-vacations"></div>
              <div class="col-8 mx-auto">
                <!-- Legend for Vacations Graph -->
                <div class="legend d-flex justify-content-between mt-1">
                  <div class="d-flex align-items-center me-3 pl-5">
                    <div class="color-box" style="background-color: #ff949b;"></div>
                    <span class="legend-text w-50">Used</span>
                  </div>
                  <div class="d-flex align-items-center pr-5">
                    <div class="color-box" style="background-color: #ffcdd1;"></div>
                    <span class="legend-text">Remaining</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- USER BUCKETS TABLE -->
          <div class="table-container mb-4">
            <div class="table-title text-white py-2 px-3" style="background-color: #3A3B76;">
              Vacation days available per user bucket
            </div>
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">Bucket</th>
                  <th scope="col">Days</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bucket in userDaysBuckets" :key="bucket.BucketName">
                  <td>{{ bucket.BucketName }}</td>
                  <td>{{ bucket.BucketValue }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Parte derecha: Leyenda y Calendarios -->
        <div class="col-4">
          <!-- Calendarios uno debajo del otro -->
          <div class="row">
            <div class="info-container mt-2">
              <i class="fa-solid fa-circle-info info-icon" @click="toggleLegend()" title="What do these colors mean?"></i>
              <div class="legend-container">
                <div class="d-flex flex-row justify-content-center gap-3 mb-2 font-small">
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

                <div class="d-flex flex-row justify-content-center gap-3 mt-2 font-small">
                  <span>Festivities:</span>
                  <div class="d-flex align-items-center font-small">
                    <span class="legend-color mr-1 festivity"></span> Festivity
                  </div>
                </div>
              </div>
            </div>
            <div class="col-12 my-calendar">
              <VCalendar class="mt-2" expanded show-weeknumbers="right" :attributes="attrs" :rows="3">
                <template #day-popover="{ day, format, masks, attributes }">
                  <div class="small ho-user text-center text-capitalize">
                    {{ format(day.date, masks.dayPopover) }}
                  </div>
                  <div v-for="{ key, customData } in attributes" :key="key">
                    <div>
                      <span
                        :class="customData.Type.toLowerCase().replace(/&/g, '').replace(/\s(.)/g, (match, group1) => group1.toUpperCase()).replace(/\s+/g, '')"></span>
                      <span class="small">{{ customData.Type[0] + customData.Type.substring(1).toLowerCase() }}</span>
                    </div>
                  </div>
                </template>
              </VCalendar>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<!-- Aquí hago el setup de getUsername para que pueda cargarme al entrar sin problemas. -->
<script setup>
import { getUsername } from '@/assets/globalFunctions';
</script>

<script>
import { getUsername, formatDate, loadingMessage, notifyError, stopLoadingMessage } from '@/assets/globalFunctions';
import { BACKEND_HOST } from '../config';
import * as echarts from 'echarts';
import { ref, computed } from 'vue';

export default {
  data() {
    const currentMonthText = new Date().toLocaleString('default', { month: 'long' });
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const minDate = new Date(currentYear, currentMonth, 1);
    return {
      range: {
        start: new Date(),
        end: new Date(),
      },
      selectedDay: null,
      currentMonthText: new Date().toLocaleString('en-US', { month: 'long' }),
      currentYear: new Date().getFullYear(),
      selectedOption: null,
      attrs: [],
      attrs2: [],
      eventsCalendarDays: [],
      users: [],
      eventColor: "",
      userDaysBuckets: null,
      minDate: minDate
    };
  },
  async created() {
    this.fetchCalendars();
    loadingMessage();
    this.createChart(`/home/get-graph-home-office`, ['#0075c2', '#0B318F', '#06B4E9'], "chart-container-days-worked");
    this.createChart(`/home/get-graph-vacations`, ['#EEBBBE', '#ED878D'], "chart-container-vacations");
    if (!this.userBuckets) this.fecthUserBuckets();
  },
  methods: {
    formatDate(date) {
      return formatDate(date);
    },
    /**
    * Obtiene la fecha del mes anterior o siguiente al actual.
    * 
    * @param {string} tipo - Un string que debe ser "anterior" o "siguiente".
    * @returns {string} Una cadena que representa la fecha en el formato new Date(YYYY, MM, DD).
    */
    obtenerMes(tipo) {
      const fechaActual = new Date();
      const añoActual = fechaActual.getFullYear();
      const mesActual = fechaActual.getMonth();
      const diaActual = fechaActual.getDate();

      let nuevoAño, nuevoMes;
      if (tipo === "anterior") {
        if (mesActual === 0) { // Si es enero (mes 0), el mes anterior es diciembre del año anterior
          nuevoAño = añoActual - 1;
          nuevoMes = 11; // Diciembre
        } else {
          nuevoAño = añoActual;
          nuevoMes = mesActual - 1;
        }
      } else if (tipo === "siguiente") {
        if (mesActual === 11) { // Si es diciembre (mes 11), el mes siguiente es enero del siguiente año
          nuevoAño = añoActual + 1;
          nuevoMes = 0; // Enero
        } else {
          nuevoAño = añoActual;
          nuevoMes = mesActual + 1;
        }
      } else if (tipo === "siguiente2") {
        if (mesActual === 10) { // Si es diciembre (mes 11), el mes siguiente es enero del siguiente año
          nuevoAño = añoActual + 1;
          nuevoMes = 0; // Enero
        } else if (mesActual === 11) {
          nuevoAño = añoActual + 1;
          nuevoMes = 1; // Febrero
        } else {
          nuevoAño = añoActual;
          nuevoMes = mesActual + 2;
        }
      } else {
        throw new Error('El parámetro debe ser "anterior" o "siguiente".'); 
      }

      const nuevaFecha = new Date(nuevoAño, nuevoMes, 1);
      const fechaFormateada = this.formatDate(nuevaFecha);
      return fechaFormateada;
    },
    getMaxDate() {
      const currentDate = new Date();
      const nextTwoMonths = new Date(currentDate.getFullYear(), currentDate.getMonth() + 2, 1);
      return nextTwoMonths;
    },
    async fetchCalendars() {
      try {
        const response = await fetch(`${BACKEND_HOST}/home/get-calendars-info`, {
          method: 'POST',
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
        this.eventsCalendarDays = data;
        this.printCalendarEvents();
        stopLoadingMessage();
      } catch (error) {
        stopLoadingMessage();
        notifyError(error.state);
      }
    },
    /**
    * Esta función busca para el primer gráfico los días que ha trabajado y de qué tipo.
    * @var urlBackend String { Es la url del backend para llamar a los datos del chart}
    * @var colors Array String { Son los colores que van a tener las partes de la chart}
    * @var nombreContainer String { Nombre del container que va a contener el chart }
    * @var labelChart String { Titulo que tiene al hacer hover el chart que sea }
    */
    async createChart(urlBackend, colors, nombreContainer, labelChart) {
      try {
        const response = await fetch(`${BACKEND_HOST}` + urlBackend, {
          method: 'POST',
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

        // Cómo hacer una de estas pies y la documentación de las mismas está en echarts.apache.org
        let chartDom = document.getElementById(nombreContainer);
        /**
        * ↓ súper importante, cuando se van a otra página y vuelven comprueba si existe la instancia y la borra si es así.
        */
        if (chartDom.querySelector('div')) {
          echarts.getInstanceByDom(chartDom).dispose();
        }
        let myChart = echarts.init(chartDom);

        // ↓ Cuando cambie la ventana de tamaño se actualizan los charts.
        window.addEventListener('resize', function () {
          myChart.resize();
        });

        let option;
        let colorPalette = colors;
        myChart.showLoading();

        let dataArray = [];

        for (let key in data) {
          dataArray.push({ value: data[key], name: key });
        }

        option = {
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              name: labelChart,
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                position: 'outside',
                formatter: function (params) {
                  let value = parseFloat(params.value);
                  return Number.isInteger(value) ? value : value.toFixed(2);
                },
                fontSize: 12,
                color: '#333',
                fontWeight: 'bold'
              },
              labelLine: {
                show: true,
                length: 10,
                lineStyle: {
                  color: '#333'
                }
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 13,
                  fontWeight: 'bold'
                }
              },
              data: dataArray,
              color: colorPalette
            }
          ]
        };

        myChart.hideLoading();
        option && myChart.setOption(option);

      } catch (error) {
        console.error("Failed to load or could not finish loading pie charts from Home Page: " + error.message)
      }
    },
    printCalendarEvents() {
      this.attrs.splice(0);

      const weekends = ref([
        {
          description: 'weekend',
          isComplete: false,
          dates: { repeat: { weekdays: [1, 7] } }, // Every Saturday and Sunday
        },
      ]);

      const colorMapping = {
        PARTIAL: 'lightBlue',
        FULL: 'blue',
        OFFICE: 'pink',
        HOLIDAYS: { default: 'yellow', CREATED: 'lightYellow' },
        FESTIVITY: 'green',
        TRAVEL: { default: 'lightPurple', CREATED: 'lighterPurple', SIGNED: 'purpleAux' },
      };

      const combinationMapping = {
        'FULL & TRAVEL': { default: 'bluepurple', CREATED: 'bluelightPurple' },
        'OFFICE & TRAVEL': { default: 'darkbluepurple', CREATED: 'darkbluelightPurple' },
        'PARTIAL & TRAVEL': 'lightbluepurple',
        'FULL & HOLIDAYS': { default: 'blueyellow', CREATED: 'bluelightYellow' },
        'OFFICE & HOLIDAYS': { default: 'darkblueyellow', CREATED: 'darkbluelightYellow' },
        'PARTIAL & HOLIDAYS': { default: 'lightblueYellow', CREATED: 'lightbluelightYellow' },
        'FESTIVITY & TRAVEL': { default: 'greenpurple', CREATED: 'greenlightPurple', REJECTED: 'greenred' },
        'OFFICE & FESTIVITY': 'darkbluegreen',
        'PARTIAL & FESTIVITY': 'lightbluegreen',
        'FULL & FESTIVITY': 'bluegreen',
        'HOLIDAYS & TRAVEL': 'yellowpurple'
      };

      const getColor = (type, state) => {
        const color = colorMapping[type];
        if (typeof color === 'object') {
          return color[state] || color.default;
        }
        return color;
      };

      const getCombinationColor = (combination, state) => {
        const color = combinationMapping[combination];
        if (typeof color === 'object') {
          return color[state] || color.default;
        }
        return color;
      };

      this.attrs = computed(() => [
        ...weekends.value.map(day => ({
          dates: day.dates,
          content: {
            color: 'weekend',
            class: 'weekend',
          },
        })),
      ]);

      for (const [date, events] of Object.entries(this.eventsCalendarDays)) {
        let valueType = '';
        let highlightColor = 'gray';
        let createdState = false;

        const eventTypes = events.map(([type, details]) => {
          const state = details ? details[1] : null;
          createdState = state === 'CREATED';
          return { type, state };
        });

        if (eventTypes.length === 1) {
          const { type, state } = eventTypes[0];
          highlightColor = getColor(type, state);
          valueType = type;
        } else {
          // Combinar tipos para manejar múltiples eventos
          valueType = eventTypes.map(e => e.type).join(' & ');
          const lastState = eventTypes[eventTypes.length - 1].state;
          highlightColor = getCombinationColor(valueType, lastState);
        }

        let day = {
          Date: date,
          Type: valueType,
        };

        // Condición para cambiar la clase de 'content' si es un 'TRAVEL' con estado 'CREATED'
        let contentClass = 'white';
        if (valueType === 'TRAVEL' && createdState) {
          contentClass = 'travelCreatedFont';
        } else if (valueType === 'HOLIDAYS' && createdState) {
          contentClass = 'holidayCreatedFont';
        }

        // Añadir al calendario
        this.attrs.push({
          key: day.Date,
          highlight: {
            class: highlightColor,
          },
          content: {
            class: contentClass,
          },
          popover: { visibility: 'hover' },
          customData: day,
          dates: day.Date,
        });
      }
    },
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },
    async fecthUserBuckets() {
      let json = {
        'email': null
      }
      try {
        loadingMessage();
        const response = await fetch(`${BACKEND_HOST}hr/get-user-days-buckets`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(json)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Unable to load user bucket days: ' + (error.message || error.state));
        }

        const data = await response.json();
        this.userDaysBuckets = data
        stopLoadingMessage();
      } catch (error) {
        this.showError(error);
      }
    },
  }
};
</script>


<style>
/* Los colores del tipo de dato en el homeView */
:root {
  --partial: #06B4E9;
  --full: #0075C2;
  --office: #0B318F;
  --holidays: #ca8a04;
  --holidaysCreated: #e4c071;
  --travel: #9333ea;
  --festivity: #45B035;
  --travelInProcess: #c999f4;
  --travelCreated: #9333ea;
}

.chart {
  position: relative;
  height: 30vh;
  overflow: hidden;
}

.legend-color {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.full,
.partial,
.officeHome,
.holidays,
.festivity,
.officeholidays,
.partialholidays,
.fulltravel,
.officetravel,
.fullholidays,
.festivitytravel,
.holidaytravel,
.officefestivy,
.partialfestivity,
.fullfestivity,
.travelSigned,
.travelCreated,
.travel,
.officefestivity {
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
  background-color: var(--partial) !important;
}

.pink,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-purple,
.officeHome {
  background-color: var(--office) !important;
}

.green,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-green,
.festivity {
  background-color: var(--festivity) !important;
}

.yellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-red,
.holidays {
  background-color: var(--holidays) !important;
}

.lightYellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-red,
.holidaysCreated {
  background: transparent !important;
  border: 2px solid var(--holidaysCreated) !important;
}

.darkPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travel {
  background-color: var(--travel) !important;
}

.darkblueyellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.officeholidays {
  background: linear-gradient(to right, var(--office) 50%, var(--holidays) 50%);
}

.darkbluelightYellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.officeholidays {
  background: linear-gradient(to right, var(--office) 50%, var(--holidaysCreated) 50%);
}

.lightblueyellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.partialholidays {
  background: linear-gradient(to right, var(--partial) 50%, var(--holidays) 50%);
}

.lightbluelightYellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.partialholidays {
  background: linear-gradient(to right, var(--partial) 50%, var(--holidaysCreated) 50%);
}

.bluepurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.fulltravel {
  background: linear-gradient(to right, var(--full) 50%, var(--travel) 50%);
}

.bluelightPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.fulltravel {
  background: linear-gradient(to right, var(--full) 50%, var(--travelCreated) 50%);
}

.yellowpurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.holidaystravel {
  background: linear-gradient(to right, var(--holidays) 50%, var(--travel) 50%);
}

.purpleAux,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travelSigned {
  background: var(--travel) !important;
}

.lightPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travelInProgress {
  background: var(--travelInProcess) !important;
}


.lighterPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travelCreated {
  background: transparent !important;
  border: 2px solid var(--travelCreated) !important;
}

.travelCreatedFont {
  color: var(--travelCreated) !important;
}

.holidayCreatedFont {
  color: var(--holidaysCreated) !important;
}

.darkbluepurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.officetravel {
  background: linear-gradient(to right, var(--office) 50%, var(--travel) 50%);
}

.darkbluelightPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.officetravel {
  background: linear-gradient(to right, var(--office) 50%, var(--travelCreated) 50%);
}

.blueyellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.fullholidays {
  background: linear-gradient(to right, var(--full) 50%, var(--holidays) 50%);
}

.bluelightYellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.fullholidays {
  background: linear-gradient(to right, var(--full) 50%, var(--holidaysCreated) 50%);
}

.greenpurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.festivitytravel {
  background: linear-gradient(to right, var(--festivity) 50%, var(--travel) 50%);
}

.greenlightPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.festivitytravel {
  background: linear-gradient(to right, var(--festivity) 50%, var(--travelCreated) 50%);
}

.redpurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.holidaytravel {
  background: linear-gradient(to right, var(--holiday) 50%, var(--travel) 50%);
}

.bluegreen,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.officefestivity {
  background: linear-gradient(to right, var(--office) 50%, var(--festivity) 50%);
}

.lightbluegreen,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.partialfestivity {
  background: linear-gradient(to right, var(--partial) 50%, var(--festivity) 50%);
}

.darkbluegreen,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.fullfestivity {
  background: linear-gradient(to right, var(--full) 50%, var(--festivity) 50%);
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
  background-color: #cab9f0
    /*#D5CCE9*/
  ;
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

#holidays:checked {
  background-color: #45B035;
  border: 2px solid #45B035;
  box-shadow: 0 0 10px #45B035;
}

#festivity:checked {
  background-color: #EC6D74;
  border: 2px solid #EC6D74;
  box-shadow: 0 0 10px #EC6D74;
}

#travelSigned.checked {
  background-color: var(--travel);
  border: 2px solid var(--travel);
  box-shadow: 0 0 10px var(--travel);
}

.weekend {
  /* color: #a7a7a7 !important; */
  color: #000000 !important;
  opacity: 0.3;
}

.legend-container {
  width: 92%;
  margin: 0 auto;
}

.legend-color {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: currentColor;
}

.mb-4 {
  margin-bottom: 10px;
}

.w-80 {
  width: 80%;
}

.container {
  margin-left: 20px !important;
  margin-right: 20px !important;
  max-width: 1800px !important;
}

#bodyApp {
  padding: 0px 80px 0px 100px;
}

.color-box {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  margin-right: 2px;
  /* Reducido para disminuir el espacio entre el color box y el texto */
}

.legend {
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.legend-text {
  margin-left: 2px;
  /* Reducido para disminuir el espacio entre el color box y el texto */
}
</style>