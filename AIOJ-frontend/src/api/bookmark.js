import request from './request'

export const bookmarkApi = {
  // 获取收藏列表
  getList: (params) => request.get('/bookmarks', { params }),
  // 收藏题目
  create: (data) => request.post('/bookmarks', data),
  // 取消收藏
  delete: (problemId) => request.delete(`/bookmarks/${problemId}`),
  // 检查是否已收藏
  check: (problemId) => request.get(`/problems/${problemId}/is-bookmarked`),
}
