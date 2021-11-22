<template>
  <div id="register" class="container-lg container-fluid">
    <div class="centered-flex-div">
      <h2 class="mb-3 mt-4">Sign Up</h2>

      <v-loader v-if="isLoading" />

      <v-alert class="mb-3" v-else-if="error.message">
        {{ error.message }}
      </v-alert>

      <form @submit.prevent="registerUser(formData)">
        <v-form-input
          v-model="formData.name"
          inputId="name"
          label="Name"
          :errors="error.errors ? error.errors.name : undefined"
          :autofocus="true"
        />
        <v-form-input
          v-model="formData.email"
          inputId="email"
          label="Email Address"
          :errors="error.errors ? error.errors.email : undefined"
        />
        <v-form-input
          v-model="formData.password"
          inputId="password"
          label="Password"
          type="password"
          :errors="error.errors ? error.errors.password : undefined"
        />
        <v-form-input
          v-model="formData.confirmPassword"
          inputId="confirmPassword"
          label="Confirm Password"
          type="password"
        />

        <div class="d-flex align-items-center justify-content-between mt-4">
          <button type="submit" class="btn btn-dark px-4">Register</button>

          <p class="mb-0">
            Have an account?
            <router-link :to="{ name: 'login', query: { redirect } }"
              >Sign In</router-link
            >
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";
import Alert from "@/components/shared/Alert";
import Loader from "@/components/shared/Loader";
import FormInput from "@/components/shared/FormInput";
import useAuthentication from "@/hooks/useAuthentication.js";

export default {
  name: "Register",
  components: {
      FormInput,
      Loader,
      Alert,
  },
  setup() {
    const { registerUser, redirect, redirectWatch, error, isLoading } =
      useAuthentication();
      
    const formData = reactive({
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    });

    redirectWatch();

    return {
      formData,
      registerUser,
      redirect,
      error,
      isLoading,
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/centered-flex-div";
</style>
