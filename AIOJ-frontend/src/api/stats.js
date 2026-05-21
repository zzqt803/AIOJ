import request from './request'

export const statsApi = {
  // 获取当前用户统计
  getMyStats: () => request.get('/users/me/stats'),
  // 获取排行榜
  getLeaderboard: (params) => request.get('/leaderboard', { params }),
}
