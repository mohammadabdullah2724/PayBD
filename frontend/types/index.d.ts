export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
}

export interface UserProfile {
  email: string;
  is_active: boolean;
}
