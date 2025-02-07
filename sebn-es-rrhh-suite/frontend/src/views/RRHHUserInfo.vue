<template>
  <main class="px-2 containerSearch flex-body">
    <h1 class="text-left mt-3 mb-2 fs-3 fw-bold col-6">User info</h1>
    <p class="mb-2">Select a user to inspect them</p>

    <!-- Top buttons and search bar -->
    <div class="row">
      <div class="d-flex">
        <!-- Search users -->
        <div id="searchContainer" class="col-md-6 pe-4 position-relative">
          <div class="input-group">
            <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
            <div class="flex-fill position-relative">
              <input type="search" class="form-control rounded-0" v-model="searchQuery" placeholder="Search user...">
            </div>
          </div>
        </div>

        <!-- Show filters -->
        <div class="dropdown position-relative">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="btn_filterTravels"
            data-bs-toggle="dropdown" aria-expanded="false">
            <span><i class="fa-solid fa-filter"></i></span> Filter
          </button>

          <div class="dropdown-menu dropdown-menu-end p-4 shadow" aria-labelledby="btn_filterTravels"
            style="min-width: 300px; position: absolute; top: 100%; right: 0; z-index: 1000;">
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
          <!-- create new user -->
          <button type="button" class="btn btn-primary bg-main mx-1" data-bs-target="#modalCreateNewUser"
            data-bs-toggle="modal">
            Create new user <i class="fa-solid fa-user-plus ms-2"></i>
          </button>
        </div>

        <!-- Download in Excel -->
        <!-- 
        <button type="button" class="btn btn-primary bg-main mx-1" @click="downloadExcel()" disabled>
          Download in Excel <i class="fa-solid fa-file-excel ms-2"></i>
        </button>-->
      </div>
    </div>

    <!-- LIST + USER INFO CONTENTS CONTAINER -->
    <div class="d-block">

      <!-- container USERS LIST + GO BACK -->
      <div class="d-flex">
        <!-- go back button (unselect user, return to list)-->
        <button id="btnBackUnselectUser" v-if="selectedUser"
          class="btn btn-secondary bg-main mr-3 rounded-circle my-4 px-3" @click="selectedUser = null; searchQuery = ''"
          style="width: fit-content; height: fit-content;" title="Return to list">
          <i class="fa-solid fa-arrow-left"></i>
        </button>

        <!-- USERS LIST -->
        <div class="gap-3 d-block col-md-6">
          <div style="max-height: 740px; overflow-y: auto;">
            <div v-for="(user, index) in filteredUsers" :key="index" class="card mt-3">
              <!-- Each card -->
              <div :id="'UserCard_' + user.Email" class="card-header titleHoliday mb-2 fs-5 d-flex"
                :title="user.FullName + ' (' + user.Email + ')'">
                <div id="btnUserCardSelect" style="flex-grow: 3" class="cursor-pointer"
                  @click="!selectedUser ? selectUser(user) : null">
                  <i class="fa-solid fa-user mr-3"></i>
                  {{ user.FullName }}, {{ user.Department }} ({{ user.City }})
                </div>

                <!-- Download report-->
                <button :id="'button' + user.Email" type="button" class="btn btn-primary bg-main mx-1 float-end"
                  @click="selectUser(user); downloadExcel()" title="Download report">
                  <a :download="'UserInfo_' + user.FullName + '_' + formatDate2Aux(new Date) + '.xlsx'">
                    Download report <i class="fa-solid fa-download ms-2"></i>
                  </a>
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- USER INFO CONTAINER-->
      <div class="row mt-4" v-if="selectedUser != null">

        <!-- LEFT HALF CONTAINER (WHILE USER IS SELECTED) -->
        <div class="col-7 overflow-hidden">

          <!-- CALENDAR + LEGEND-->
          <div id="calendarContainer">
            <!-- calendar  -->
            <div class="row-md-6">
              <div class="calendar-container">
                <!-- legend -->
                <div class="info-container">
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
                        <span class="legend-color mr-1 vacations-notSigned"></span> Created
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
                        <span class="legend-color mr-1 travels-notSigned"></span> Created
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
                <VCalendar expanded :attributes="attrs">
                  <template #day-popover="{ day, format, masks, attributes }">
                    <div class="small ho-user text-center text-capitalize">
                      {{ format(day.date, masks.dayPopover) }}
                    </div>
                    <div v-for="{ key, highlight, popover } in attributes" :key="key">
                      <div>
                        <span :class="{
                          'travelCreated': popover.label.toLowerCase().includes('signs 0/2'),
                          'travelInProgress': popover.label.toLowerCase().includes('signs 1/2'),
                          'travelSigned': popover.label.toLowerCase().includes('signs 2/2'),
                          'holidays': popover.label.toLowerCase().includes('CREATED'),
                          'holidays': popover.label.toLowerCase().includes('SIGNED'),
                          'holidays': popover.label.toLowerCase().includes('REJECTED'),
                          [popover.label.toLowerCase()]: !popover.label.toLowerCase().includes('signs')
                        }" class="mr-3"></span>
                        <span class="small">
                          {{
                            popover.label[0] + popover.label.substring(1).toLowerCase() === 'Holiday created'
                              ? 'Holiday requested'
                              : popover.label[0] + popover.label.substring(1).toLowerCase() === 'Holiday signed'
                                ? 'Holiday approved'
                          : popover.label[0] + popover.label.substring(1).toLowerCase()
                          }}
                        </span>
                      </div>
                    </div>
                  </template>
                </VCalendar>
              </div>
            </div>
          </div>

          <!-- user info cards -->
          <div class="row mt-4">
            <!-- HOLIDAYS INFO -->
            <div class="col-6">
              <div id="holidaysContainer" class="card scrollable-card mb-3 mt-0">
                <div class="card-header titleHoliday mb-2 fs-5 d-flex justify-content-between align-items-center"
                  @click="toggleCardVisibility('holidayCards', 'toggleHolidays')"
                  title="User's holidays for the current year">
                  <div>
                    <i class="fa-solid fa-umbrella-beach mr-3"></i> Holidays
                  </div>
                  <span>
                    <i id="toggleHolidays" class="fa-solid fa-angle-down"></i>
                  </span>
                </div>

                <!-- Aplicar el estilo scrollable-content solo a la parte desplazable -->
                <div id="holidayCards" class="card-body scrollable-content" style="display: none;">
                  <div v-for="vacation in userVacations
                    .filter(vacation => new Date(vacation.startingDay).getFullYear() === new Date().getFullYear())
                    .sort((a, b) => new Date(b.startingDay) - new Date(a.startingDay))" :key="vacation.id"
                    class="card mb-3">

                    <div class="card-body" :title="vacation.status">
                      <h6 class="card-subtitle mb-2 fs-5 titleHolidays">Holiday</h6>
                      <p class="card-text fs-6 fw-medium" v-if="!vacation.partialDay">
                        {{ formatDate(vacation.startingDay) }} - {{ formatDate(vacation.finishingDay) }}
                      </p>
                      <p class="card-text fs-6 fw-medium" v-if="vacation.partialDay">
                        {{ formatDate(vacation.startingDay) }} -
                        {{ Math.floor((vacation.totalQuantity / (this.hourConversionValue / 60)) / 60) }} Hrs.
                        {{ Math.floor((vacation.totalQuantity / (this.hourConversionValue / 60)) % 60) }} Min.
                      </p>
                    </div>

                    <div class="position-absolute top-0 end-0 translate-middle p-2 border rounded-circle"
                      :style="{ backgroundColor: this.color[vacation.status] }" :title="vacation.status">
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-6">
              <div id="travelsContainer" class="card scrollable-card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center titleHoliday mb-2 fs-5"
                  @click="toggleCardVisibility('travelCards', 'toggleTravels')"
                  title="User's travels for the current year">
                  <div>
                    <i class="fa-solid fa-plane mr-3"></i> Travels
                  </div>
                  <i id="toggleTravels" class="fa-solid fa-angle-down"></i>
                </div>

                <!-- Aplicar el estilo scrollable-content solo a la parte desplazable -->
                <div id="travelCards" class="card-body scrollable-content" style="display: none;">
                  <div v-for="travel in userTravels
                    .filter(travel => new Date(travel.dateFrom).getFullYear() === new Date().getFullYear())
                    .sort((a, b) => new Date(b.dateFrom) - new Date(a.dateFrom))" :key="travel.id"
                    class="card mb-3 cursor-pointer" @click="showTravelDetailsModal(travel)"
                    data-bs-target="#modalTravelDetails" data-bs-toggle="modal">

                    <div class="card-body" title="Open travel details">
                      <h6 class="card-subtitle mb-2 fs-5 titleHolidays">{{ travel.reason }}</h6>
                      <p class="card-text fs-6 fw-medium">
                        <i class="fa-solid fa-plane w-7"></i> {{ travel.destination }}
                      </p>
                      <p class="card-text fs-6 fw-medium">
                        <i class="fa-solid fa-calendar w-7"></i>
                        {{ formatDate(travel.dateFrom) }} - {{ formatDate(travel.dateTo) }}
                      </p>
                    </div>

                    <div class="position-absolute top-0 end-0 translate-middle p-0.5 border rounded"
                      :style="{ backgroundColor: this.color[travel.status] }"
                      style="color: white; font-weight: 500; width:25%; text-align: center; font-size: small"
                      :title="travel.status">
                      Num. {{ travel.id }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- RIGHT HALF CONTAINER: USER DETAILS FORM -->
        <div id="userDetailsContainer" class="col-5 px-5 py-4 border rounded mb-4">
          <div id="detailsTopButtonsContainer">
            <button id="btnEdit" class="btn btn-primary bg-main" @click=" toggleEditUserDetails(true)"
              v-show="!isEditing" title="Edit user">
              <i class="fa-solid fa-pencil me-2"></i> Edit
            </button>

            <button type="submit" v-show="isEditing" id="btnSaveChanges" class="btn btn-primary bg-main"
              @click.prevent="validateUserDetails()" title="Save changes">
              <i class="fa-solid fa-check me-2"></i> Save
            </button>

            <button id="btnCancelEditDetails" v-show="isEditing" class="btn btn-secondary bg-main mx-2"
              @click="toggleEditUserDetails(false)">
              <i class="fa-solid fa-x me-2"></i> Cancel
            </button>

            <button id="btnDelete" class="btn btn-secondary float-end" data-bs-target="#modalDeleteUser"
              data-bs-toggle="modal" title="Delete user">
              <i class="fa-solid fa-trash me-2"></i>
              Delete
            </button>
          </div>

          <h1 class="mb-4 fs-5 fw-bold content-between text-center w-100">User details</h1>
          <form :id="userDetailsForm">
            <!-- full name-->
            <div class="mb-3 row">
              <label for="userDetailsFullName" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Full name
              </label>
              <input type="text" class="form-control formEditableField" id="userDetailsFullName"
                v-model="userDetailsForm.userFullName" disabled />
            </div>

            <!-- email -->
            <div class="mb-3 row">
              <label for="userDetailsEmail" class="form-label">Email</label>
              <input type="text" class="form-control" id="userDetailsEmail" v-model="userDetailsForm.email" readonly
                disabled />
            </div>

            <!-- city -->
            <div class="mb-3 row">
              <label for="userDetailsCity" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>City
              </label>
              <select class="form-control formEditableField" id="userDetailsCity" v-model="userDetailsForm.city"
                disabled>
                <option v-for="city in cities">{{ city }}</option>
              </select>
            </div>

            <!-- position -->
            <div class="mb-3 row">
              <label for="userDetailsPosition" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Position
              </label>
              <select class="form-control formEditableField" id="userDetailsPosition" v-model="userDetailsForm.position"
                disabled>
                <option v-for="position in positions">
                  {{ position }}
                </option>
              </select>
            </div>

            <!-- department -->
            <div class="mb-3 row">
              <label for="userDetailsDepartment" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Department
              </label>
              <select class="form-control formEditableField" id="userDetailsDepartment"
                v-model="userDetailsForm.department" disabled>
                <option v-for="department in departments" :value="department.name">
                  {{ department.name }}
                </option>
              </select>
            </div>

            <!-- subDepartment -->
            <div class="mb-3 row">
              <label for="userDetailsSubDepartment" class="form-label">Subdepartment</label>
              <select class="form-control formEditableField" id="userDetailsSubDepartment"
                v-model="userDetailsForm.subDepartment" disabled>
                <option :value="null">None</option>
                <option v-for="subDepartment in subDepartments" :value="subDepartment.SubDepartment">
                  {{ subDepartment.SubDepartment }}
                </option>
              </select>
            </div>

            <!-- costCenter -->
            <div class="mb-3 row">
              <label for="userDetailsCostCenter" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Cost center
              </label>
              <input type="number" class="form-control formEditableField" id="userDetailsCostCenter"
                v-model="userDetailsForm.costCenter" min="0" step="1" disabled placeholder="None" />
            </div>

            <!-- workingHours -->
            <div class="mb-3 row">
              <label for="userDetailsWorkingHours" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Working hours
              </label>
              <input type="number" class="form-control formEditableField" id="userDetailsWorkingHours"
                v-model="userDetailsForm.workingHours" min="1" step="1" max="8" required disabled />
            </div>

            <!-- techResponsible -->
            <div class="mb-3 row">
              <label for="userDetailsTechResponsible" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Tech responsible
              </label>
              <select class="form-control formEditableField" id="userDetailsTechResponsible"
                v-model="userDetailsForm.techResponsible" disabled>
                <option v-for="user in users" :value="user.Email">
                  {{ user.FullName }}
                </option>
              </select>
            </div>

            <!-- travelResponsible -->
            <div class="mb-3 row">
              <label for="userDetailsTravelResponsible" class="form-label">
                <span v-show="isEditing" style="color: red">* </span>Travel responsible
              </label>
              <select class="form-control formEditableField" id="userDetailsTravelResponsible"
                v-model="userDetailsForm.travelResponsible" disabled>
                <option v-for="user in users" :value="user.Email">
                  {{ user.FullName }}
                </option>
              </select>
            </div>

            <!-- Buckets user days -->
            <div id="userBucketsContainer" class="mb-3 row border py-2">
              <h1 class="mb-2">Vacation days available:</h1>
              <div class="row d-flex my-1 mx-2" v-for="bucket in userBuckets">
                <label :id="'bucketName_' + bucket.bucketName" :for="'bucketValue_' + bucket.bucketValue"
                  class="col-6">{{
                    bucket.BucketName }}</label>

                <input type="text" class="col-6" :id="'bucketValue_' + bucket.bucketValue" readonly disabled
                  :value="bucket.BucketValue" />
              </div>
            </div>

            <!-- Reset password -->
            <div class="mb-2 row">
              <label for="btnResetUserPassword" class="form-label">Have they forgotten their password?</label>
              <button id="btnResetUserPassword" type="button" class="btn btn-secondary" @click="resetUserPassword()">
                Reset password
              </button>
            </div>

          </form>
        </div>

      </div>

    </div>

    <!-- MODALS: -->

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

    <!-- modal confirm delete user -->
    <div class="modal fade" id="modalDeleteUser" tabindex="-1" role="dialog"
      aria-labelledby="modalDeleteUserCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modalDeleteUserLongTitle">Delete user</h5>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this user?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="deleteUser()">
              Accept
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal create new user -->
    <div class="modal fade" id="modalCreateNewUser" tabindex="-1" role="dialog"
      aria-labelledby="modalCreateNewUserCenterTitle" aria-hidden="true">
      <div id="createUserModal" class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modalTravelDetailsLongTitle">Create user</h5>
          </div>

          <div class="modal-body">
            <form :id="createUserForm" @submit.prevent="validateNewUser()">

              <div class="modal-body">
                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserFullName" class="form-label">Full Name:</label>
                  <input type="text" class="form-control" id="createUserFullName" required
                    v-model="createUserForm.fullName" placeholder="First and last name...">
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserEmail" class="form-label">Email:</label>
                  <input type="text" class="form-control" id="createUserEmail" required v-model="createUserForm.email"
                    placeholder="example.example@sebn.com">
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserCity" class="form-label">City:</label>
                  <select class="form-select" id="createUserCity" @change="calcNewUserHolidays()"
                    v-model="createUserForm.city" required>
                    <option :value="null" selected disabled hidden>Select a city...</option>
                    <option v-for="city in cities">{{ city }}</option>
                  </select>
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserDepartment" class="form-label">Department:</label>
                  <select class="form-select" id="createUserDepartment" v-model="createUserForm.department" required>
                    <option :value="null" selected disabled hidden>Select a department...</option>
                    <option v-for="department in departments" :value="department.name">
                      {{ department.name }}
                    </option>
                  </select>

                </div>

                <div class="mb-3">
                  <label for="createUserSubDepartment" class="form-label">Subdepartment:</label>
                  <select class="form-select" id="createUserSubDepartment" v-model="createUserForm.subDepartment"
                    required>
                    <option :value="null">None</option>
                    <option v-for="subDepartment in subDepartments" :value="subDepartment.SubDepartment">
                      {{ subDepartment.SubDepartment }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="createUserCostCenter" class="form-label">Cost center:</label>
                  <input type="number" class="form-control formEditableField" id="createUserCostCenter"
                    v-model="createUserForm.costCenter" placeholder="Cost center id..." min="0" step="1" />
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserWorkingHours" class="form-label">Working Hours:</label>
                  <input type="number" class="form-control formEditableField" id="createUserWorkingHours"
                    v-model="createUserForm.workingHours" placeholder="Hours/day..." min="1" step="1" max="8"
                    required />
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserPosition" class="form-label">Position:</label>
                  <select class="form-select" id="createUserPosition" v-model="createUserForm.position" required>
                    <option :value="null" selected disabled hidden>Select a position...</option>
                    <option v-for="position in positions">
                      {{ position }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserTechResponsible" class="form-label">Tech responsible:</label>
                  <select class="form-select" id="createUserTechResponsible" v-model="createUserForm.techResponsible"
                    required>
                    <option :value="null" selected disabled hidden>Select a tech responsible...</option>
                    <option v-for="user in users" :value="user.Email">
                      {{ user.FullName }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserTravelResponsible" class="form-label">Travel Responsible:</label>
                  <select class="form-select" id="createUserTravelResponsible"
                    v-model="createUserForm.travelResponsible" required>
                    <option :value="null" selected disabled hidden>Select a travel responsible...</option>
                    <option v-for="user in users" :value="user.Email">
                      {{ user.FullName }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <span style="color: red">* </span>
                  <label for="createUserUpperManagement" class="form-label">Gerency Responsible:</label>
                  <select id="createUserUpperManagement" class="form-select" v-model="createUserForm.upperManagement"
                    required>
                    <option :value="null" selected disabled hidden>Select a manager...</option>
                    <option v-for="manager in managers" :value="manager">
                      {{ manager }}
                    </option>
                  </select>
                </div>

                <div class="mb-3 row">
                  <div class="col-md-6">
                    <span style="color: red">* </span>
                    <label class="form-label" for="createUserStartWorking">Starts Working:</label>
                    <input id="createUserStartWorking" class="form-control" type="date" @change="calcNewUserHolidays()"
                      required v-model="createUserForm.startWorking">
                  </div>

                  <div class="col-md-6 d-flex flex-column">
                    <label class="form-label" for="createUserVacationsCalc">Total vacation days:</label>
                    <input type="text" class="form-control" id="createUserVacationsCalc" placeholder="Total Days"
                      readonly v-model="createUserForm.totalVacationDays" required>
                  </div>
                </div>
              </div>

              <div class="modal-footer">
                <button id="btnCloseModalCreateUser" type="button" class="btn btn-secondary" data-bs-dismiss="modal"
                  @click="resetCreateUserForm()">
                  Cancel
                </button>

                <button type="submit" class="btn btn-primary">
                  Accept
                </button>
              </div>
            </form>
          </div>

        </div>
      </div>
    </div>

  </main>
</template>

<script>
import { formatDate, formatDate2, notifyError, notifySuccess, loadingMessage, stopLoadingMessage } from '@/assets/globalFunctions';
import ModalTravelDetails from '@/components/ModalTravelDetails.vue';
import { ref, computed, useSSRContext } from 'vue';
import { BACKEND_HOST } from '../config';

export default {
  components: {
    ModalTravelDetails
  },
  data() {
    return {
      users: [],
      color: { 'CREATED': "#e7ad41", 'SIGNED': "#7ab870", 'REJECTED': "#c75353" },

      selectedDepartmentFilter: 'all',
      searchQuery: '',
      userReport: null,
      attrs: [],

      selectedUser: null,
      userFullName: "",
      selectedTravel: null, //if a travel is selected WHILE user is selected
      userFestivities: [],
      userTravels: [],
      userVacations: [],
      userHomeOffice: [],
      userBuckets: [],
      userDetails: [],
      hourConversionValue: 0,

      isEditing: false,
      userDetailsForm: {
        userFullName: '',
        email: '',
        city: '',
        position: '',
        department: '',
        subDepartment: '',
        costCenter: '',
        workingHours: '',
        techResponsible: '',
        travelResponsible: ''
      },

      formIsValid: true, //flag used to validate both forms, create and details (they're validated separately obviously)

      cities: ['PAM', 'CUE', 'MAR'],
      positions: ['Internship', 'Employee', 'Manager'],
      managers: [],
      departments: [],
      subDepartments: [],
      cityVacationDays: null,

      createUserForm: {
        fullName: null,
        email: null,
        city: null,
        position: null,
        department: null,
        subDepartment: null,
        costCenter: null,
        workingHours: null,
        techResponsible: null,
        travelResponsible: null,
        upperManagement: null,
        startWorking: '',
        totalVacationDays: null
      }
    }
  },
  created() {
    this.reload();
  },
  watch: {
    searchQuery(newQuery) {
      if (newQuery !== this.selectedUser?.FullName) {
        this.selectedUser = null;
      }
    },
    /* Disable user card click WHILE a user is selected (to prevent reload) */
    selectedUser(newSelectedUser) {
      const btnUserOpenDetails = document.getElementById("btnUserCardSelect")
      if (newSelectedUser) {
        btnUserOpenDetails.classList.remove("cursor-pointer");
      } else {
        this.userTravels = [];
        this.userVacations = [];
        this.userHomeOffice = [];
        this.userBuckets = [];
        this.userDetails = [];
        this.userReport = null;
        btnUserOpenDetails.classList.add("cursor-pointer")
      }
    }
  },
  computed: {
    filteredUsers() {
      let filtered = this.users;
      filtered = this.users.filter(user =>
        (user.FullName && user.FullName.toLowerCase().includes(this.searchQuery.toLowerCase()))
        ||
        (user.Email && user.Email.toLowerCase().includes(this.searchQuery.toLowerCase()))
      );

      //To apply selected filters
      if (this.selectedDepartmentFilter != 'all') {
        filtered = this.users.filter(user =>
          user.Department == this.selectedDepartmentFilter
        );
      }
      return filtered;
    }
  },
  methods: {
    async reload() {
      loadingMessage();
      await this.fetchUsers();
      if (this.departments.length == 0) this.fetchDepartments();
      if (this.subDepartments.length == 0) this.fetchSubDepartments();
      if (this.managers.length == 0) this.fetchManagers();
      if (!this.cityVacationDays) this.fetchCityVacationDays()
      stopLoadingMessage();
    },
    toggleLegend() {
      const legend = document.querySelector('.legend-container');
      legend.classList.toggle('show');
    },
    showError(error) {
      notifyError(error.state || error.message)
      console.error(error.state || error.message)
      stopLoadingMessage()
    },
    formatDate(date) {
      return formatDate(date);
    },

    formatDate2Aux(date) {
      return formatDate2(date);
    },
    resetFilters() {
      this.selectedDepartmentFilter = 'all';
    },


    /* COMMON FORM-RELATED METHODS */
    formValidationError(elementId, message) {
      this.formIsValid = false;
      if (elementId) document.getElementById(elementId).classList.add("hasError")
      let error = new Error(message)
      notifyError(error.message);
      console.error(error.message)
    },
    cleanFormValidationErrorFields() {
      const elements = document.querySelectorAll('.hasError');
      elements.forEach(element => {
        element.classList.remove('hasError');
      });
      this.formIsValid = true;
    },


    /* METHODS WHEN A USER HAS BEEN SELECTED */
    async selectUser(user) {
      if (!this.selectedUser) {
        loadingMessage();
        this.searchQuery = user.FullName;
        this.selectedUser = user;

        this.isEditing = false;
        this.resetUserDetailsForm();
        this.attrs.length = 0; //to empty Proxy(Array)
        this.userTravels = [];
        this.userVacations = [];
        this.userHomeOffice = [];

        await this.fetchUserDetails(user.Email);
        await this.loadFormPlaceholders();
        await this.printCalendar();
        stopLoadingMessage();
      }
    },
    /*Hide or expand the travels/vacations cards list*/
    toggleCardVisibility(cardContainer_id, icon_id) {
      let card = document.getElementById(cardContainer_id)
      let icon = document.getElementById(icon_id)

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
    showTravelDetailsModal(selectedTravel) {
      this.selectedTravel = selectedTravel
      this.userFullName = this.selectedUser.FullName

      this.$nextTick(() => {
        this.$refs.travelDetails.openSelectedTravel(this.userFullName, this.selectedTravel)
      });
    },
    resetUserDetailsForm() {
      this.userDetailsForm = {
        userFullName: '',
        email: '',
        city: '',
        position: '',
        costCenter: '',
        workingHours: '',
        department: '',
        subDepartment: '',
        techResponsible: '',
        travelResponsible: ''
      };
    },
    loadFormPlaceholders() {
      this.userDetailsForm = {
        userFullName: this.selectedUser.FullName,
        email: this.selectedUser.Email,
        city: this.selectedUser.City,
        position: this.selectedUser.Position,
        department: this.selectedUser.Department,
        subDepartment: this.selectedUser.SubDepartment,
        costCenter: this.selectedUser.CostCenter,
        workingHours: this.selectedUser.WorkingHours,
        techResponsible: this.selectedUser.TechResponsible,
        travelResponsible: this.selectedUser.TravelResponsible,
      };
      this.fetchUserDaysBuckets();
    },
    toggleEditUserDetails(isEditing) {
      this.isEditing = isEditing;
      let formEditableFields = document.querySelectorAll('.formEditableField');
      formEditableFields.forEach(element => {
        element.disabled = !this.isEditing;
      });
      this.cleanFormValidationErrorFields();
      if(!isEditing) this.loadFormPlaceholders();
    },
    async printCalendar() {
      if (this.selectedUser) {
        await Promise.all([this.fetchUserVacations(this.selectedUser.Email), this.fetchUserHomeOffice(this.selectedUser.Email), this.fetchUserTravels(this.selectedUser.Email), this.fetchUserFestivities(this.selectedUser.Email)]);

        this.attrs.splice(0);

        //print weekends
        const weekends = ref([
          {
            description: 'weekend',
            isComplete: false,
            dates: { repeat: { weekdays: [1, 7] } }, // Every saturday and sunday
          },
        ]);
        this.attrs = computed(() => [
          ...weekends.value.map(day => ({
            dates: day.dates,
            content: {
              class: "lightGray" //custom css class for color
            }
          })),
        ]);

        //print travels
        if (this.userTravels.length > 0) {
          this.userTravels.forEach(day => {
            const startDate = new Date(day.dateFrom);
            const endDate = new Date(day.dateTo);
            let highlightValue = "purpleAux"
            let signCount = " (signs 2/2)"
            let classColor = "white";

            if (day.status != 'DELETED' && day.status != 'REJECTED') {
              if (day.status == "CREATED") {
                if (day.managementSignature != null || day.responsibleSignature != null) {
                  highlightValue = "lightPurple";
                  signCount = " (signs 1/2)";
                } else {
                  highlightValue = "lighterPurple"
                  signCount = " (signs 0/2)";
                  classColor = "lighterPurple";
                }
              }
              this.attrs.push({
                highlight: { class: highlightValue },
                content: { class: classColor },
                popover: {
                  label: day.id + ": " + day.reason + signCount,
                  visibility: 'hover'
                },
                dates: [[startDate, endDate]]
              })
            }
          });
        }


        //print vacations
        if (this.userVacations.length > 0) {
          this.userVacations.forEach(day => {
            const startDate = new Date(day.startingDay);
            const endDate = new Date(day.finishingDay);
            let highlightValue = "yellow";

            if (day.status != 'DELETED' && day.status != 'REJECTED') {
              if (day.status == "CREATED") highlightValue = "yellow";
              this.attrs.push({
                highlight: { class: highlightValue },
                content: { class: 'white' },
                popover: {
                  label: "Holiday " + day.status
                },
                dates: [[startDate, endDate]],
              })
            }
          });
        }

        //print home office
        if (this.userHomeOffice.length > 0) {
          this.userHomeOffice.forEach((day => {
            let highlightValue = {};
            switch (day.Type) {
              case "OFFICE": highlightValue = "pink"
                break;
              case "FULL": highlightValue = "blue"
                break;
              case "PARTIAL": highlightValue = "lightBlue"
                break;
            };
            this.attrs.push({
              highlight: { class: highlightValue },
              content: { class: 'white' },
              popover: {
                label: day.Type,
              },
              dates: day.Date,
            })
          }));
        }

        //print festivities
        if (this.userFestivities.length > 0) {
          this.userFestivities.forEach((day => {
            this.attrs.push({
              content: {class: "green"},
              popover: {
                label: "Festivity (" + String(this.selectedUser.City).toUpperCase() + ")",
              },
              dates: day.Date,
            })
          }));
        }
      }
    },
    validateUserDetails() {
      this.cleanFormValidationErrorFields();

      try {
        //Required fields validations
        if (!this.userDetailsForm.userFullName || this.userDetailsForm.userFullName.trim() == '') this.formValidationError('userDetailsFullName', 'Full Name field must not be empty')
        if (!this.userDetailsForm.workingHours) this.formValidationError('userDetailsWorkingHours', 'Working hours field must not be empty')

        //Other validations
        if (this.userDetailsForm.userFullName.split(" ").length < 2) this.formValidationError('userDetailsFullName', 'Full Name needs to be at least two words (first and last name)')
        if (this.userDetailsForm.workingHours < 1 || this.userDetailsForm.workingHours > 8) this.formValidationError('userDetailsWorkingHours', 'Working hours must be a number between 1 and 8, both included')
        if (this.userDetailsForm.position == "Manager") this.formValidationError('userDetailsPosition', 'Position can not be upgraded to Manager. Contact us to handle the situation.')

        //if everything alright, we create the new user
        if (this.formIsValid) this.updateUserDetails()
      } catch (error) {
        console.error(error);
      }
    },
    async updateUserDetails() {
      let data = {
        'email': this.selectedUser.Email,
        'fullName': this.userDetailsForm.userFullName,
        'city': this.userDetailsForm.city,
        'position': this.userDetailsForm.position,
        'department': this.userDetailsForm.department,
        'subDepartment': this.userDetailsForm.subDepartment,
        'costCenter': this.userDetailsForm.costCenter,
        'workingHours': this.userDetailsForm.workingHours,
        'techResponsible': this.userDetailsForm.techResponsible,
        'travelResponsible': this.userDetailsForm.travelResponsible
      }

      try {
        const response = await fetch(`${BACKEND_HOST}user/update-user-details`, {
          method: 'PUT',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Failed to update the user: " + (error.message || error.state));
        }

        notifySuccess("User updated succesfully!")
        this.toggleEditUserDetails(false)
      } catch (error) {
        this.showError(error);
      }
    },
    async resetUserPassword() {
      let data = { 'userEmail': this.selectedUser.Email }
      try {
        const response = await fetch(`${BACKEND_HOST}access/reset-user-password`, {
          method: 'PUT',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || error.state);
        }

        notifySuccess("User's password has been reset successfully!");
      } catch (error) {
        this.showError(error)
      }
    },
    async deleteUser() {
      let data = {
        'email': this.selectedUser.Email
      }

      try {
        const response = await fetch(`${BACKEND_HOST}user/delete-user`, {
          method: 'PUT',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Failed to delete the user: " + (error.message || error.state));
        }

        notifySuccess("User deleted succesfully!")
        this.selectedUser = null
        this.searchQuery = ''

      } catch (error) {
        this.showError(error);
      }
    },


    /* METHODS FOR ADDING A NEW USER */
    resetCreateUserForm() {
      this.createUserForm = {
        fullName: null,
        email: null,
        city: null,
        position: null,
        costCenter: null,
        workingHours: null,
        department: null,
        subDepartment: null,
        techResponsible: null,
        travelResponsible: null,
        upperManagement: null,
        startWorking: null,
        totalVacationDays: null
      };
      this.cleanFormValidationErrorFields();
    },
    calcNewUserHolidays() {
      if (this.createUserForm.startWorking && this.createUserForm.city) {
        const selectedDate = new Date(this.createUserForm.startWorking);
        const city = this.createUserForm.city;

        const cityDays = this.cityVacationDays;

        const value = cityDays[city];
        const today = new Date();
        const endOfYear = new Date(today.getFullYear(), 11, 31);
        const oneDay = 24 * 60 * 60 * 1000; // milisegundos en un día
        const daysLeft = Math.round((endOfYear - selectedDate) / oneDay);

        const result = (daysLeft * value) / 365;
        this.createUserForm.totalVacationDays = result.toFixed(2);
      }
    },
    validateNewUser() {
      this.cleanFormValidationErrorFields();

      try {
        //Required fields validations
        if (!this.createUserForm.fullName || this.createUserForm.fullName.trim() == '') this.formValidationError('createUserFullName', 'Full name field must not be empty')
        if (!this.createUserForm.email || this.createUserForm.email.trim() == '') this.formValidationError('createUserEmail', 'Email field must not be empty')
        if (!this.createUserForm.city) this.formValidationError('createUserCity', 'City field must not be empty')
        if (!this.createUserForm.position) this.formValidationError('createUserPosition', 'Position field must not be empty')
        if (!this.createUserForm.department) this.formValidationError('createUserDepartment', 'Department field must not be empty')
        if (!this.createUserForm.techResponsible) this.formValidationError('createUserTechResponsible', 'Tech reponsible field must not be empty')
        if (!this.createUserForm.travelResponsible) this.formValidationError('createUserTravelResponsible', 'Travel responsible field must not be empty')
        if (!this.createUserForm.upperManagement) this.formValidationError('createUserUpperManagement', 'Gerency field must not be empty')
        if (!this.createUserForm.workingHours) this.formValidationError('createUserWorkingHours', 'Working hours field must not be empty')
        if (!this.createUserForm.startWorking || this.createUserForm.startWorking == '') this.formValidationError('createUserStartWorking', 'Starts working field must not be empty')

        //Other validations
        if (this.createUserForm.fullName.split(" ").length < 2) this.formValidationError('createUserFullName', 'Full name needs to be at least two words (first and last name)')
        if (!this.createUserForm.email.endsWith('@sebn.com')) this.formValidationError('createUserEmail', 'Email needs to have a valid format')

        //if everything alright, we create the new user
        if (this.formIsValid) this.createNewUser()
      } catch (error) {
        console.error(error);
      }
    },
    async createNewUser() {
      const fullname = this.createUserForm.fullName;
      const email = this.createUserForm.email;
      const department = this.createUserForm.department;
      const subDepartment = this.createUserForm.subDepartment;
      const costCenter = this.createUserForm.costCenter;
      const workingHours = this.createUserForm.workingHours;
      const position = this.createUserForm.position;
      const techResponsible = this.createUserForm.techResponsible;
      const travelResponsible = this.createUserForm.travelResponsible;
      const city = this.createUserForm.city;
      const gerency = this.createUserForm.upperManagement;
      const startDate = this.createUserForm.startWorking;

      const data = {
        fullname: fullname,
        email: email,
        department: department,
        subDepartment: subDepartment,
        costCenter: costCenter,
        workingHours: workingHours,
        position: position,
        techResponsible: techResponsible,
        travelResponsible: travelResponsible,
        city: city,
        gerency: gerency,
        startDate: startDate
      };

      try {
        const response = await fetch(`${BACKEND_HOST}hr/create-user`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || error.state);
        }

        notifySuccess('User created successfully!');

        //TODO: encontrar una forma de verdad de cerrar el modal tras crear el user
        const modal = new bootstrap.Modal(document.getElementById("modalCreateNewUser"));
        modal.hide(); //esto no me hace dismiss :c
        document.getElementById("btnCloseModalCreateUser").click //esto es una chamada 

        this.resetCreateUserForm();
        this.fetchUsers();
      } catch (error) {
        this.showError(error)
      }
    },



    /* CREATE SINGLE USER REPORT */
    async downloadExcel() {
      loadingMessage();
      let userEmail = this.selectedUser.Email

      //Get all the information about the user (UNFILTERED)
      let userInfo = {};
      if (this.userDetails.length == 0) await this.fetchUserDetails(userEmail);
      userInfo.userDetails = this.userDetails;
      if (this.userBuckets.length == 0) await this.fetchUserDaysBuckets(userEmail);
      userInfo.userBuckets = this.userBuckets;
      if (this.userHomeOffice.length == 0) await this.fetchUserHomeOffice(userEmail);
      userInfo.userHomeOffice = this.userHomeOffice;
      if (this.userVacations.length == 0) await this.fetchUserVacations(userEmail);
      userInfo.userVacations = this.userVacations;
      if (this.userTravels.length == 0) await this.fetchUserTravels(userEmail);
      userInfo.userTravels = this.userTravels;

      await this.createReport(userInfo)
      stopLoadingMessage();
    },
    async createReport(userInfo) {
      const data = {
        userData: userInfo
      };

      try {
        const response = await fetch(`${BACKEND_HOST}user/get-user-info-report`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error("Failted to generate report: " + (error.message || error.state));
        }

        notifySuccess("Report created successfully!")
        const blob = await response.blob();
        const url = window.URL.createObjectURL(new Blob([blob]));
        this.userReport = url;
        await this.createAndRemoveLink(userInfo);
      } catch (error) {
        this.showError(error)
      }
    },
    async createAndRemoveLink(userInfo) {
      const a = document.createElement('a');
      a.href = this.userReport;
      a.download = 'UserInfo_' + userInfo.userDetails.FullName + '_' + this.formatDate2Aux(new Date()) + '.xlsx';
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
      }, 1000);
    },


    /* FETCH METHODS */
    async fetchUsers() { //SIMPLE LIST
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-all-users-simple-list`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Users were unable to load: ' + (error.message || error.state));
        }

        const data = await response.json();
        this.users = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserDetails(selectedUserEmail) {
      let pData = {
        'email': this.selectedUser.Email || selectedUserEmail
      }
      try {
        const response = await fetch(`${BACKEND_HOST}user/get-user-details`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || error.state);
        }

        const data = await response.json();
        this.selectedUser = data;
        this.userDetails = this.selectedUser;
        this.hourConversionValue = (1 / this.userDetails.WorkingHours).toFixed(3)
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserVacations(selectedUserEmail) {
      let pData = {
        'email': selectedUserEmail
      }

      try {
        const response = await fetch(`${BACKEND_HOST}user/get-user-holidays`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message);
        }

        const data = await response.json();
        this.userVacations = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserHomeOffice(selectedUserEmail) {
      let pData = {
        'email': selectedUserEmail
      }

      try {
        const response = await fetch(`${BACKEND_HOST}home-office/get-user-home-office`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || error.state);
        }

        const data = await response.json();
        this.userHomeOffice = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserTravels(selectedUserEmail) {
      let pData = {
        'user_email': selectedUserEmail
      }

      try {
        const response = await fetch(`${BACKEND_HOST}travel/get-user-travels`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || error.state);
        }

        const data = await response.json();
        this.userTravels = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserFestivities(selectedUserEmail) {
      try {
        const bodyData = {Email: selectedUserEmail};

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
          throw new Error(errorData.message || error.state);
        }

        const data = await response.json();
        this.userFestivities = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchDepartments() {
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-departments`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Departments could not be loaded' + (error.message || error.state));
        }

        const data = await response.json();
        this.departments = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchSubDepartments() {
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-sub-departments`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Subdepartments could not be loaded' + (error.message || error.state));
        }

        const data = await response.json();
        this.subDepartments = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchManagers() {
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-all-managers`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Managers could not be loaded' + (error.message || error.state));
        }

        const data = await response.json();
        this.managers = data.Managers;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchUserDaysBuckets(selectedUserEmail) {
      let pData = {
        'email': this.selectedUser.Email || selectedUserEmail
      }
      try {
        const response = await fetch(`${BACKEND_HOST}hr/get-user-days-buckets`, {
          method: 'POST',
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pData)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('User buckets could not be loaded' + (error.message || error.state));
        }

        const data = await response.json();
        this.userBuckets = data;
      } catch (error) {
        this.showError(error);
      }
    },
    async fetchCityVacationDays() {
      try {
        const response = await fetch(`${BACKEND_HOST}holiday/get-city-vacation-days-cur-year`, {
          headers: {
            'Authorization': localStorage.getItem('Authorization'),
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error('Unable to load city vacation days: ' + (error.message || error.state));
        }
        const data = await response.json();
        this.cityVacationDays = data
      } catch (error) {
        this.showError(error);
      }
    },
  }
}
</script>

<style>
#travelDetailsModal {
  max-width: 1000px;
}

#createUserModal {
  max-width: 700px;
}

.full,
.partial,
.officeHome,
.holidays,
.festivity,
.travelSigned,
.travelCreated,
.travelInProgress,
.office,
.created,
.signed,
.rejected {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-bottom: 0.5px;
  border-radius: 5px;
  margin-right: 5px;
}

:root {
  --partial: #06B4E9;
  --full: #0075C2;
  --office: #0B318F;
  --holidays: #ca8a04;
  --travel: #9333ea;
  --festivity: #45B035;
  --travelInProcess: #c999f4;
  --travelCreated: #9333ea;
  --created: #e7ad41;
  --signed: #7ab870;
  --rejected: #c75353;
}

.purpleAux,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travelInProgress {
  background-color: var(--travel) !important;
}

.lightPurple,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-lightBlue,
.travelInProgress {
  background: var(--travelInProcess) !important;
}


.lighterPurple,
.travelCreated {
  background: transparent !important;
  border: 2px solid var(--travelCreated) !important;
  color: #9333ea !important;
}

.blue,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-blue,
.full {
  background-color: #0075C2 !important;
}

.created {
  background-color: var(--created);
}

.signed {
  background-color: var(--signed);
}

.rejected {
  background-color: var(--rejected);
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
  color: white;
  font-weight: bold;
}

.yellow,
.vc-highlight-bg-solid.vc-day-popover-row-highlight.vc-attr.vc-green,
.holidays {
  background-color: var(--holidays) !important;
}

.lightGray {
  color: #a1a1a1 !important;
}

.form-check-input:checked {
  background-color: #501eb6;
  border-color: #4c2a85;
  opacity: 100%;
}

.form-control:disabled {
  background-color: rgb(223, 223, 223)
    /* var(--bs-primary-bg); */
}

.form-check-input:disabled~.form-check-label,
.form-check-input[disabled]~.form-check-label {
  opacity: 100%;
}

.form-control {
  border: solid lightgray 0.15rem;
}

.hasError {
  border: solid #b61e1e 0.15rem;
  border-color: #b61e1e;
  background-color: #b61e1e28;
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

.vc-light.vc-attr,
.vc-light .vc-attr {
  --vc-content-color: white;
  --vc-highlight-light-content-color: white;
}

.scrollable-content {
  max-height: 700px;
  overflow-y: auto;
}

.card-header {
  background-color: #f8f9fa;
  /* Color de fondo para los encabezados */
  cursor: pointer;
}

.card-body {
  padding: 10px;
}

.scrollable-card {
  margin-bottom: 20px;
}
</style>