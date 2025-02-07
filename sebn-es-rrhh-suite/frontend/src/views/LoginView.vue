<template>
  <div class="background">
    <div class="shape"></div>
    <div class="shape"></div>
  </div>
  <form @submit.prevent="login">
    <h3>Login Here</h3>

    <label for="email">Email</label>
    <input type="email" v-model="email" id="email" placeholder="Email" required>

    <label for="password">Password</label>
    <div class="password-container">
      <input :type="passwordVisible ? 'text' : 'password'" v-model="password" id="password" placeholder="Password"
        required>
      <span @click="changeVisibility" class="visibility-icon">
        <svg v-if="passwordVisible" width="20" height="20" viewBox="0 0 512 512" fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M346.317 321.218C346.317 371.386 305.648 412.054 255.48 412.054C205.312 412.054 164.644 371.386 164.644 321.218C164.644 271.05 205.312 230.381 255.48 230.381C305.648 230.381 346.317 271.05 346.317 321.218Z"
            fill="black" />
          <path
            d="M263.316 101.949C267.506 104.395 269.752 106.638 272 111C272.361 113.651 272.361 113.651 272.341 116.525C272.34 117.605 272.34 118.686 272.34 119.8C272.324 120.955 272.309 122.11 272.293 123.301C272.289 124.492 272.284 125.684 272.28 126.911C272.263 130.712 272.226 134.512 272.188 138.313C272.172 140.891 272.159 143.47 272.146 146.049C272.113 152.366 272.063 158.683 272 165C306.27 164.526 340.44 174.135 371.039 189.188C373.108 190.191 372.911 190.001 375.314 191.029C375.67 190.387 376.712 188.716 377.079 188.054C381.355 180.352 385.669 172.672 390 165C392.833 159.958 395.73 154.952 398.559 149.908C402.149 143.738 405.068 140.311 412 138C418.27 137.469 422.864 138.182 428 142C431.866 146.736 432.796 150.88 432.486 156.979C431.964 160.224 431.038 162.241 429.398 165.074C425.294 172.283 421.25 179.526 417.211 186.771C413.967 192.569 410.653 198.303 407.164 203.957C405.863 206.086 406.342 205.469 404.508 208.149C408.987 210.829 412.361 212.568 415.625 215.063C416.145 215.46 416.665 215.857 417.201 216.266C429.825 225.964 441.593 236.447 452.875 247.672C458.023 252.787 463.155 257.918 468.317 263.018C470.613 265.292 472.9 267.577 475.188 269.859C477.559 272.197 479.91 274.555 482.27 276.903C485.599 280.939 486.413 284.804 486.246 290.016C485.66 294.744 483.456 297.802 479.938 300.813C476.083 303.683 474.135 304.239 469.375 304.438C468.372 304.498 467.369 304.559 466.336 304.621C457.907 303.052 451.489 294.718 445.742 288.832C441.198 284.235 436.66 279.632 432.134 275.017C420.926 263.605 409.307 253.05 396.556 243.404C309.272 177.882 183.088 184.69 101 255C100.333 255.57 99.6665 256.139 98.9795 256.726C88.6951 265.766 79.2491 275.721 69.636 285.46C63.1441 292.031 55.3915 303.045 46.0977 304.434C39.9107 304.442 35.7565 304.4 31 300C26.9024 295.459 25.9156 292.335 25.6719 286.23C27.5191 273.674 48.2385 258.414 56.6229 249.976C67.2301 239.31 77.7526 228.803 90 220C95.4228 215.889 100.984 212.062 106.694 208.354C102.691 200.101 98.6658 192.77 94 184.875C93.1144 183.365 93.1144 183.365 92.2109 181.824C88.9114 176.206 85.5701 170.617 82.1641 165.063C79.2872 159.965 79.4504 154.695 80 149C81.2738 144.562 83.7683 141.82 87.75 139.563C93.3335 137.174 98.299 137.083 104 139.188C109.336 142.241 111.753 147.361 114.655 152.597C116.293 155.524 117.978 158.421 119.664 161.32C125.192 170.834 137.001 191.245 137.001 191.245C137.001 191.245 141.967 188.717 144.906 187.398C145.639 187.077 146.372 186.755 147.126 186.423C176.229 173.572 207.976 164.64 240 165C239.989 164.339 239.978 163.678 239.966 162.997C239.856 156.103 239.78 149.208 239.725 142.313C239.7 139.742 239.666 137.171 239.623 134.599C239.562 130.898 239.534 127.198 239.512 123.496C239.486 122.351 239.46 121.206 239.434 120.026C239.431 112.964 240.143 109.231 245 104C250.375 100.125 257.169 99.43 263.316 101.949Z"
            fill="black" />
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M263.348 356.594C267.537 354.149 269.783 351.905 272.031 347.544C272.392 344.892 272.392 344.892 272.372 342.019C272.372 340.938 272.371 339.858 272.371 338.744C272.356 337.589 272.34 336.433 272.324 335.243C272.32 334.051 272.316 332.86 272.311 331.632C272.295 327.832 272.257 324.032 272.219 320.231C272.204 317.652 272.19 315.074 272.178 312.495C272.145 306.178 272.094 299.861 272.031 293.544C306.302 294.018 340.471 284.408 371.07 269.356C373.139 268.352 372.942 268.542 375.345 267.515C375.701 268.157 376.743 269.828 377.11 270.489C381.387 278.192 385.701 285.872 390.031 293.544C392.864 298.586 395.761 303.592 398.591 308.636C402.181 314.806 405.099 318.233 412.031 320.544C418.301 321.075 422.895 320.362 428.031 316.544C431.898 311.807 432.828 307.664 432.518 301.565C431.995 298.32 431.069 296.303 429.43 293.469C425.326 286.26 421.282 279.017 417.242 271.772C413.999 265.975 410.685 260.24 407.195 254.587C405.894 252.458 406.373 253.075 404.539 250.395C409.018 247.714 412.392 245.976 415.656 243.481C416.176 243.084 416.696 242.687 417.232 242.278C429.856 232.58 441.624 222.097 452.906 210.872C458.054 205.757 463.186 200.626 468.348 195.525C470.645 193.251 472.931 190.967 475.219 188.684C477.59 186.347 479.941 183.989 482.302 181.641C485.631 177.605 486.444 173.74 486.277 168.528C485.691 163.799 483.487 160.742 479.969 157.731C476.115 154.861 474.166 154.305 469.406 154.106C468.403 154.046 467.4 153.985 466.367 153.923C457.938 155.492 451.52 163.826 445.773 169.712C441.229 174.308 436.691 178.911 432.165 183.526C420.957 194.938 409.338 205.494 396.587 215.14C309.303 280.661 183.119 273.853 101.031 203.544C100.364 202.974 99.6977 202.404 99.0107 201.817C88.7263 192.778 79.2803 182.823 69.6672 173.084C63.1753 166.512 55.4228 155.499 46.1289 154.11C39.942 154.102 35.7878 154.144 31.0312 158.544C26.9336 163.084 25.9468 166.208 25.7031 172.313C27.5504 184.87 48.2697 200.129 56.6542 208.568C67.2613 219.233 77.7838 229.741 90.0312 238.544C95.4541 242.655 101.015 246.482 106.725 250.19C102.723 258.443 98.6971 265.773 94.0312 273.669C93.1457 275.179 93.1457 275.179 92.2422 276.719C88.9426 282.337 85.6013 287.927 82.1953 293.481C79.3185 298.579 79.4817 303.849 80.0312 309.544C81.305 313.982 83.7995 316.724 87.7812 318.981C93.3647 321.37 98.3303 321.461 104.031 319.356C109.367 316.303 111.784 311.183 114.687 305.947C116.324 303.02 118.009 300.122 119.695 297.223C125.223 287.71 137.032 267.299 137.032 267.299C137.032 267.299 141.999 269.827 144.938 271.145C145.67 271.467 146.403 271.789 147.158 272.121C176.26 284.971 208.007 293.904 240.031 293.544C240.02 294.205 240.009 294.866 239.998 295.547C239.887 302.441 239.811 309.335 239.757 316.23C239.731 318.802 239.697 321.373 239.654 323.944C239.593 327.646 239.565 331.346 239.543 335.048C239.517 336.193 239.491 337.338 239.465 338.517C239.462 345.579 240.174 349.313 245.031 354.544C250.406 358.419 257.2 359.114 263.348 356.594Z"
            fill="black" />
        </svg>
      </span>
    </div>

    <div class="forgot-password text-center">
      <a href="#" @click="forgotPassword()" title="Send password reset email">Have you forgotten your password?</a>
    </div>

    <button type="submit">Log In</button>
  </form>

  <div class="contact-support">
    <a href="#" class="d-flex align-items-center text-decoration-none">
      <i class="fas fa-headset me-2"></i> Contact Support
    </a>
  </div>
