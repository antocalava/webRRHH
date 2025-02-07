<template>
  <div class="background">
    <div class="shape"></div>
    <div class="shape"></div>
  </div>
  <form @submit.prevent="changePassword">
    <h3>Change Password</h3>

    <label for="newPassword">New Password</label>
    <div class="password-container">
      <input :type="passwordVisible ? 'text' : 'password'" v-model="newPassword" id="newPassword"
        placeholder="Enter new password" autocomplete="off" required />
      <span @click="changeVisibility" class="visibility-icon">
        <svg v-if="passwordVisible" width="20" height="20" viewBox="0 0 512 512" fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M255.999 152C247.163 152 239.999 159.164 239.999 168V264C239.999 272.836 247.163 280 255.999 280H351.999C360.835 280 367.999 272.836 367.999 264C367.999 159.164 304.835 96 199.999 96C191.163 96 183.999 103.164 183.999 112V184C183.999 192.836 191.163 200 199.999 200C208.835 200 215.999 192.836 215.999 184V128H255.999V168H223.999V184H191.999C191.999 167.455 203.455 153.999 215.999 143.999C199.455 152 191.999 167.455 191.999 184H191.999C191.999 183.271 191.999 152 255.999 152Z"
            fill="black" />
        </svg>
      </span>
    </div>

    <label for="confirmPassword">Confirm Password</label>
    <div class="password-container">
      <input :type="passwordVisible ? 'text' : 'password'" v-model="confirmPassword" id="confirmPassword"
        placeholder="Confirm new password" autocomplete="off" required />
      <span @click="changeVisibility" class="visibility-icon">
        <svg v-if="passwordVisible" width="20" height="20" viewBox="0 0 512 512" fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M255.999 152C247.163 152 239.999 159.164 239.999 168V264C239.999 272.836 247.163 280 255.999 280H351.999C360.835 280 367.999 272.836 367.999 264C367.999 159.164 304.835 96 199.999 96C191.163 96 183.999 103.164 183.999 112V184C183.999 192.836 191.163 200 199.999 200C208.835 200 215.999 192.836 215.999 184V128H255.999V168H223.999V184H191.999C191.999 167.455 203.455 153.999 215.999 143.999C199.455 152 191.999 167.455 191.999 184H191.999C191.999 183.271 191.999 152 255.999 152Z"
            fill="black" />
        </svg>
      </span>
    </div>

    <button type="submit">Submit</button>
  </form>
</template>


<script>
import { notifySuccess, notifyError } from '../assets/globalFunctions';
import { BACKEND_HOST } from '../config';

export default {
  data() {
    return {
      newPassword: "",
      confirmPassword: "",
      newPasswordVisible: false,
      confirmPasswordVisible: false
    };
  },
  methods: {
    changeVisibility(e) {
      let button = e.target.closest("button");

      if (!button) {
        return;
      }
      let input = button.previousElementSibling;

      if (!input) {
        return;
      }
      let type = input.type === 'password' ? 'text' : 'password';
      input.setAttribute('type', type);

      if (button.dataset.input === "new") {
        this.newPasswordVisible = !this.newPasswordVisible;
      } else if (button.dataset.input === "confirm") {
        this.confirmPasswordVisible = !this.confirmPasswordVisible;
      }

    },
    changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        notifyError('Passwords do not match');
        return;
      }

      if (!this.newPassword || !this.confirmPassword || this.newPassword.trim().length === 0 || this.confirmPassword.trim().length === 0) {
        notifyError("Please fill in all fields");
        return;
      }

      const passwordRegex = /^[a-zA-Z0-9]{6,}$/;
      if (!passwordRegex.test(this.newPassword)) {
        notifyError('The password must contain only letters and numbers, with a minimum length of 6 characters.');
        return;
      }

      const requestBody = {
        newPassword: this.newPassword
      };

      fetch(`${BACKEND_HOST}access/change-password`, {
        method: 'POST',
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error in the API call');
          }
          return response.json();
        })
        .then(() => {
          notifySuccess("Password successfully changed");
          const timeout = 500;
          setTimeout(() => {
            localStorage.removeItem('Authorization');
            localStorage.removeItem('name');
            localStorage.removeItem('rank');
            setTimeout(function () {
              location.reload();
            }, timeout);
          }, timeout);
        })
        .catch(error => {
          console.error(error);
          notifyError('Error in the application');
        });
    }
  }
};
</script>

<style scoped>
.form-container {
  background-color: #ffffff;
  /* Fondo blanco para el formulario */
  border-radius: 10px;
  /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* Sombreado suave */
  max-width: 400px;
  /* Ancho máximo para el formulario */
  width: 100%;
  /* Ancho del 100% del contenedor */
}

.min-vh-100 {
  min-height: 100vh;
  /* Altura mínima del contenedor para centrar verticalmente */
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

*,
*:before,
*:after {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

body {
  background-color: #080710;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  /* Negrita */
}

.background {
  width: 430px;
  height: 520px;
  position: absolute;
  transform: translate(-50%, -50%);
  left: 50%;
  top: 50%;
}

.background .shape {
  height: 200px;
  width: 200px;
  position: absolute;
  border-radius: 50%;
}

.background .shape:first-child {
  background: linear-gradient(#0075C2, #06B4EA);
  left: -80px;
  top: -80px;
}

.background .shape:last-child {
  background: linear-gradient(to right, #A591CD, #24006D);
  right: -30px;
  bottom: -80px;
}

form {
  height: 490px;
  width: 400px;
  background-color: rgba(255, 255, 255, 0.13);
  position: absolute;
  transform: translate(-50%, -50%);
  top: 50%;
  left: 50%;
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 40px rgba(8, 7, 16, 0.6);
  padding: 50px 35px;
}

form * {
  font-family: 'Poppins', sans-serif;
  color: #000000;
  font-weight: 600;
  /* Negrita */
  letter-spacing: 0.5px;
  outline: none;
  border: none;
}

form h3 {
  font-size: 32px;
  font-weight: 500;
  line-height: 42px;
  text-align: center;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-top: 30px;
  font-size: 16px;
  font-weight: 500;
}

input {
  display: block;
  height: 50px;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.07);
  border-radius: 3px;
  padding: 0 10px;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 500;
}

::placeholder {
  color: #e5e5e5;
}

button {
  margin-top: 50px;
  width: 100%;
  background-color: #FFFFFF;
  color: #080710;
  padding: 15px 0;
  font-size: 18px;
  font-weight: 600;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease;
}

button:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.password-container {
  position: relative;
}

input[type="password"] {
  padding-right: 40px;
}

.visibility-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.visibility-icon svg {
  fill: #000;
}
</style>