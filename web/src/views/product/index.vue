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

defineOptions({ name: '商品管理' })

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
  name: '商品',
  initForm: {
    // stock: 0,
    // price: 0,
  },
  doCreate: api.createProduct,
  doDelete: api.deleteProduct,
  doUpdate: api.updateProduct,
  refresh: () => $table.value?.handleSearch(),
})

const supplierOptions = ref([])

onMounted(() => {
  $table.value?.handleSearch()
  api.getSuppliersList().then((res) => {
    supplierOptions.value = res.data
  })
})

const columns = [
  {
    title: '名称',
    key: 'name',
    width: 80,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '描述',
    key: 'description',
    width: 80,
    align: 'center',
  },
  {
    title: '价格',
    key: 'price',
    width: 80,
    align: 'center',
  },
  {
    title: '库存',
    key: 'stock',
    width: 80,
    align: 'center',
  },
  {
    title: '备注',
    key: 'remark',
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
          [[vPermission, 'post/api/v1/product/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ product_id: row.id }, false),
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
                [[vPermission, 'delete/api/v1/product/delete']]
              ),
            default: () => h('div', {}, '确定删除该角色吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="商品列表">
    <template #action>
      <NButton v-permission="'post/api/v1/product/create'" type="primary" @click="handleAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建商品
      </NButton>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getProductsList"
    >
      <template #queryBar>
        <QueryBarItem label="商品名" :label-width="50">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入商品名"
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
          label="商品名"
          path="name"
          :rule="{
            required: true,
            message: '请输入商品名',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.name" placeholder="请输入商品名" />
        </NFormItem>
        <NFormItem label="描述" path="description">
          <NInput v-model:value="modalForm.description" placeholder="请输入描述" />
        </NFormItem>
        <NFormItem label="价格" path="price">
          <NInput v-model:value="modalForm.price" placeholder="请输入价格" type="number" />
        </NFormItem>
        <NFormItem label="库存" path="stock">
          <NInput v-model:value="modalForm.stock" placeholder="请输入库存" type="number" />
        </NFormItem>
        <NFormItem label="供应商" path="supplier_id">
              <NTreeSelect
                v-model:value="modalForm.supplier_id"
                :options="supplierOptions"
                key-field="id"
                label-field="name"
                placeholder="请选择供应商"
                clearable
                default-expand-all
              ></NTreeSelect>
            </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput v-model:value="modalForm.remark" placeholder="请输入备注" />
        </NFormItem>
        
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
