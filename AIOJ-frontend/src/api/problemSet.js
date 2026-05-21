import request from './request'

export const problemSetApi = {
  // 获取题单列表
  getList: (params) => request.get('/problem-sets', { params }),
  // 获取题单详情
  getDetail: (id) => request.get(`/problem-sets/${id}`),
  // 创建题单
  create: (data) => request.post('/problem-sets', data),
  // 更新题单
  update: (id, data) => request.put(`/problem-sets/${id}`, data),
  // 删除题单
  delete: (id) => request.delete(`/problem-sets/${id}`),
  // 添加题目到题单
  addProblem: (setId, data) => request.post(`/problem-sets/${setId}/problems`, data),
  // 从题单移除题目
  removeProblem: (setId, problemId) => request.delete(`/problem-sets/${setId}/problems/${problemId}`),
}
