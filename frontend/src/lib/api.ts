/**
 * KisanSlot / FarmQueue Typed API Client Wrapper
 * Smart India Hackathon 2026 - Problem Statement 26032
 */

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  version: string;
  timestamp: string;
  database: string;
  platform: string;
}

export interface TokenResponse {
  access: string;
  refresh: string;
}

export interface FarmerUser {
  id: number;
  phone: string;
  full_name: string;
  village: string;
  district: string;
  state: string;
  preferred_language: string;
  crop_type: string;
  role: 'farmer';
}

export interface StaffUser {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role: 'operator' | 'officer' | 'admin';
  is_staff: boolean;
}

export interface SendOTPResponse {
  status: string;
  message: string;
  phone: string;
  is_registered: boolean;
  dev_otp?: string;
}

export interface AuthResponse<U = FarmerUser | StaffUser> {
  status: string;
  message: string;
  tokens: TokenResponse;
  user: U;
}

export interface RegisterFarmerData {
  phone: string;
  full_name: string;
  village?: string;
  district?: string;
  state?: string;
  preferred_language?: string;
  crop_type?: string;
}

export interface ApiRootModuleResponse {
  message: string;
  module: string;
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' ? 'http://localhost:8000' : 'http://backend:8000');

export class ApiError extends Error {
  status: number;
  data?: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

// Token helper utilities for client side
export const authStorage = {
  saveTokens: (tokens: TokenResponse, user?: any) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('kisanslot_access_token', tokens.access);
      localStorage.setItem('kisanslot_refresh_token', tokens.refresh);
      if (user) {
        localStorage.setItem('kisanslot_user', JSON.stringify(user));
      }
    }
  },
  getAccessToken: (): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('kisanslot_access_token');
    }
    return null;
  },
  getUser: (): any | null => {
    if (typeof window !== 'undefined') {
      const data = localStorage.getItem('kisanslot_user');
      return data ? JSON.parse(data) : null;
    }
    return null;
  },
  clear: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('kisanslot_access_token');
      localStorage.removeItem('kisanslot_refresh_token');
      localStorage.removeItem('kisanslot_user');
    }
  },
};

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${API_BASE_URL}${cleanEndpoint}`;

  const token = authStorage.getAccessToken();
  const authHeaders: Record<string, string> = {};
  if (token) {
    authHeaders['Authorization'] = `Bearer ${token}`;
  }

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...authHeaders,
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    const isJson = response.headers
      .get('content-type')
      ?.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      const msg =
        typeof data === 'object' && data !== null
          ? data.message || data.detail || (data.phone ? data.phone[0] : null) || (data.otp ? data.otp[0] : null) || JSON.stringify(data)
          : String(data);
      throw new ApiError(
        msg || `API request failed with status ${response.status}`,
        response.status,
        data
      );
    }

    return data as T;
  } catch (error: any) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      error.message || 'Failed to connect to backend service',
      0,
      null
    );
  }
}

export const apiClient = {
  // System Health
  getHealth: () => request<HealthCheckResponse>('/api/health/'),

  // Authentication & Accounts
  auth: {
    sendFarmerOTP: (phone: string) =>
      request<SendOTPResponse>('/api/accounts/farmer/send-otp/', {
        method: 'POST',
        body: JSON.stringify({ phone }),
      }),

    verifyFarmerOTP: (phone: string, otp: string) =>
      request<AuthResponse<FarmerUser>>('/api/accounts/farmer/verify-otp/', {
        method: 'POST',
        body: JSON.stringify({ phone, otp }),
      }),

    registerFarmer: (data: RegisterFarmerData) =>
      request<AuthResponse<FarmerUser>>('/api/accounts/farmer/register/', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    loginStaff: (credentials: { username: string; password: string }) =>
      request<AuthResponse<StaffUser>>('/api/accounts/staff/login/', {
        method: 'POST',
        body: JSON.stringify(credentials),
      }),

    getCurrentUser: () => request<any>('/api/accounts/me/'),

    refreshToken: (refreshToken: string) =>
      request<{ access: string }>('/api/auth/token/refresh/', {
        method: 'POST',
        body: JSON.stringify({ refresh: refreshToken }),
      }),
  },

  // Modules Scaffolding
  accounts: {
    getRoot: () => request<ApiRootModuleResponse>('/api/accounts/'),
  },
  centres: {
    getRoot: () => request<ApiRootModuleResponse>('/api/centres/'),
  },
  bookings: {
    getRoot: () => request<ApiRootModuleResponse>('/api/bookings/'),
  },
  queue: {
    getRoot: () => request<ApiRootModuleResponse>('/api/queue/'),
  },
  notifications: {
    getRoot: () => request<ApiRootModuleResponse>('/api/notifications/'),
  },
};

export default apiClient;
