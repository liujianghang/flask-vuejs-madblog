<template>
  <!-- 使用role属性告诉辅助设备（如屏幕阅读器）这个元素所扮演的角色，起到一个增强作用 -->
  <!-- 这里的class是动态绑定，接收props -->
  <div class="alert" role="alert" v-bind:class="'alert-' + variant">
    {{ message }}
  </div>
</template>

<script>
export default {
  name: "Alert",
  props:['variant','message']
}
</script>

<style scoped>

</style>
