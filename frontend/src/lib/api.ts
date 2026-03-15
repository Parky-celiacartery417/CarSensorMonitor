import { CarDetail, CarFilters, CarListResponse, CarStats, TokenResponse } from "./types";

const API_BASE = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api`;

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((options.headers as Record<string, string>) || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

export async function login(username: string, password: string): Promise<string> {
  const data = await request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  if (typeof window !== "undefined") {
    localStorage.setItem("token", data.access_token);
  }
  return data.access_token;
}

export function logout(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export async function getCars(filters: CarFilters = {}): Promise<CarListResponse> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, String(value));
    }
  });
  const query = params.toString();
  return request<CarListResponse>(`/cars${query ? `?${query}` : ""}`);
}

export async function getCarById(id: string): Promise<CarDetail> {
  return request<CarDetail>(`/cars/${id}`);
}

export async function getMakers(): Promise<string[]> {
  return request<string[]>("/cars/makers");
}

export async function getStats(): Promise<CarStats> {
  return request<CarStats>("/cars/stats");
}
