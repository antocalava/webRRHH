import { useToast } from "vue-toastification";
import { ref } from 'vue';

export let hasUpdateResponsible = ref(false);
export let hasUpdateManagement = ref(false);
let firstLogin = true;
let toggled = true;

export function notifySuccess(message) {
  const toast = useToast();
  toast.success(message, {
    timeout: 2500
  });
}

export function notifyError(message) {
  const toast = useToast();
  toast.error(message, {
    timeout: 3500,
  });
}

export function updateResponsible(value) {
  hasUpdateResponsible = ref(value);
}

export function updateManagement(value) {
  hasUpdateManagement = ref(value);
}
/*We save the username in the localStorage to later read it and print it*/
export function saveUsername(email) {
  let [name, surname] = email.split('@')[0].split('.');
  name = name.charAt(0).toUpperCase() + name.slice(1);
  surname = surname.charAt(0).toUpperCase() + surname.slice(1);
  let fullName = `${name} ${surname}`;
  localStorage.setItem('name', fullName);
}

//We get the username of the user logged in
export function getUsername() {
  return localStorage.getItem('name');
}

//TODO: fix, this method is not reusable EITHER
export function closeModalAndBackdrop() {
  const modal = document.getElementById('modalConfirm');
  const backdrop = document.getElementsByClassName('modal-backdrop')[0];

  modal.style.display = 'none';
  backdrop.style.display = 'none';
}

//TODO: fix, this method is not reusable. TO FIX: TAKE IN PARAMETER THE ELEMENT ID OF THE MODAL
export function openModal() {
  //remove backdrop if exists
  const backdrop = document.getElementsByClassName('modal-backdrop')[0];
  if (backdrop) {
    backdrop.remove();
  }
  const modal = document.getElementById('modalConfirm'); // replace string with parameter!!!!
  modal.style.display = 'block';
}

//TODO: make a method to dismiss the modal too plssssssssssss, also taking modal element id as paramenetr

export function formatDate(date) {
  if (!date) return '';
  const d = new Date(date);
  const day = d.getDate().toString().padStart(2, '0');
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const year = d.getFullYear();
  return `${day}/${month}/${year}`;
}

export function formatDate2(date) {
  if (!date) return '';
  const d = new Date(date);
  const day = d.getDate().toString().padStart(2, '0');
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const year = d.getFullYear();
  return `${year}-${month}-${day}`;
}

export function capitalizeWords(words) {
  return words.toLowerCase().replace(/(^|[\s\u200B-\u200D\uFEFF-])\S/gu, char => {
    return char.toUpperCase();
  });
}

export function loadingMessage() {
  let loadingMessage = document.getElementById("loadingMessage");

  if (!loadingMessage) {
    loadingMessage = document.createElement("div");
    loadingMessage.id = "loadingMessage";
    loadingMessage.role = "alert";
    loadingMessage.innerHTML = " Loading";
    loadingMessage.classList.add("message");
    document.getElementById("app").appendChild(loadingMessage);
  }
  setTimeout(() => {
    loadingMessage?.classList.remove("hide");
    loadingMessage.classList.add("show");
  }, 200);
}

export function showNavbar(toggleId, navId, headerId) {
  const toggle = document.getElementById(toggleId),
    nav = document.getElementById("nav-bar"),
    bodypd = document.getElementById("bodyApp"),
    headerpd = document.getElementById("header")
  // Validate that all variables exist
  if (toggle && nav && bodypd && headerpd) {

    toggle.addEventListener('click', () => {
      // show navbar
      nav.classList.toggle('show')
      // change icon
      toggle.classList.toggle('bx-x')
      // add padding to body
      bodypd.classList.toggle('body-pd')
      // add padding to header
      headerpd.classList.toggle('body-pd')
      toggled = !toggled;
    })
  }
}


export function stopLoadingMessage() {
  let loadingMessage = document.getElementById("loadingMessage");
  if (loadingMessage.classList.contains('show')) {
    loadingMessage?.classList.remove("show");
    loadingMessage?.classList.add("hide");
  }
}

window.onload = function (event) {
  switch (window.location.href) {
    case 'http://localhost:8864/':
      document.getElementById('home').classList.add('active');
      break;
    case 'http://localhost:8864/trip':
      document.getElementById('trip').classList.add('active');
      break;
    case 'http://localhost:8864/calendar':
      document.getElementById('calendar').classList.add('active');
      break;
    case 'http://localhost:8864/home-office':
      document.getElementById('home-office').classList.add('active');
      break;
    case 'http://localhost:8864/responsible':
      document.getElementById('responsible').classList.add('active');
      break;
    case 'http://localhost:8864/travel':
      document.getElementById('travel').classList.add('active');
      break;
    default:
      //TODO: FIX --> this cannot be the default case, it blows up when you logOut
      document.getElementById('hrDropdown').classList.add('active');
      break;
  }

  //Si está logueado cargamos la navbar
  if (!!localStorage.getItem('Authorization')) {
    let toggled = false;
    
    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink() {
      if (linkColor) {
        linkColor.forEach(l => l.classList.remove('active'))
        this.classList.add('active')
      }
    }
    linkColor.forEach(l => l.addEventListener('click', colorLink))

    if (document.getElementById("hrDropdown")) {
      document.getElementById("hrDropdown").addEventListener('click', () => {
        const showNavbar = (toggleId, navId) => {
          const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById("bodyApp"),
            headerpd = document.getElementById("header");
    
          if (toggle && nav && bodypd) {
            if (!nav.classList.contains('show')) {
              nav.classList.add('show');
              toggle.classList.add('bx-x');
              bodypd.classList.add('body-pd');
              headerpd.classList.add('body-pd'); 
            }
          }
        }
    
        showNavbar('header-toggle', 'nav-bar');
      });
    }
  } else {
    const loginView = document.querySelector('.loginView');
    if (loginView) {
      const grandparent = loginView.parentElement.parentElement;
      grandparent.style.margin = '0';
      grandparent.style.padding = '0';
    }
  }

  if(localStorage.getItem('Authorization') === true && firstLogin) {
    firstLogin = false;
    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');
  } else {
    firstLogin = true;
  }
};

