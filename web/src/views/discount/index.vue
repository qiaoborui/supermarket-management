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

defineOptions({ name: '优惠等级管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

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
  name: '优惠等级',
  initForm: {},
  doCreate: api.createDiscountLevel,
  doDelete: api.deleteDiscountLevel,
  doUpdate: api.updateDiscountLevel,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

const columns = [
  {
    title: '优惠等级',
    key: 'name',
    width: 80,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '优惠比例',
    key: 'discount',
    width: 80,
    align: 'center',
  }, 
  {
    title: '所需积分',
    key: 'points_required',
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
          [[vPermission, 'post/api/v1/discount_level/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ discount_level_id: row.id }, false),
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
                [[vPermission, 'delete/api/v1/discount_level/delete']]
              ),
            default: () => h('div', {}, '确定删除该等级吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="等级列表">
    <template #action>
      <NButton v-permission="'post/api/v1/discount_level/create'" type="primary" @click="handleAdd"> 
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建优惠等级
      </NButton>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getDiscountLevels"
    >
      <template #queryBar>
        <QueryBarItem label="优惠等级" :label-width="50">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入优惠等级"
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
          label="优惠等级"
          path="name"
          :rule="{
            required: true,
            message: '请输入优惠等级',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.name" placeholder="请输入优惠等级" />
        </NFormItem>
        <NFormItem label="优惠比例" path="discount"
            :rule="{
                required: true,
                message: '请输入优惠比例',
                trigger: ['input', 'blur'],
            }"
        >
          <NInput v-model:value="modalForm.discount" placeholder="请输入优惠比例" />
        </NFormItem>

        <NFormItem label="所需积分" path="points_required"
            :rule="{
                required: true,
                message: '请输入所需积分',
                trigger: ['input', 'blur'],
            }"
        >
            <NInput v-model:value="modalForm.points_required" placeholder="请输入所需积分" />
        </NFormItem>
        
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
