import request from './request'

export const discussionApi = {
  // 获取题目讨论列表
  getList: (problemId, params) => request.get(`/problems/${problemId}/discussions`, { params }),
  // 发表评论
  create: (problemId, data) => request.post(`/problems/${problemId}/discussions`, data),
  // 删除评论
  delete: (id) => request.delete(`/discussions/${id}`),
}
