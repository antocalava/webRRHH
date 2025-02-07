<template>
  <main class="mt-3 mx-2 flex-body">
    <div class="container">
      <div class="row justify-content-center">
        <change-password-form/>
      </div>
    </div>
  </main>
</template>

<script>
  import ChangePasswordForm from '../components/ChangePasswordForm.vue';

  export default {
    components: {
      ChangePasswordForm 
    }
  };
</script>
