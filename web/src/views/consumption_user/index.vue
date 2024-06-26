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

defineOptions({ name: '消费记录管理' })

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
  name: '消费记录',
  initForm: {},
  doCreate: api. createConsumption,
  doDelete: api.deleteConsumption,
  doUpdate: api.updateConsumption,
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
    queryItems.value.member_name = members.data[0].realname
  }
  console.log('queryItems:', queryItems)
  $table.value?.handleSearch()
})


const columns = [
  {
    title: '真实姓名',
    key: 'member_name',
    width: 80,
    align: 'center',
  }, 
  {
    title: '会员等级',
    key: 'discount_level_name',
    width: 90,
    align: 'center',
  },
  {
    title: '消费金额',
    key: 'amount_spent',
    width: 80,
    align: 'center',
  },
  {
    title: '实际消费金额',
    key: 'actual_amount_spent',
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
  },
  {
    title: '操作',
    key: 'actions',
    width: 80,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEdit(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit-outline', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/consumption_record/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ member_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                    style: 'margin-right: 8px;',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/consumption_record/delete']]
              ),
            default: () => h('div', {}, '确定删除该消费记录吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="消费记录">
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getConsumptions"
    >
    </CrudTable>
  </CommonPage>
</template>
