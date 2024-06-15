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
  $table.value?.handleSearch()
  const resp = await api.getDiscountLevels()
  discount_levels.value = resp.data
  console.log('discount_levels:', discount_levels.value) 
  const resp2 = await api.getMembers()
  memberList.value = resp2.data
  console.log('memberList:', memberList.value)
  const resp3 = await api.getUserList()
  userList.value = resp3.data
})


watch(
  modalForm,
  (newVal, oldVal) => {
    console.log('modalForm changed:', newVal, oldVal);
    if (newVal.member_id) {
      let member_id = modalForm.value.member_id;
      console.log('member_id:', member_id);
      let member = memberList.value.find((item) => item.id === member_id);
      console.log('member:', member);
      if (member) {
        discount_level = discount_levels.value.find((item) => item.id === member.discount_level_id);
        if (discount_level) {
          modalForm.value.discount_level_id = discount_level.id;
          modalForm.value.actual_amount_spent = newVal.amount_spent * discount_level.discount;
        }
      }
    }
  },
  { deep: true }
);

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
    <template #action>
      <NButton v-permission="'post/api/v1/member/create'" type="primary" @click="handleAdd"> 
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建消费记录
      </NButton>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getConsumptions"
    >
      <template #queryBar>
        <QueryBarItem label="会员" :label-width="50">
          <NInput
            v-model:value="queryItems.member_name"
            clearable
            type="text"
            placeholder="请输入会员姓名"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :disabled="modalAction === 'view'"
      >
        <NFormItem label="会员" path="member_id">
          <NTreeSelect
            v-model:value="modalForm.member_id"
            :options="memberList"
            key-field="id"
            filterable
            label-field="realname"
            placeholder="请选择用户"
            clearable
            default-expand-all
          ></NTreeSelect>
        </NFormItem> 
        <NFormItem
          label="消费金额"
          path="amount_spent"
          :rule="{
            required: true,
            message: '请输入消费金额',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.amount_spent" placeholder="请输入消费金额" type="number" />
        </NFormItem>
        <NFormItem
          label="实际消费金额"
          path="actual_amount_spent"
          aria-disabled="true"
        >
          <NInput v-model:value="modalForm.actual_amount_spent" placeholder="请输入实际消费金额" type="number" />
        </NFormItem>
        <NFormItem
          label="折扣等级"
          path="discount_level_id"
          aria-disabled="true"
        >
          <NInput v-model:value="modalForm.discount_level_id" placeholder="请输入会员等级" type="number" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
