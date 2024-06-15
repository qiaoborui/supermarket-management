import { request } from '@/utils'

export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  signup: (data) => request.post('/base/signup', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  uploadUser: (data = {}) => request.post('/user/upload', data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),

  // discount_level
  getDiscountLevels: (params = {}) => request.get('/discount_level/list', { params }),
  createDiscountLevel: (data = {}) => request.post('/discount_level/create', data),
  updateDiscountLevel: (data = {}) => request.post('/discount_level/update', data),
  deleteDiscountLevel: (params = {}) => request.delete('/discount_level/delete', { params }),
  // member
  getMembers: (params = {}) => request.get('/member/list', { params }),
  createMember: (data = {}) => request.post('/member/create', data),
  updateMember: (data = {}) => request.post('/member/update', data),
  deleteMember: (params = {}) => request.delete('/member/delete', { params }),
  // consumption
  getConsumptions: (params = {}) => request.get('/consumption_record/list', { params }),
  createConsumption: (data = {}) => request.post('/consumption_record/create', data),
  updateConsumption: (data = {}) => request.post('/consumption_record/update', data),
  deleteConsumption: (params = {}) => request.delete('/consumption_record/delete', { params }),
}
