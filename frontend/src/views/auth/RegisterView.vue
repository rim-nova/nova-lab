<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h1 class="text-center text-4xl font-extrabold text-gray-900">
          Create Account
        </h1>
        <p class="mt-2 text-center text-sm text-gray-600">
          Join InfinityInsight today
        </p>
      </div>

      <div class="card">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <input
              v-model="form.full_name"
              type="text"
              required
              class="input-field mt-1"
              placeholder="John Doe"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <input
              v-model="form.username"
              type="text"
              required
              class="input-field mt-1"
              placeholder="johndoe"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              v-model="form.email"
              type="email"
              required
              class="input-field mt-1"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              v-model="form.password"
              type="password"
              required
              class="input-field mt-1"
              placeholder="••••••••"
            />
            <p class="mt-1 text-xs text-gray-500">
              Must be at least 8 characters with uppercase, lowercase, and numbers
            </p>
          </div>

          <div v-if="error" class="text-red-600 text-sm">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary"
          >
            {{ loading ? 'Creating account...' : 'Register' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <router-link to="/login" class="text-primary-600 hover:text-primary-500">
            Already have an account? Sign in
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  full_name: '',
  username: '',
  email: '',
  password: '',
  role: 'analyst'
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''

  try {
    await authStore.register(form.value)
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
