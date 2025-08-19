<template>
  <div class="container">
    <h1 class="text-center">Welcome to Chatire!</h1>

    <div id="auth-container" class="row">
      <ul class="nav nav-tabs nav-fill" id="myTab">
        <li class="nav-item">
          <a class="nav-link active" id="signup-tab" data-bs-toggle="tab" href="#signup" aria-controls="signup">Sign
            Up</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" id="signin-tab" data-bs-toggle="tab" href="#signin" aria-controls="signin">Sign In</a>
        </li>
      </ul>

      <div class="tab-content" id="myTabContent">

        <div class="tab-pane fade show active" id="signup" aria-labelledby="signup-tab">
          <form @submit.prevent="signUp">
            <div class="mb-3">
              <input v-model="email" type="email" class="form-control" id="email" placeholder="Email Address" required>
            </div>
            <div class="row">
              <div class="col-md-12 mb-3">
                <input v-model="username" type="text" class="form-control" id="signup-username" placeholder="Username"
                  required>
              </div>
              <div class="col-md-6 mb-3">
                <input v-model="password" type="password" class="form-control" id="signup-password"
                  placeholder="Password" required>
              </div>
              <div class="col-md-6 mb-3">
                <input v-model="re_password" type="password" class="form-control" id="signup-re-password"
                  placeholder="Confirm Password" required>
              </div>
            </div>
            <div class="mb-3">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="toc" required>
                <label class="form-check-label" for="toc">
                  Accept terms and Conditions
                </label>
              </div>
            </div>
            <button type="submit" class="btn btn-primary w-100">Sign up</button>
          </form>
        </div>

        <div class="tab-pane fade" id="signin" aria-labelledby="signin-tab">
          <form @submit.prevent="signIn">
            <div class="mb-3">
              <input v-model="username" type="text" class="form-control" id="signin-username" placeholder="Username"
                required>
            </div>
            <div class="mb-3">
              <input v-model="password" type="password" class="form-control" id="signin-password" placeholder="Password"
                required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Sign in</button>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      re_password: ''
    }
  },
  methods: {
    async signUp() {
      try {
        const response = await fetch('http://localhost:8000/auth/users/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.$data)
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        alert("Your account has been created. You will be signed in automatically");
        this.signIn();
      } catch (error) {
        alert(error);
      }
    },

    async signIn() {
      const credentials = { username: this.username, password: this.password };
      try {
        const response = await fetch('http://localhost:8000/auth/token/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        const data = await response.json();
        sessionStorage.setItem('authToken', data.auth_token);
        sessionStorage.setItem('username', this.username);
        this.$router.push('/chats');
      } catch (error) {
        alert(error);
      }
    }
  }
}
</script>

<style scoped>
#auth-container {
  margin-top: 50px;
}

.tab-content {
  padding-top: 20px;
}
</style>
