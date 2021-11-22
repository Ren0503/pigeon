<template>
  <div class="alert" :class="type" role="alert">
    <strong>
      <slot />
    </strong>
  </div>
</template>

<script>
export default {
  name: "Alert",
  props: {
    type: {
      type: String,
      default: "alert-info",
    },
  },
};
</script>

<style scoped lang="scss">
</style>
