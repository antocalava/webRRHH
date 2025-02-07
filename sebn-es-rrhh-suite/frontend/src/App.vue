<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div :class="{ 'authenticated': isAuthenticated, 'unauthenticated': !isAuthenticated }"
    style="width: 100%; height: 85vh;">
    <Navbar v-if="isAuthenticated" />
    <RouterView />
  </div>
</template>


<script>
import Navbar from './components/NavbarItem.vue';
export default {
  components: {
    Navbar
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('Authorization');
    }
  }
}
</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.authenticated {
  /* Estilos para cuando el usuario está autenticado */
  margin-left: 0px;
  /* Ajusta el margen si tienes un sidebar o navbar a la izquierda */
}

.unauthenticated {
  /* Estilos para cuando el usuario no está autenticado */
  margin: 0;
}


@media (min-width: 1024px) {
  /* header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  } */

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
