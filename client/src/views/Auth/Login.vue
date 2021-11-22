<template>
  <div id="login" class="container-lg container-fluid">
    <div class="centered-flex-div">
      <h2 class="mb-3 mt-4">Sign In</h2>

      <v-loader v-if="isLoading" />

      <v-alert v-else-if="error.message">
        {{ error.message }}
      </v-alert>

      <form @submit.prevent="loginUser(formData)">
        <v-form-input
          v-model="formData.email"
          inputId="email"
          label="Email Address"
          :autofocus="true"
          :autocomplete="true"
        />
        <v-form-input
          class="mb-1"
          v-model="formData.password"
          inputId="password"
          label="Password"
          type="password"
          :autocomplete="true"
        />

        <div class="d-flex align-items-center justify-content-between mt-4">
          <button type="submit" class="btn btn-dark px-4">Login</button>

          <p class="mb-0">
            New User?
            <router-link :to="{ name: 'register', query: { redirect } }">
              Sign Up
            </router-link>
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
  name: "Login",
  components: {
    FormInput,
    Loader,
    Alert,
  },
  setup() {
    const { user, loginUser, redirect, redirectWatch, isLoading, error } =
      useAuthentication();

    const formData = reactive({
      email: "",
      password: "",
    });

    redirectWatch();

    return {
      formData,
      loginUser,
      redirect,
      isLoading,
      error,
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/centered-flex-div";
</style>