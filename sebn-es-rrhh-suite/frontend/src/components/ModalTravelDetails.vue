<template>
  <div v-if="isLoading" class="loading-overlay d-flex justify-content-center align-items-center">
    <div class="loading-spinner"></div>
  </div>

  <div id="travelForm" class="px-10 pb-10 mt-4" :class="{ 'modal-blur': isLoading }">
    <div class="row">
      <form>
        <!-- name & cost center -->
        <div class="mb-3 row">
          <div class="col-md-6">
            <label for="userFullName" class="form-label">Employee's name</label>
            <input type="text" class="form-control" id="userFullName" v-model="form.userFullName" readonly disabled
              required />
          </div>
          <div class="col-md-6">
            <label for="costCenter" class="form-label">Cost center</label>
            <input type="number" step="1" min="0" class="form-control" id="costCenter" disabled v-model="form.costCenter"
              required>
          </div>
        </div>

        <!-- dates & duration -->
        <div class="row mb-3" id="datesContainer">
          <div class="col-md-4">
            <label for="dateFrom" class="form-label">Date from</label>
            <input type="date" class="form-control" id="dateFrom" v-model="form.dateFrom" required @change="calcDayAmount"
              disabled />
          </div>
          <div class="col-md-4">
            <label for="dateTo" class="form-label">Date to</label>
            <input type="date" class="form-control" id="dateTo" v-model="form.dateTo" required @change="calcDayAmount"
              disabled />
          </div>
          <div class="col-md-4">
            <label for="dayAmount" class="form-label">Day amount</label>
            <input type="number" class="form-control" id="dayAmount" v-model="form.dayAmount" min="0" readonly disabled>
          </div>
        </div>

        <!-- destination -->
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="destination" class="form-label">Destination country</label>
            <input id="destination" class="form-control" v-model="form.destination" required disabled />
          </div>

          <div class="col-md-6">
            <label for="address" class="form-label">Address/es</label>
            <textarea type="text" class="form-control" id="address" v-model="form.address" required style="height: 40px;"
              maxlength="140" disabled></textarea>
          </div>
        </div>

        <div class="row mb-3">
          <!-- added value-->
          <div class="mb-3 col-md-6">
            <label class="form-label">Trip creates added value</label>
            <div>
              <div class="form-check form-check-inline d-inline-flex align-items-center gap-2">
                <input class="form-check-input" type="radio" name="addedValueRadio" id="addedValueTrue" value="1"
                  v-model="form.addedValue" disabled />
                <label class="form-check-label" for="addedValueTrue">Yes</label>
              </div>
              <div class="form-check form-check-inline d-inline-flex align-items-center gap-2">
                <input class="form-check-input" type="radio" name="addedValueRadio" id="addedValueFalse" value="0"
                  v-model="form.addedValue" disabled />
                <label class="form-check-label" for="addedValueFalse">No</label>
              </div>
            </div>
          </div>

          <!-- advance payment-->
          <div class=" col-md-6 d-block">
            <div class="row mb-3 ">
              <label class="form-label" for="advancePaymentCheck" style="width:fit-content">Request advance
                payment?</label>
              <input class="form-check-input" type="checkbox" id="advancePaymentCheck" value="1"
                v-model="form.advancePayment" disabled />
            </div>

            <div v-if="form.advancePayment" class="row">
              <label class="form-label" for="advancePaymentAmount" style="width:fit-content">Amount</label>
              <input class="form-control" type="number" id="advancePaymentAmount" v-model="form.advancePaymentAmount"
                min="0" value="0" step="any" required style="width:50%" disabled />
              <!-- tanto el punto como la coma te lo transforman en DECIMAL-->
            </div>
          </div>
        </div>

        <!-- reason -->
        <div class="col-mb-12 mb-3">
          <label for="reason" class="form-label">Reason</label>
          <textarea class="form-control" id="reason" v-model="form.reason" rows="3" required disabled></textarea>
        </div>

        <!-- transport -->
        <div class="row mb-3">
          <label class="form-label">Means of transport:</label>
          <div class="d-flex" id="transportContainer">
            <div class="form-check d-flex align-items-center gap-2">
              <input class="form-check-input" type="checkbox" id="Plane" v-model="form.transport['Plane']" disabled />
              <label class="form-check-label" for="Plane">Plane</label>
            </div>
            <div class="form-check d-flex align-items-center gap-2 ml-6">
              <input class="form-check-input" type="checkbox" id="Train" v-model="form.transport['Train']" disabled />
              <label class="form-check-label" for="Train">Train</label>
            </div>
            <div class="form-check d-flex align-items-center gap-2 ml-6">
              <input class="form-check-input" type="checkbox" id="RentCar" v-model="form.transport['RentCar']" disabled />
              <label class="form-check-label" for="RentCar">Rented vehicle</label>
            </div>
            <div class="form-check d-flex align-items-center gap-2 ml-6">
              <input class="form-check-input" type="checkbox" id="BusinessCar" v-model="form.transport['BusinessCar']"
                disabled />
              <label class="form-check-label" for="BusinessCar">Business vehicle</label>
            </div>
            <div class="form-check d-flex align-items-center gap-2 ml-6">
              <input class="form-check-input" type="checkbox" id="PrivateCar" v-model="form.transport['PrivateCar']"
                disabled />
              <label class="form-check-label" for="PrivateCar">Private vehicle</label>
            </div>
            <div class="form-check d-flex align-items-center gap-2 ml-6">
              <input class="form-check-input" type="checkbox" id="Taxi" v-model="form.transport['Taxi']" disabled />
              <label class="form-check-label" for="Taxi">Taxi - pick-up</label>
            </div>
          </div>
        </div>

      </form>
    </div>
  </div>

