export const authConfig = {
  tokenKey: 'paybd_access_token',
  refreshTokenKey: 'paybd_refresh_token',
};

export function saveAuthTokens(tokens: { access_token: string; refresh_token: string }) {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.setItem(authConfig.tokenKey, tokens.access_token);
  window.localStorage.setItem(authConfig.refreshTokenKey, tokens.refresh_token);
}

export function getStoredAccessToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }

  return window.localStorage.getItem(authConfig.tokenKey);
}

export function clearAuthTokens() {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.removeItem(authConfig.tokenKey);
  window.localStorage.removeItem(authConfig.refreshTokenKey);
}

export function getAuthHeaders(token: string | null) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
