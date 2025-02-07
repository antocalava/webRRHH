<template>
  <header class="header d-flex justify-content-between align-items-center" id="header">
    <div class="header_toggle">
      <i class='bx bx-menu' id="header-toggle"></i>
    </div>

    <strong class="position-absolute start-50 translate-middle-x">{{ getUsername() }}</strong>

    <div class="d-flex align-items-center">
      <a href="#" class="me-3" style="font-weight: bold; color: #3A3B76; text-decoration: underline;"
        data-bs-toggle="modal" data-bs-target="#feedbackModal">
        Send us feedback!
      </a>

      <!-- Modal -->
      <div class="modal fade" id="feedbackModal" tabindex="-1" aria-labelledby="feedbackModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="feedbackModalLabel">Feedback</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <!-- Formulario de feedback -->
              <form id="feedbackForm">
                <!-- Select para elegir el motivo -->
                <div class="mb-3">
                  <label for="contactReason" class="form-label required">Why do you seek to contact us?</label>
                  <select class="form-select" v-model="feedbackTag" id="contactReason" required>
                    <option value="BUG">Inform of a problem</option>
                    <option value="MOD">Suggest stylistic and usability changes</option>
                    <option value="ADD">Request a new feature</option>
                    <option value="INF">Send us a review</option>
                    <option value="QNA">Ask a question</option>
                  </select>
                </div>

                <!-- Input para resumir las ideas -->
                <div class="mb-3">
                  <label for="summaryInput" class="form-label required">Summarize your ideas</label>
                  <input type="text" class="form-control" id="summaryInput" placeholder="Subject..." maxlength="300" v-model="feedbackTitle" required>
                </div>

                <!-- Textarea para más detalles -->
                <div class="mb-3">
                  <label for="detailsTextarea" class="form-label">Provide more details</label>
                  <textarea class="form-control" id="detailsTextarea" rows="4" style="resize: vertical;"
                  v-model="feedbackMessage" placeholder="Provide more details..."></textarea>
                </div>

                <!-- Input para adjuntar imágenes -->
                <div class="mb-3 d-none">   <!-- TODO: quitar d-none a input images feedback cuando back esté preparado para recibir imagenes -->
                  <label for="imageUpload" class="form-label">Attach images</label>
                  <input type="file" class="form-control" id="imageUpload" accept=".png, .jpg, .jpeg" multiple>
                </div>

              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" id="submitFeedbackBtn" class="btn btn-primary" @click="sendFeedback()" >Submit Feedback</button>
            </div>
          </div>
        </div>
      </div>

      <div class="header_image">
        <a id="account">
          <RouterLink to="/account">
            <img src="@/assets/user.png" alt="" width="32" height="32" class="rounded-circle">
          </RouterLink>
        </a>
      </div>
    </div>

  </header>
  <div class="l-navbar" id="nav-bar">
    <nav class="nav">
      <div>
        <a href="/" class="nav_logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="25px" height="25px" viewBox="0 0 138 138" fill="none" class="nav_logo-icon bx">
            <path d="M137.5 109C137.5 146.555 105.555 136 67.9999 136C30.4446 136 0 146.555 0 109C0 71.4446 30.4446 -0.000244141 67.9999 -0.000244141C105.555 -0.000244141 137.5 71.4446 137.5 109Z" fill="#915EFF"/>
            <path d="M37.0249 123C35.7749 123 35.1499 122.375 35.1499 121.125V51.5999C35.1499 50.7999 35.3999 50.0499 35.8999 49.3499L53.5999 24.1499C54.1499 23.3999 54.9499 23.0249 55.9999 23.0249H82.8499C83.9499 23.0249 84.7499 23.3999 85.2499 24.1499L103.1 49.3499C103.6 50.0499 103.85 50.7999 103.85 51.5999V121.125C103.85 122.375 103.225 123 101.975 123H74.5249C73.2749 123 72.6499 122.375 72.6499 121.125V92.9999H66.3499V121.125C66.3499 122.375 65.7249 123 64.4749 123H37.0249ZM69.4999 66.9749C71.6499 66.9749 73.3999 66.2999 74.7499 64.9499C76.0999 63.5999 76.7749 61.8749 76.7749 59.7749C76.7749 57.6249 76.0999 55.8749 74.7499 54.5249C73.3999 53.1749 71.6499 52.4999 69.4999 52.4999C67.3499 52.4999 65.5999 53.1749 64.2499 54.5249C62.8999 55.8749 62.2249 57.6249 62.2249 59.7749C62.2249 61.8749 62.8999 63.5999 64.2499 64.9499C65.5999 66.2999 67.3499 66.9749 69.4999 66.9749Z" fill="white"/>
            <path d="M97 54C92.0769 46.9752 92.3846 45.8248 87.7692 43.7052C83.1538 41.5856 77.9231 41.2826 73 43.7052" stroke="#915EFF" stroke-width="8"/>
            <path d="M42 54C46.9231 46.9752 46.6154 45.8248 51.2308 43.7052C55.8462 41.5856 61.0769 41.2826 66 43.7052" stroke="#915EFF" stroke-width="8"/>
          </svg>
          <span class="nav_logo-name">HR Suite</span>
        </a>
        <div class="nav_list">
          <RouterLink to="/">
            <a class="nav_link" id="home">
              <i class="fa-solid fa-house me-3 nav_icon"></i>
              <span class="nav_name">Home</span>
            </a>
          </RouterLink>
          <RouterLink to="/home-office">
            <a class="nav_link" id="home-office" v-if="!isIntern">
              <i class="fa-solid fa-house-laptop me-3 nav_icon"></i>
              <span class="nav_name">Home Office</span>
            </a>
          </RouterLink>
          <RouterLink to="/calendar">
            <a class="nav_link" id="calendar">
              <i class="fa-solid fa-umbrella-beach me-3 nav_icon"></i>
              <span class="nav_name">Holidays</span>
            </a>
          </RouterLink>
          <RouterLink to="/trip">
            <a class="nav_link" id="trip" v-if="!isIntern">
              <i class="fa-solid fa-plane me-3 nav_icon"></i>
              <span class="nav_name">Travels</span>
            </a>
          </RouterLink>
          <!-- Sección Responsible con notificación -->
          <RouterLink to="/responsible">
            <a class="nav_link position-relative" v-if="isResponsible" @click="clearUpdate('responsible')"
              id="responsible">
              <i class="fa-solid fa-sitemap me-3 nav_icon"></i>
              <span class="nav_name">Responsible</span>
              <!-- Condicional para mostrar el puntito si hay actualización -->
              <span v-if="hasUpdateResponsible" class="notification-dot"></span>
            </a>
          </RouterLink>
          <!-- Sección Management con notificación -->
          <RouterLink to="/management">
            <a class="nav_link position-relative" v-if="isManager" @click="clearUpdate('management')" id="management">
              <i class="fa-solid fa-cogs me-3 nav_icon"></i>
              <span class="nav_name">Management</span>
              <!-- Condicional para mostrar el puntito si hay actualización -->
              <span v-if="hasUpdateManagement" class="notification-dot"></span>
            </a>
          </RouterLink>
          <li class="nav-item dropdown mt-1" v-if="isAdmin">
            <a href="#" class="nav_link d-flex justify-content-between align-items-center w-100" id="hrDropdown"
              role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <div>
                <i class="fa-solid fa-users-gear nav_icon me-4"></i>
                <span class="nav_name ml-1">HR</span>
              </div>
              <i id="arrowDown" class="fa-solid fa-angle-down mr-4 d-none"></i>
              <i id="arrowUp" class="fa-solid fa-angle-up mr-4"></i>
            </a>
            <ul class="dropdown-menu" aria-labelledby="hrDropdown">
              <li>
                <RouterLink to="/hr/festivities" class="dropdown-item">Festivities</RouterLink>
              </li>
              <li>
                <RouterLink to="/hr/city-days" class="dropdown-item">City days</RouterLink>
              </li>
              <li>
                <RouterLink to="/hr/logs" class="dropdown-item">Logs</RouterLink>
              </li>
              <li>
                <RouterLink to="/hr/inputs" class="dropdown-item">Inputs</RouterLink>
              </li>
              <li>
                <RouterLink to="/hr/userinfo" class="dropdown-item">User Info</RouterLink>
              </li>
              <li>
                <RouterLink to="/hr/reporting" class="dropdown-item">Reporting</RouterLink>
              </li>
              <!--  <li>
                <RouterLink to="/hr/headcount" class="dropdown-item">Head Count</RouterLink>
              </li> -->
            </ul>
          </li>
        </div>
      </div>
      <a @click="logout" to="/" class="nav_link">
        <i class='bx bx-log-out nav_icon'></i>
        <span class="nav_name">Log out</span>
      </a>
    </nav>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getUsername, hasUpdateResponsible, hasUpdateManagement, updateManagement, updateResponsible, showNavbar, loadingMessage, stopLoadingMessage, notifySuccess } from "../assets/globalFunctions.js";
