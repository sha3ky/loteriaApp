<!-- PostComponent.vue -->
<template>
  <div class="post">
    <h2>{{ post.author }}</h2>
    <p>{{ post.content }}</p>
  </div>
</template>

<script>
export default {
  props: {
    post: Object,
  },
};
</script>

<style scoped>
.post {
  background: #fff;

  margin-bottom: 1em;
  border-bottom: 1px solid #ddd;
}
.post h2 {
  font-size: 1.3em;
  margin-bottom: 0.5em;
}
.post p {
  color: #888;
}
</style>
