export const authConfig = {
  tokenKey: 'paybd_access_token',
  refreshTokenKey: 'paybd_refresh_token',
};

export function getAuthHeaders(token: string | null) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
