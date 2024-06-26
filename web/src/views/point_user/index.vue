<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives,watch } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NPopconfirm,
  NTag,
  NTree,
  NDrawer,
  NDrawerContent,
  NTabs,
  NTabPane,
  NGrid,
  NGi,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useUserStore } from '@/store'

defineOptions({ name: '积分变动记录' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')
const discount_levels = ref([])
const userList = ref([])
const memberList = ref([])
let discount_level = ref('')
const {
  modalVisible,
  modalAction,
  modalTitle,
  modalLoading,
  handleAdd,
  handleDelete,
  handleEdit,
  handleSave,
  modalForm,
  modalFormRef,
} = useCRUD({
  name: '积分记录',
  initForm: {},
  refresh: () => $table.value?.handleSearch(),
})
const userStore = useUserStore()
onMounted(async () => {
  const userId = userStore.userId
  const members = await api.getMembers({ 
    user_id: userId,
    page: 1,
    page_size: 10000,
   })
  console.log(members)
  if (members) {
    queryItems.value.realname = members.data[0].realname
  }
  console.log('queryItems:', queryItems)
  $table.value?.handleSearch()
})

const columns = [
  {
    title: '真实姓名',
    key: 'realname',
    width: 80,
    align: 'center',
  }, 
  {
    title: '积分变动',
    key: 'points_changed',
    width: 90,
    align: 'center',
  },
  {
    title: '积分变动类型',
    key: 'transaction_type',
    width: 80,
    align: 'center',
  },
  {
    title: '手机号',
    key: 'phone',
    width: 80,
    align: 'center',
  },

  {
    title: '创建日期',
    key: 'created_at',
    width: 60,
    align: 'center',
    render(row) {
      return h('span', formatDate(row.created_at))
    },
  },
  {
    title: '更新日期',
    key: 'updated_at',
    width: 60,
    align: 'center',
    render(row) {
      return h('span', formatDate(row.updated_at))
    },
  }
]
</script>

<template>
  <CommonPage show-footer title="积分记录">
    <template #action>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getPointTransactions"
    >
    </CrudTable>
  </CommonPage>
</template>
