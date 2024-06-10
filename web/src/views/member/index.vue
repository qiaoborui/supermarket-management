<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
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

defineOptions({ name: '会员管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')
const discount_levels = ref([])
const user_ids = ref([])

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
  name: '会员',
  initForm: {},
  doCreate: api.createMember,
  doDelete: api.deleteMember,
  doUpdate: api.updateMember,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
  api.getDiscountLevels().then((res) => {
    discount_levels.value = res.data
  })
  api.getUserList().then((res) => {
    user_ids.value = res.data
  })
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
    title: '手机号',
    key: 'phone',
    width: 90,
    align: 'center',
  },
  {
    title: '身份证号',
    key: 'personal_id',
    width: 160,
    align: 'center',
  },
  {
    title: '住址',
    key: 'address',
    width: 80,
    align: 'center',
  },
  {
    title: '积分',
    key: 'points',
    width: 80,
    align: 'center',
  },
  {
    title: '等级',
    key: 'discount_level_name',
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
          [[vPermission, 'post/api/v1/member/update']]
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
                [[vPermission, 'delete/api/v1/member/delete']]
              ),
            default: () => h('div', {}, '确定删除该会员吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="会员列表">
    <template #action>
      <NButton v-permission="'post/api/v1/member/create'" type="primary" @click="handleAdd"> 
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建会员
      </NButton>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getMembers"
    >
      <template #queryBar>
        <QueryBarItem label="会员" :label-width="50">
          <NInput
            v-model:value="queryItems.name"
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
        <NFormItem
          label="真实姓名"
          path="realname"
          :rule="{
            required: true,
            message: '请输入真实姓名',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.realname" placeholder="请输入真实姓名" />
        </NFormItem>
        <NFormItem
          label="手机号"
          path="phone"
          :rule="{
            required: true,
            message: '请输入手机号',
            trigger: ['input', 'blur'],
          }"  
        >
          <NInput v-model:value="modalForm.phone" placeholder="请输入手机号" />
        </NFormItem>
        <NFormItem
          label="身份证号"
          path="personal_id"
          :rule="{
            required: true,
            message: '请输入身份证号',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.personal_id" placeholder="请输入身份证号" />
        </NFormItem>
        <NFormItem
          label="住址"
          path="address"
          :rule="{
            required: true,
            message: '请输入住址',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.address" placeholder="请输入住址" />
        </NFormItem>
        <NFormItem
          label="积分"
          path="points"
          :rule="{
            required: true,
            message: '请输入积分',
            trigger: ['input', 'blur'],
          }"
        > 
          <NInput v-model:value="modalForm.points" placeholder="请输入积分" />
        </NFormItem>
        <NFormItem label="等级" path="discount_level_id">
          <NTreeSelect
            v-model:value="modalForm.discount_level_id"
            :options="discount_levels"
            key-field="id"
            label-field="name"
            placeholder="请选择等级"
            clearable
            default-expand-all
          ></NTreeSelect>
        </NFormItem>   
        <NFormItem label="用户" path="user_id">
          <NTreeSelect
            v-model:value="modalForm.user_id"
            :options="user_ids"
            key-field="id"
            filterable
            label-field="username"
            placeholder="请选择用户"
            clearable
            default-expand-all
          ></NTreeSelect>
        </NFormItem> 
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
