<template>
  <AppPage :show-footer="true" bg-cover :style="{ backgroundImage: `url(${bgImg})` }">
    <div
      style="transform: translateY(25px)"
      class="m-auto max-w-1500 min-w-345 f-c-c rounded-10 bg-white bg-opacity-60 p-15 card-shadow"
      dark:bg-dark
    >
      <div hidden w-380 px-20 py-35 md:block>
        <icon-custom-front-page pt-10 text-300 color-primary></icon-custom-front-page>
      </div>

      <div w-320 flex-col px-20 py-35>
        <h5 f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-logo mr-10 text-50 color-primary /> 注册
        </h5>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="请输入用户名"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.email"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="请输入邮箱"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="registerInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="请输入密码"
            :maxlength="20"
            @keypress.enter="handleSignup"
          />
        </div>
        <div mt-20>
          <n-button
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleSignup"
          >
            注册
          </n-button>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import bgImg from '@/assets/images/login_bg.webp'
import api from '@/api'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { query } = useRoute()
const { t } = useI18n({ useScope: 'global' })

const registerInfo = ref({
  username: '',
  email: '',
  password: '',
})

const loading = ref(false)
async function handleSignup() {
  const { username, password,email } = registerInfo.value
  if (!username || !password || !email) {
    $message.warning(t('views.login.message_input_username_password'))
    return
  }
  try {
    loading.value = true
    $message.loading("注册中")
    const res = await api.signup({
      username: username,
      password: password.toString(),
      email: email
    })
    console.log(res)
    if (res.code === 200) {
      $message.success('注册成功')
    } else {
      $message.error(res.msg)
    }
    router.push({ path: '/login' })
  } catch (e) {
    console.error('login error', e.error)
  }
  loading.value = false
}
</script>