import { BACKEND_HOST } from "../config";

let feedbackTag = ref("BUG")
let feedbackTitle = ref("")
let feedbackMessage = ref("")

const router = useRouter();
const route = useRoute();

const isAuth = ref(false);

const logout = () => {
  localStorage.removeItem('Authorization');
  localStorage.removeItem('name');
  localStorage.removeItem('rank');
  isAuth.value = false;
  setTimeout(function () {
    location.reload();
  }, 600);
  router.push('/');
}

const userRoles = localStorage.getItem('rank');
const isIntern = computed(() => userRoles.includes('xfapochizfrtv05ikicmqbb4y4ld5415jhwg7yk81fzbh6paw122sc06t6i70fpl'));
const isAdmin = computed(() => userRoles.includes('cb88dfe7c01e300d2be5b0368f2e50895dd181601a7d31e61bfd7e597f7ef127'));
const isManager = computed(() => userRoles.includes('38ovzt6htlz9dvkfpb6gdidjlt2zkxsue4q39wfehxlp7ykhjrp75hmk954spu0n'));
const isResponsible = computed(() => userRoles.includes('e7698668c7a6762266de376ce96adbea6e2cc5cd203bad0adb4e1832480b784b'));

onMounted(() => {
  isAuth.value = localStorage.getItem('Authorization') ? true : false;
  checkForUpdates();
  if(document.getElementById('hrDropdown')) {
    document.getElementById('hrDropdown').addEventListener('click', function () {
    changeIcon();
  });
  }
  document.getElementById('imageUpload').addEventListener('change', handleFiles);

  // Manejo del modal
  document.getElementById('submitFeedbackBtn').addEventListener('click', function () {
    const contactReason = document.getElementById('contactReason').value;
    const summary = document.getElementById('summaryInput').value;
    const details = document.getElementById('detailsTextarea').value;
    const files = document.getElementById('imageUpload').files;

    // Convierte los archivos a base64 para que así los puedas usar en python
    const fileArray = Array.from(files);
    const promises = fileArray.map(file => convertToBase64(file));

    Promise.all(promises).then(results => {
      const images = results.map((base64, index) => ({
        filename: fileArray[index].name,
        data: base64
      }));

      const feedbackData = {
        contactReason,
        summary,
        details,
        images
      };

      // LLAMADA A LA API AQUÍ
      console.log(feedbackData);

      // Restablecer el formulario
      document.getElementById('feedbackForm').reset();

      // Ocultar el modal
      const feedbackModal = bootstrap.Modal.getInstance(document.getElementById('feedbackModal'));
      feedbackModal.hide();

      // Notificación de éxito
      notifySuccess("Thanks for contacting us, we'll take matters as soon as possible!");
    });
  });


  /* Esto es para ocultar la navbar al abrir el modal **/
  let originalZIndex = null;

  const navbar = document.querySelector('.l-navbar');

  if (navbar) {
    document.getElementById('feedbackModal').addEventListener('shown.bs.modal', function () {
      if (originalZIndex === null) {
        originalZIndex = window.getComputedStyle(navbar).zIndex;
      }
      navbar.style.zIndex = 2;
    });

    document.getElementById('feedbackModal').addEventListener('hidden.bs.modal', function () {
      navbar.style.zIndex = originalZIndex;
    });
  }
});

