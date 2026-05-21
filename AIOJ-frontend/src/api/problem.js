import request from './request'
 
export const problemApi = {
  // 获取题目列表
  getList: (params) => request.get('/problems', { params }),
  // 获取题目详情
  getDetail: (id) => request.get(`/problems/${id}`),
}