<template>
  <div class="d-flex justify-content-center">
    <div class="" style="width: 600px;">
      <div v-if="sessionStarted" id="chat-container" class="card">
        <div class="card-header text-white text-center fw-bold subtle-blue-gradient">
          Share the page URL to invite new friends
        </div>

        <div class="card-body">
          <div class="d-flex flex-column">
            <div v-for="(message, index) in messages" :key="index" class="d-flex my-1"
              :class="message.user.username === username ? 'justify-content-end' : 'justify-content-start'">
              <div v-if="message.user.username !== username" class="">
                <div class="circle-icon rounded-circle">{{ message.user.username.charAt(0).toUpperCase() }}</div>
              </div>
              <div class="flex-fill"
                :class="message.user.username === username ? 'd-flex justify-content-end' : 'd-flex justify-content-start'">
                <span class="mx-3"
                  :class="{ 'card-text': true, 'speech-bubble': true, 'speech-bubble-user': message.user.username === username, 'speech-bubble-peer': message.user.username !== username, 'text-white': message.user.username === username, 'subtle-blue-gradient': message.user.username === username }">
                  {{ message.message }}
                </span>
              </div>
              <div v-if="message.user.username === username" class="">
                <div class="circle-icon rounded-circle">{{ message.user.username.charAt(0).toUpperCase() }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer text-muted">
          <form @submit.prevent="postMessage">
            <div class="row">
              <div class="col-sm-10">
                <input v-model="message" class="form-control" type="text" placeholder="Type a message" />
              </div>
              <div class="col-sm-2">
                <button class="btn btn-primary">Send</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <div v-else class="card border-0">
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
      username: '',
      messages: [] as Array<{ user: { username: string }, message: string }>,
      message: ''
    }
  },

  created() {
    this.username = sessionStorage.getItem('username') || '';

    if (this.$route.params.uri) {
      this.joinChatSession()
    }
  },

  methods: {
    async startChatSession() {
      try {
        const response = await fetch('http://localhost:8000/api/chats/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${sessionStorage.getItem('authToken')}`
          }
        });

        if (response.ok) {
          const data = await response.json();

          this.sessionStarted = true;
          this.$router.push(`/chats/${data.uri}/`);
        } else {
          const errorText = await response.text();
          alert(errorText);
        }
      } catch (error) {
        console.error('Error starting chat session:', error);
        alert('Failed to start chat session. Please try again.');
      }
    },

    async postMessage() {
      const data = { message: this.message };

      try {
        const response = await fetch(`http://localhost:8000/api/chats/${this.$route.params.uri}/messages/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${sessionStorage.getItem('authToken')}`
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          const responseData = await response.json();
          this.messages.push(responseData);
          this.message = ''; // clear the message after sending
        } else {
          const errorText = await response.text();
          alert(errorText);
        }
      } catch (error) {
        console.error('Error posting message:', error);
        alert('Failed to post message. Please try again.');
      }
    },

    async joinChatSession() {
      const uri = this.$route.params.uri;

      try {
        const response = await fetch(`http://localhost:8000/api/chats/${uri}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${sessionStorage.getItem('authToken')}`
          },
          body: JSON.stringify({ username: this.username })
        });

        if (response.ok) {
          const data = await response.json();
          const user = data.members.find((member: { username: string }) => member.username === this.username);

          if (user) {
            this.sessionStarted = true;
            this.fetchChatSessionHistory();
          }
        } else {
          const errorText = await response.text();
          alert(errorText);
        }
      } catch (error) {
        console.error('Error joining chat session:', error);
        alert('Failed to join chat session. Please try again.');
      }
    },

    async fetchChatSessionHistory() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/chats/${this.$route.params.uri}/messages/`, {
          headers: {
            'Authorization': `Token ${sessionStorage.getItem('authToken')}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.messages = data.messages;
        } else {
          const errorText = await response.text();
          alert(errorText);
        }
      } catch (error) {
        console.error('Error fetching chat session history:', error);
        alert('Failed to fetch chat session history. Please try again.');
      }
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
