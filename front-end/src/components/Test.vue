<template>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onPass">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" v-model="Form.Test1" class="form-control"  id="username" placeholder="">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="text" v-model="Form.Test2" class="form-control"  id="password" placeholder="">
          </div>
          <button type="submit" class="btn btn-primary">Pass on</button>
        </form>
      </div>
    </div>
</template>

<script>
import store from "../store";

export default {
   name: 'Test',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      Form: {
        Test1: '',
        Test2: ''
      }
    }
  },
  methods: {
    onPass (e) {

      const path = '/test'
      // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$axios.post(path, {
          'Test1': this.Form.Test1,
          'Test2': this.Form.Test2,
          'ifImg': true
        }).then((response) => {
          // handle success
          alert(response.data.message1)
        })
        .catch((error) => {
          // handle error
          console.log(error)
        })
    }
  }

}
</script>

<style scoped>

</style>