/* Unread signing request notifications*/
//Each time user navigates with navbar, check if they have notifications
router.beforeEach((to, from, next) => {
  if (to.path === '/responsible') {
    clearUpdate('responsible');
  } else if (to.path === '/management') {
    clearUpdate('management');
  } else {
    checkForUpdates();
  }
  next();
});
const checkForUpdates = () => {
  if (hasUpdateResponsible.value != true) {
    setTimeout(() => {
      hasUpdateResponsible.value = true;
    }, 1000);
  }
  if (hasUpdateManagement.value != true) {
    setTimeout(() => {
      hasUpdateManagement.value = true;
    }, 1000);
  }
}
//Remove notification dot
const clearUpdate = (section) => {
  if (section === 'responsible') {
    updateResponsible(false);
  } else if (section === 'management') {
    updateManagement(false);
  }
}

function handleFiles(event) {
  const files = event.target.files;
  const fileArray = Array.from(files);
  const promises = fileArray.map(file => convertToBase64(file));

  Promise.all(promises).then(results => {
    const images = results.map((base64, index) => ({
      filename: fileArray[index].name,
      data: base64
    }));

    // Convert to JSON
    const jsonImages = JSON.stringify(images);

    // Do something with jsonImages
    console.log(jsonImages);
  });
}

function convertToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function sendFeedback(){
  // Convierte los archivos a base64 para que así los puedas usar en python
  const files = document.getElementById('imageUpload').files;
  const fileArray = Array.from(files);
  const promises = fileArray.map(file => convertToBase64(file));

  try {

    let json = {}
    await Promise.all(promises).then(results => {
      const images = results.map((base64, index) => ({
        filename: fileArray[index].name,
        data: base64
      }));

      json = {
        'tag': this.feedbackTag,
        'title': this.feedbackTitle,
        'message': this.feedbackMessage,
        'img': images
      } 
    });

    loadingMessage();
    const response = await fetch(`${BACKEND_HOST}access/send-feedback`, {
      method: 'POST',
      headers: {
        'Authorization': localStorage.getItem('Authorization'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(json)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error('Unable to send feedback: ' + (error.message || error.state));
    }

    notifySuccess("Feedback sent successfully!");
    stopLoadingMessage();

    document.getElementById('feedbackForm').reset();
    const feedbackModal = bootstrap.Modal.getInstance(document.getElementById('feedbackModal'));
    feedbackModal.hide();
  } catch (error) {
    console.log(error.message);
    stopLoadingMessage();
  }
};

function changeIcon() {
  let arrowDown = document.getElementById('arrowDown');
  let arrowUp = document.getElementById('arrowUp');
  if (!arrowUp.classList.contains('d-none')) {
    arrowDown.classList.remove('d-none');
    arrowUp.classList.add('d-none');
  } else {
    arrowDown.classList.add('d-none');
    arrowUp.classList.remove('d-none');
  }
}
</script>
<style scoped>
.notification-dot {
  position: absolute;
  top: 0px;
  left: 40px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: red;
}
</style>