</template>

<script>
import { formatDate2, notifyError } from "@/assets/globalFunctions";
import { BACKEND_HOST } from '../config';

export default {
  name: 'ModalTravelDetails',
  data() {
    return {
      userFullName: "",
      selectedTravel: [],
      transportNamesOrder: ['Plane','Train','RentCar','BusinessCar','PrivateCar','Taxi'],

      form: {
        userFullName: '',
        destination: '',
        address: '',
        costCenter: '',
        dateFrom: '',
        dateTo: '',
        dayAmount: 0,
        addedValue: 0,
        advancePayment: 0,
        advancePaymentAmount: 0.00,
        reason: '',
        transport: {'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }
      }
    };
  },
  methods: {
    startLoading() {
      this.isLoading = true;
    },
    stopLoading() {
      this.isLoading = false;
    },
    openSelectedTravel(userFullName, selectedTravel) {
      this.resetForm();
      this.userFullName = userFullName;
      this.selectedTravel = selectedTravel;
      this.loadTravelInfo();
    },
    async loadTravelInfo() {
      this.startLoading(); 

      this.form = {
        userFullName: this.userFullName,
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
      this.stopLoading();
    },
    resetForm() {
      this.form = {
        userFullName: '',
        destination: '',
        address: '',
        costCenter: '',
        dateFrom: '',
        dateTo: '',
        dayAmount: 0,
        addedValue: 0,
        advancePayment: 0,
        advancePaymentAmount: 0.00,
        reason: '',
        transport: {'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }
      }
    },
    transformTransportStringtoMap(transportString) {
      let transportMap = {'Plane': false, 'Train': false, 'RentCar': false, 'BusinessCar': false, 'PrivateCar': false, 'Taxi': false }

      //if string is null, all transportOps remain false
      if(transportString){
        let transportOpsChosen = Array.from(transportString.split(";"))

        this.transportNamesOrder.forEach(transportOp =>{
          if (transportOpsChosen.includes(transportOp)) transportMap[transportOp] = true;
        });
      }
      return transportMap;
    },
  }
};
</script>

<style scoped>
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

.modal-blur {
  position: relative;
  filter: blur(4px);
  pointer-events: none;
  opacity: 0.5;
  z-index: 1;
}

/* Overlay con el spinner centrado */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  background: rgba(255, 255, 255, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #24006D;
  /* Color del spinner */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
