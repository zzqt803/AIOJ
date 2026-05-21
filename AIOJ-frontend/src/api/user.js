import request from './request'

export const userApi = {
  // 获取当前用户信息
  getMe: () => request.get('/users/me'),
  // 获取用户统计
  getMyStats: () => request.get('/users/me/stats'),
}
