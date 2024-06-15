<template>
  <AppPage :show-footer="false">
    <div flex-1>
      <n-card rounded-10>
        <div flex items-center justify-between>
          <div flex items-center>
            <img rounded-full width="60" :src="userStore.avatar" />
            <div ml-10>
              <p text-20 font-semibold>
                {{ $t('views.workbench.text_hello', { username: userInfo.name ?? (userInfo.name || userStore.name) }) }}
              </p>
              <p mt-5 text-14 op-60>{{ $t('views.workbench.text_welcome') }}</p>
            </div>
          </div>
          <n-space :size="12" :wrap="false">
            <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
          </n-space>
        </div>
      </n-card>
    <div>
      <n-card v-if="is_member" title="个人信息" style="max-width: 500px;" bordered hoverable :segmented="{ content: 'soft' }">
    <div class="info-item">
      <strong>真实姓名：</strong>{{ userInfo.name }}
    </div>
    <div class="info-item">
      <strong>积分：</strong>{{ userInfo.points }}
    </div>
    <div class="info-item">
      <strong>手机号：</strong>{{ userInfo.phone }}
    </div>
    <div class="info-item">
      <strong>身份证号：</strong>{{ userInfo.idCard }}
    </div>
    <div class="info-item">
      <strong>住址：</strong>{{ userInfo.address }}
    </div>
    <n-button block size="large" type="info" @click="editInfo">
      修改信息
    </n-button>
  </n-card>
  </div>
      <!-- <n-card
        :title="$t('views.workbench.label_project')"
        size="small"
        :segmented="true"
        mt-15
        rounded-10
      >
        <template #header-extra>
          <n-button text type="primary">{{ $t('views.workbench.label_more') }}</n-button>
        </template>
        <div flex flex-wrap justify-between>
          <n-card
            v-for="i in 9"
            :key="i"
            class="mb-10 mt-10 w-300 cursor-pointer"
            hover:card-shadow
            title="Vue FastAPI Admin"
            size="small"
          >
            <p op-60>{{ dummyText }}</p>
          </n-card>
        </div>
      </n-card> -->
  <div class="mx-auto w-full max-w-md">
    <n-button v-if="showButton" @click="showModal = true" type="primary">
      点击进行实名注册
    </n-button>
  </div>
  <n-modal v-model:show="showModal" aria-modal="true" role="dialog">
    <n-card style="width: 600px" title="认证信息" bordered="false" size="huge">
      <template #header-extra>
        请输入您的认证信息
      </template>
      <n-form>
        <n-form-item label="真实姓名">
          <n-input v-model:value="name" placeholder="请输入您的真实姓名" />
        </n-form-item>
        <n-form-item label="手机号">
          <n-input v-model:value="phone" placeholder="请输入您的手机号" />
        </n-form-item>
        <n-form-item label="身份证号">
          <n-input v-model:value="idCard" placeholder="请输入您的身份证号" />
        </n-form-item>
        <n-form-item label="住址">
          <n-input v-model:value="address" placeholder="请输入您的住址" />
        </n-form-item>
        <n-form-item>
          <n-checkbox v-model:checked="agree">我已阅读并同意隐私协议</n-checkbox>
        </n-form-item>
      </n-form>
      <p>Agree value: {{ agree }}</p>
      <template #footer>
        <n-button block size="large" type="primary" @click="submitForm">
          确认认证
        </n-button>
      </template>
    </n-card>
  </n-modal>
  </div>

  </AppPage>
</template>

<script setup>
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
import { NModal, NForm, NFormItem, NInput, NButton, NCheckbox,NCard, useMessage } from 'naive-ui'
const dummyText = '一个基于 Vue3.0、FastAPI、Naive UI 的轻量级后台管理模板'
const { t } = useI18n({ useScope: 'global' })
import api from '~/src/api';
import { is } from '~/src/utils';
const userInfo = ref({
  name: '',
  phone: '',
  idCard: '',
  address: '',
  points: 0,
})



const message = useMessage()
const showButton = ref(true)
const user_id = ref('')
const member_list = ref([])
const is_member = ref(false)
onMounted(() => {
  user_id.value = userStore.userId
  api.getMembers({ user_id: user_id.value }).then((res) => {
    member_list.value = res.data
    // 查看 member里有没有 user_id
    if (member_list.value.length > 0) {
      showButton.value = false
      is_member.value = true
    }
  }).then(() => {
    api.getMembers({ user_id: user_id.value }).then((res) => {
      member_list.value = res.data
      // 查看 member里有没有 user_id
      if (member_list.value.length > 0) {
        userInfo.value.name = member_list.value[0].realname
        userInfo.value.phone = member_list.value[0].phone
        userInfo.value.idCard = member_list.value[0].personal_id
        userInfo.value.address = member_list.value[0].address
        userInfo.value.points = member_list.value[0].points
      }
  })
})
})
const showModal = ref(false)
const name = ref('')
const phone = ref('')
const idCard = ref('')
const address = ref('')
const agree = ref(false)
const discount_levels = ref([])
async function submitForm() {
  if (!agree) {
    message.error('请先同意隐私协议')
    return
  }
  const resp = await api.getDiscountLevels()
  discount_levels.value = resp.data
  // 从 discount_levels 中找到最低的 discount_level
  const discount_level = discount_levels.value.reduce((prev, current) => {
    return prev.points_required < current.points_required ? prev : current
  })
  api.createMember({ user_id: user_id.value, realname: name.value, phone: phone.value, personal_id: idCard.value, address: address.value, discount_level_id: discount_level.id }).then((res) => {
    message.success('认证成功')
    showButton.value = false
    closeModal()
  })
  showModal.value = false
  // 刷新页面
  location.reload()
}
const userStore = useUserStore()
</script>
<style scoped>
.info-item {
  margin-bottom: 20px; /* 增加了较大的底部边距来提高每项之间的视觉间隔 */
  font-size: 16px;
  line-height: 1.5;
}
</style>