</template>

<script>
import axios from 'axios';
import { loadingMessage, notifyError, notifySuccess, saveUsername, stopLoadingMessage } from "@/assets/globalFunctions.js";
import { BACKEND_HOST } from '../config';

export default {
  data() {
    return {
      email: '',
      password: '',
      message: '',
      passwordVisible: false
    }
  },
  methods: {
    changeVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    login() {
      loadingMessage();
      axios.post(`${BACKEND_HOST}access/login`, {
        email: this.email,
        password: this.password
      })
        .then(response => {
          this.message = response;
          if (response && response.data && response.status === 200) {
            localStorage.setItem('Authorization', response.data.authorization);
            this.$cookies.set('AuthorizationCookie', response.data.authorization); //TODO: securizar cookie y guardar token y rank en secure cookies (https)

            this.getRank();
            saveUsername(this.email);
            this.$router.push('/');
            stopLoadingMessage();
          }
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.message = error.response.data.message;
          } else {
            this.message = 'Unknown Error occurred during login';
          }
          notifyError(this.message);
          stopLoadingMessage();
        });
    },
    async getRank() {
      await fetch(`${BACKEND_HOST}access/get-rank`, {
        headers: {
          'Authorization': localStorage.getItem('Authorization'),
          'Content-Type': 'application/json',
        }
      }).then(response => {
        if (!response.ok) {
          throw new Error('The user could not be obtained');
        }
        return response.json();
      }).then(data => {
        localStorage.setItem('rank', data['rank']);
        setTimeout(() => {
          location.reload();
        }, 200);
      }).catch(error => {
        console.error(error);
        notifyError('The user could not be obtained');
      });
    },
    checkEmailValid() {
      try {
        if (!this.email || this.email.trim() == '') throw new Error('Please, provide an email');
        if (!this.email.endsWith('@sebn.com')) throw new Error('Email needs to have a valid format');

        return true
      } catch (error) {
        notifyError(error.message)
        return false
      }
    },
    async forgotPassword() {
      if (this.checkEmailValid) {
        loadingMessage()
        const data = {
          loginEmail: this.email
        };

        try {
          const response = await fetch(`${BACKEND_HOST}access/forgot-password`, {
            method: 'POST',
            headers: {
              'Authorization': localStorage.getItem('Authorization'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error("Failed to request password reset: " + (error.message || error.state));
          }

          notifySuccess('Password reboot request was Successful! You will receive an email as soon as HR resets it');
          stopLoadingMessage();
        } catch (error) {
          console.error(error);
          stopLoadingMessage();
        }
      }
    },
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap');
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
  letter-spacing: 0.5px;
  outline: none;
  border: none;
}

form h3 {
  font-size: 32px;
  font-weight: 500;
  line-height: 42px;
  text-align: center;
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
  font-weight: 300;
}

::placeholder {
  color: #e5e5e5;
}

button {
  margin-top: 30px;
  width: 100%;
  background-color: #FFFFFF;
  color: #080710;
  padding: 15px 0;
  font-size: 18px;
  font-weight: 600;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  outline: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  /* Sombra sutil */
  transition: box-shadow 0.3s ease;
  /* Suaviza la transición de la sombra */
}

button:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2), 0 3px 6px rgba(0, 0, 0, 0.12);
  /* Aumenta la sombra al pasar el mouse */
}

.password-container {
  position: relative;
}

input[type="password"],
input[type="text"] {
  width: 100%;
  padding-right: 40px;
  /* Espacio para el icono */
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

.forgot-password {
  margin-top: 15px;
  text-align: right;
}

.forgot-password a {
  font-size: 14px;
  color: #06B4EA;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-password a:hover {
  color: #0075C2;
  text-decoration: underline;
}

.contact-support {
  position: absolute;
  bottom: -5%;
  right: 2%;
}

.contact-support a {
  font-size: 14px;
  color: #06B4EA;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.contact-support a:hover {
  color: #0075C2;
  background-color: rgba(0, 117, 194, 0.1);
}

.contact-support i {
  font-size: 16px;
}
</style>
