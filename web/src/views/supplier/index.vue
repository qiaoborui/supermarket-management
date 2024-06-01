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

defineOptions({ name: '角色管理' })

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
  name: '供应商',
  initForm: {},
  doCreate: api.createSupplier,
  doDelete: api.deleteSupplier,
  doUpdate: api.updateSupplier,
  refresh: () => $table.value?.handleSearch(),
})

const pattern = ref('')
const menuOption = ref([]) // 菜单选项
const active = ref(false)
const menu_ids = ref([])
const role_id = ref(0)
const apiOption = ref([])
const api_ids = ref([])
const apiTree = ref([])

function buildApiTree(data) {
  const processedData = []
  const groupedData = {}

  data.forEach((item) => {
    const tags = item['tags']
    const pathParts = item['path'].split('/')
    const path = pathParts.slice(0, -1).join('/')
    const summary = tags.charAt(0).toUpperCase() + tags.slice(1)
    const unique_id = item['method'].toLowerCase() + item['path']
    if (!(path in groupedData)) {
      groupedData[path] = { unique_id: path, path: path, summary: summary, children: [] }
    }

    groupedData[path].children.push({
      id: item['id'],
      path: item['path'],
      method: item['method'],
      summary: item['summary'],
      unique_id: unique_id,
    })
  })
  processedData.push(...Object.values(groupedData))
  return processedData
}

onMounted(() => {
  $table.value?.handleSearch()
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
    title: '手机号',
    key: 'phone',
    width: 80,
    align: 'center',
  },
  {
    title: '邮箱',
    key: 'email',
    width: 80,
    align: 'center',
  },
  {
    title: '邮箱',
    key: 'email',
    width: 80,
    align: 'center',
  },
  {
    title: '地址',
    key: ' address',
    width: 80,
    align: 'center',
  },
  {
    title: '备注',
    key: ' remark',
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
          [[vPermission, 'post/api/v1/supplier/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ role_id: row.id }, false),
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
                [[vPermission, 'delete/api/v1/supplier/delete']]
              ),
            default: () => h('div', {}, '确定删除该角色吗?'),
          }
        ),
      ]
    },
  },
]

async function updateRoleAuthorized() {
  const checkData = apiTree.value.getCheckedData()
  const apiInfos = []
  checkData &&
    checkData.options.forEach((item) => {
      if (!item.children) {
        apiInfos.push({
          path: item.path,
          method: item.method,
        })
      }
    })
  const { code, msg } = await api.updateRoleAuthorized({
    id: role_id.value,
    menu_ids: menu_ids.value,
    api_infos: apiInfos,
  })
  if (code === 200) {
    $message?.success('设置成功')
  } else {
    $message?.error(msg)
  }

  const result = await api.getRoleAuthorized({ id: role_id.value })
  menu_ids.value = result.data.menus.map((v) => {
    return v.id
  })
}
</script>

<template>
  <CommonPage show-footer title="供应商列表">
    <template #action>
      <NButton v-permission="'post/api/v1/role/create'" type="primary" @click="handleAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建供应商
      </NButton>
    </template>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getSuppliersList"
    >
      <template #queryBar>
        <QueryBarItem label="供应商名" :label-width="50">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入供应商名"
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
          label="供应商名"
          path="name"
          :rule="{
            required: true,
            message: '请输入供应商名',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.name" placeholder="请输入供应商名" />
        </NFormItem>
        <NFormItem label="手机号" path="phone">
          <NInput v-model:value="modalForm.phone" placeholder="请输入手机号" />
        </NFormItem>
        <NFormItem label="邮箱" path="email">
          <NInput v-model:value="modalForm.email" placeholder="请输入邮箱" />
        </NFormItem>
        <NFormItem label="地址" path="address">
          <NInput v-model:value="modalForm.address" placeholder="请输入地址" />
        </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput v-model:value="modalForm.remark" placeholder="请输入备注" />
        </NFormItem>
        
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
