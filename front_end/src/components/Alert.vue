<template>
  <div>
    <b-alert v-bind:variant="status" show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message', 'status'],
};
</script>
