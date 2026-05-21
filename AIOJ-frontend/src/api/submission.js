import request from './request'
 
export const submissionApi = {
  // 提交代码
  submit: (data) => request.post('/submissions', data),
  // 获取提交列表
  getList: (params) => request.get('/submissions', { params }),
  // 获取提交详情（轮询用）
  getDetail: (id) => request.get(`/submissions/${id}`),
//   // 获取 AI 分析结果
//   getAiAnalysis: (id) => request.get(`/submissions/${id}/ai-analysis`),
}
 