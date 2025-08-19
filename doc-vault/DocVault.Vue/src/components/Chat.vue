<template>
  <div class="container mx-auto">
    <div class="col-sm-6 offset-md-3">

      <div v-if="sessionStarted" id="chat-container" class="card">
        <div class="card-header text-white text-center fw-bold subtle-blue-gradient">
          Share the page URL to invite new friends
        </div>

        <div class="card-body">
          <div class="container chat-body">
            <div class="row chat-section">
              <div class="col-sm-2">
                <div class="circle-icon rounded-circle">D</div>
              </div>
              <div class="col-sm-7">
                <span class="card-text speech-bubble speech-bubble-peer">Hello!</span>
              </div>
            </div>
            <div class="row chat-section">
              <div class="col-sm-7 offset-md-3">
                <span class="card-text speech-bubble speech-bubble-user float-end text-white subtle-blue-gradient">
                  Whatsup, another chat app?
                </span>
              </div>
              <div class="col-sm-2">
                <div class="circle-icon rounded-circle">A</div>
              </div>
            </div>
            <div class="row chat-section">
              <div class="col-sm-2">
                <div class="circle-icon rounded-circle">D</div>
              </div>
              <div class="col-sm-7">
                <p class="card-text speech-bubble speech-bubble-peer">
                  Yes this is Chatire, it's pretty cool and it's Open source
                  and it was built with Django and Vue JS so we can tweak it to our satisfaction.
                </p>
              </div>
            </div>
            <div class="row chat-section">
              <div class="col-sm-7 offset-md-3">
                <p class="card-text speech-bubble speech-bubble-user float-end text-white subtle-blue-gradient">
                  Okay i'm already hacking around let me see what i can do to this thing.
                </p>
              </div>
              <div class="col-sm-2">
                <div class="circle-icon rounded-circle">A</div>
              </div>
            </div>
            <div class="row chat-section">
              <div class="col-sm-7 offset-md-3">
                <p class="card-text speech-bubble speech-bubble-user float-end text-white subtle-blue-gradient">
                  We should invite james to see this.
                </p>
              </div>
              <div class="col-sm-2">
                <div class="circle-icon rounded-circle">A</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer text-muted">
          <form>
            <div class="row">
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="Type a message" />
              </div>
              <div class="col-sm-2">
                <button class="btn btn-primary">Send</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <div v-else>
        <h3 class="text-center">Welcome !</h3>

        <br />

        <p class="text-center">
          To start chatting with friends click on the button below, it'll start a new chat session
          and then you can invite your friends over to chat!
        </p>

        <br />

        <button @click="startChatSession" class="btn btn-primary btn-lg w-100">Start Chatting</button>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ChatComponent',
  data() {
    return {
      sessionStarted: false,
      username: ''
    }
  },

  created() {
    this.username = sessionStorage.getItem('username') || '';
  },

  methods: {
    startChatSession() {
      this.sessionStarted = true
      this.$router.push('/chats/chat_url/')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

.btn {
  border-radius: var(--bs-btn-border-radius) !important;
}



.card-header a {
  text-decoration: underline;
}

.card-body {
  background-color: #ddd;
}

.chat-body {
  margin-top: -15px;
  margin-bottom: -5px;
  height: 380px;
  overflow-y: auto;
}

.speech-bubble {
  display: inline-block;
  position: relative;
  border-radius: 0.4em;
  padding: 10px;
  background-color: #fff;
  font-size: 14px;
}

.subtle-blue-gradient {
  background: linear-gradient(45deg, #004bff, #007bff);
}

.speech-bubble-user:after {
  content: "";
  position: absolute;
  right: 4px;
  top: 10px;
  width: 0;
  height: 0;
  border: 20px solid transparent;
  border-left-color: #007bff;
  border-right: 0;
  border-top: 0;
  margin-top: -10px;
  margin-right: -20px;
}

.speech-bubble-peer:after {
  content: "";
  position: absolute;
  left: 3px;
  top: 10px;
  width: 0;
  height: 0;
  border: 20px solid transparent;
  border-right-color: #ffffff;
  border-top: 0;
  border-left: 0;
  margin-top: -10px;
  margin-left: -20px;
}

.chat-section:first-child {
  margin-top: 10px;
}

.chat-section {
  margin-top: 15px;
}

.send-section {
  margin-bottom: -20px;
  padding-bottom: 10px;
}

.circle-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f16000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 20px;
}
</style>
