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
onMounted(() => {
  $table.value?.handleSearch()
})

const columns = [
  {
    title: 'ID',
    key: 'id',
    width: 30,
    align: 'center',
    ellipsis: { tooltip: true },
  },
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
  <CommonPage show-footer title="消费记录">
    <template #action>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getPointTransactions"
    >
      <template #queryBar>
        <QueryBarItem label="会员" :label-width="50">
          <NInput
            v-model:value="queryItems.realname"
            clearable
            type="text"
            placeholder="请输入会员姓名"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="手机号" :label-width="50">
          <NInput
            v-model:value="queryItems.phone"
            clearable
            type="text"
            placeholder="请输入手机号"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>
