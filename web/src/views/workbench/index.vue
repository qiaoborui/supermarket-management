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
    <div v-if="!isSuperAdmin">
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
  <div v-if="isSuperAdmin">
    <n-date-picker v-model:value="range" type="daterange" clearable style="max-width: 300px;" />
    <div class="flex flex-wrap justify-between items-start gap-4">
  <n-card style="flex: 1 1 calc(33.33% - 16px); max-width: calc(33.33% - 16px);">
    <div id="memberChart" style="width: 100%; height: 400px;"></div> 
  </n-card>
  <n-card style="flex: 1 1 calc(33.33% - 16px); max-width: calc(33.33% - 16px);">
    <div id="amountChart" style="width: 100%; height: 400px;"></div>
  </n-card>
  <n-card style="flex: 1 1 calc(33.33% - 16px); max-width: calc(33.33% - 16px);">
    <div id="discountChart" style="width: 100%; height: 400px;"></div>
  </n-card>
</div>
  </div>
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
  <n-modal v-model:show="showModifyModal" aria-modal="true" role="dialog">
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
      </n-form>
      <template #footer>
        <n-button block size="large" type="primary" @click="updateForm">
          确认更新
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
import { ref,watch } from 'vue'
import { NModal, NForm, NFormItem, NInput, NButton, NCheckbox,NCard, useMessage } from 'naive-ui'
import * as echarts from 'echarts';
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
// 计算一周前的时间
const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)

const range = ref([oneWeekAgo, Date.now()])

let start_time = ref(convertDate(range.value[0],true))
let end_time = ref(convertDate(range.value[1],false))
// 监听 range 的变化
watch(range, async (newRange) => {
  console.log('newRange:', newRange)
  start_time.value = convertDate(newRange[0],true)
  end_time.value = convertDate(newRange[1],false)
  console.log('start_time:', start_time)
  console.log('end_time:', end_time)
  await renderDicountChart()
  await renderLineChart()

})

function convertDate(time, isStart) {
  //convert timestamp to 2024-06-17 00:00:00.000000
  const date = new Date(time)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = isStart ? '00' : '23'
  const minutes = isStart ? '00' : '59'
  const seconds = isStart ? '00' : '59'
  const milliseconds = isStart ? '000' : '999'
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`
}

const isSuperAdmin = ref(false)
const message = useMessage()
const showButton = ref(true)
const user_id = ref('')
const member_list = ref([])
const is_member = ref(false)
onMounted(() => {
  renderPieChart()
  renderLineChart()
  renderDicountChart()
  user_id.value = userStore.userId
  isSuperAdmin.value = userStore.userInfo.is_superuser
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
const showModifyModal = ref(false)
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
    location.reload()
  })
  showModal.value = false
  // 刷新页面
}
async function editInfo() {
  showModifyModal.value = true
  // 首先获取之前的用户信息
  const resp = await api.getMembers({ user_id: user_id.value })
  console.log('resp:', resp)
  member_list.value = resp.data
  // 将表单中的信息填充到结构中用于更新
  name.value = member_list.value[0].realname
  phone.value = member_list.value[0].phone
  idCard.value = member_list.value[0].personal_id
  address.value = member_list.value[0].address
}
async function updateForm() {
  const resp = await api.getMembers({ user_id: user_id.value })
  member_list.value = resp.data
  // 将表单中的信息填充到结构中用于更新
  member_list.value[0].realname = name.value
  member_list.value[0].phone = phone.value
  member_list.value[0].personal_id = idCard.value
  member_list.value[0].address = address.value
  console.log('member_list:', member_list.value)
  api.updateMember(member_list.value[0]).then((res) => {
    message.success('更新成功')
    showButton.value = false
    closeModal()
  })
  showModifyModal.value = false
  // 刷新页面
  location.reload()
}
async function renderPieChart() {
  const member = await api.getMemberLevelStatistics()
  const chart = echarts.init(document.getElementById('memberChart'))
  const discount_levels = member.data.map((item) => item.level)
  const member_count = member.data.map((item) => item.count)
  const option = {
    title: {
      text: '会员等级统计',
    },
    tooltip: {},
    legend: {
      orient: 'horizontal',
      bottom: '0',
      data: discount_levels,
    },
    series: [
      {
        name: '会员数量',
        type: 'pie',
        radius: '50%',
        data: member_count.map((count, index) => ({
          value: count,
          name: discount_levels[index],
        })),
      },
    ],
  }
  chart.setOption(option);

}
async function renderDicountChart(){
  console.log('start_time:', start_time.value)
  const data = await api.getDiscountStatistics({start_time: start_time.value, end_time: end_time.value})
  const chart = echarts.init(document.getElementById('discountChart'))
  const date = data.data.map((item) => item.date)
  const discount = data.data.map((item) => item.total_amount)
  console.log('date:', date)
  console.log('discount:', discount)
  const option = {
    title: {
      text: '折扣统计',
    },
    tooltip: {},
    xAxis: {
      type: 'category',
      data: date,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: discount,
        type: 'line',
      },
    ],
  }
  chart.setOption(option);
}
async function renderLineChart(){
  const data = await api.getConsumptionStatistics({start_time: start_time.value, end_time: end_time.value})
  const chart = echarts.init(document.getElementById('amountChart'))
  const date = data.data.map((item) => item.date)
  const amount = data.data.map((item) => item.total_amount)
  const option = {
    title: {
      text: '消费金额统计',
    },
    tooltip: {},
    xAxis: {
      type: 'category',
      data: date,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: amount,
        type: 'line',
      },
    ],
  }
  chart.setOption(option);
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