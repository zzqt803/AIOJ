import request from './request'
 
export const authApi = {
  login: (data) => request.post('/auth/login', data),
  register: (data) => request.post('/auth/register', data),
  changePassword: (data) => request.post('/auth/password', data),
}
 