<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import {
  NButton,
  NCheckbox,
  NCheckboxGroup,
  NForm,
  NFormItem,
  NImage,
  NInput,
  NSpace,
  NSwitch,
  NTag,
  NPopconfirm,
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NTreeSelect,
  NUpload,
  useMessage,
} from 'naive-ui'

const message = useMessage();

const handleSuccess = (response, file) => {
  message.success(`文件上传成功: ${file.name}`);
};

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate, renderIcon, getToken } from '@/utils'
import { useCRUD } from '@/composables'
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useUserStore } from '@/store'

defineOptions({ name: '用户管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '用户',
  initForm: {},
  doCreate: api.createUser,
  doUpdate: api.updateUser,
  doDelete: api.deleteUser,
  refresh: () => $table.value?.handleSearch(),
})

const roleOption = ref([])

onMounted(() => {
  $table.value?.handleSearch()
  api.getRoleList({ page: 1, page_size: 9999 }).then((res) => (roleOption.value = res.data))
})

const columns = [
  {
    title: '名称',
    key: 'username',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '邮箱',
    key: 'email',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '用户角色',
    key: 'role',
    width: 60,
    align: 'center',
    render(row) {
      const roles = row.roles ?? []
      const group = []
      for (let i = 0; i < roles.length; i++)
        group.push(
          h(NTag, { type: 'info', style: { margin: '2px 3px' } }, { default: () => roles[i].name })
        )
      return h('span', group)
    },
  },
  {
    title: '超级用户',
    key: 'is_superuser',
    align: 'center',
    width: 40,
    render(row) {
      return h(
        NTag,
        { type: 'info', style: { margin: '2px 3px' } },
        { default: () => (row.is_superuser ? '是' : '否') }
      )
    },
  },
  {
    title: '上次登录时间',
    key: 'last_login',
    align: 'center',
    width: 80,
    ellipsis: { tooltip: true },
    render(row) {
      return h(
        NButton,
        { size: 'small', type: 'text', ghost: true },
        {
          default: () => (row.last_login !== null ? formatDate(row.last_login) : null),
          icon: renderIcon('mdi:update', { size: 16 }),
        }
      )
    },
  },
  {
    title: '禁用',
    key: 'is_active',
    width: 50,
    align: 'center',
    render(row) {
      return h(NSwitch, {
        size: 'small',
        rubberBand: false,
        value: row.is_active,
        loading: !!row.publishing,
        checkedValue: false,
        uncheckedValue: true,
        onUpdateValue: () => handleUpdateDisable(row),
      })
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
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/user/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ user_id: row.id }, false),
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
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/user/delete']]
              ),
            default: () => h('div', {}, '确定删除该用户吗?'),
          }
        ),
      ]
    },
  },
]

// 修改用户禁用状态
async function handleUpdateDisable(row) {
  if (!row.id) return
  const userStore = useUserStore()
  if (userStore.userId === row.id) {
    $message.error('当前登录用户不可禁用！')
    return
  }
  row.publishing = true
  row.is_active = row.is_active === false ? true : false
  row.publishing = false
  const role_ids = []

  try {
    await api.updateUser(row)
    $message?.success(row.is_active ? '已取消禁用该用户' : '已禁用该用户')
    $table.value?.handleSearch()
  } catch (err) {
    // 有异常恢复原来的状态
    row.is_active = row.is_active === false ? true : false
  } finally {
    row.publishing = false
  }
}

let lastClickedNodeId = null


const validateAddUser = {
  username: [
    {
      required: true,
      message: '请输入名称',
      trigger: ['input', 'blur'],
    },
  ],
  email: [
    {
      required: true,
      message: '请输入邮箱地址',
      trigger: ['input', 'change'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        const re = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        if (!re.test(modalForm.value.email)) {
          callback('邮箱格式错误')
          return
        }
        callback()
      },
    },
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  confirmPassword: [
    {
      required: true,
      message: '请再次输入密码',
      trigger: ['input'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        if (value !== modalForm.value.password) {
          callback('两次密码输入不一致')
          return
        }
        callback()
      },
    },
  ],
  roles: [
    {
      type: 'array',
      required: true,
      message: '请至少选择一个角色',
      trigger: ['blur', 'change'],
    },
  ],
}
</script>

<template>
  <NLayout has-sider wh-full>
    <NLayoutContent>
      <CommonPage show-footer title="用户列表">
        <template #action>
          <div class="flex justify-between space-x-4">
            <NButton v-permission="'post/api/v1/user/create'" type="primary" @click="handleAdd">
              <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建用户
            </NButton>
            <NUpload
              action="/api/v1/user/upload"
              :headers="{token: getToken()}"
              accept=".csv"
              show-upload-list={false}
              show-file-list="false"
              @finish="handleSuccess"
            > 
              <NButton type="primary">
          <TheIcon icon="material-symbols:upload" :size="18" class="mr-5" />导入用户
              </NButton>
            </NUpload>
          </div>
        </template>
        <template #upload>
          
        </template>
        <!-- 表格 -->
        <CrudTable
          ref="$table"
          v-model:query-items="queryItems"
          :columns="columns"
          :get-data="api.getUserList"
        >
          <template #queryBar>
            <QueryBarItem label="名称" :label-width="40">
              <NInput
                v-model:value="queryItems.username"
                clearable
                type="text"
                placeholder="请输入用户名称"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="邮箱" :label-width="40">
              <NInput
                v-model:value="queryItems.email"
                clearable
                type="text"
                placeholder="请输入邮箱"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
          </template>
        </CrudTable>

        <!-- 新增/编辑 弹窗 -->
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
            :rules="validateAddUser"
          >
            <NFormItem label="用户名称" path="username">
              <NInput v-model:value="modalForm.username" clearable placeholder="请输入用户名称" />
            </NFormItem>
            <NFormItem label="邮箱" path="email">
              <NInput v-model:value="modalForm.email" clearable placeholder="请输入邮箱" />
            </NFormItem>
            <NFormItem v-if="modalAction === 'add'" label="密码" path="password">
              <NInput
                v-model:value="modalForm.password"
                show-password-on="mousedown"
                type="password"
                clearable
                placeholder="请输入密码"
              />
            </NFormItem>
            <NFormItem v-if="modalAction === 'add'" label="确认密码" path="confirmPassword">
              <NInput
                v-model:value="modalForm.confirmPassword"
                show-password-on="mousedown"
                type="password"
                clearable
                placeholder="请确认密码"
              />
            </NFormItem>
            <NFormItem label="角色" path="role_ids">
              <NCheckboxGroup v-model:value="modalForm.role_ids">
                <NSpace item-style="display: flex;">
                  <NCheckbox
                    v-for="item in roleOption"
                    :key="item.id"
                    :value="item.id"
                    :label="item.name"
                  />
                </NSpace>
              </NCheckboxGroup>
            </NFormItem>
            <NFormItem label="超级用户" path="is_superuser">
              <NSwitch
                v-model:value="modalForm.is_superuser"
                size="small"
                :checked-value="true"
                :unchecked-value="false"
              ></NSwitch>
            </NFormItem>
            <NFormItem label="禁用" path="is_active">
              <NSwitch
                v-model:value="modalForm.is_active"
                :checked-value="false"
                :unchecked-value="true"
                :default-value="true"
              />
            </NFormItem>
          </NForm>
        </CrudModal>
      </CommonPage>
    </NLayoutContent>
  </NLayout>
  <!-- 业务页面 -->
</template>
