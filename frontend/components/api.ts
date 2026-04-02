"use client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

async function request(path: string, options: RequestInit = {}) {
  const token = getToken();

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Request failed");
  }

  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }

  return null;
}

export async function login(username: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);

  const res = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Login failed");
  }

  return res.json();
}

export async function register(email: string, password: string) {
  return request("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getMe() {
  return request("/api/v1/auth/me");
}

export async function getProperties() {
  return request("/api/v1/properties");
}

export async function createProperty(payload: {
  title: string;
  address: string;
  description?: string;
  city?: string;
  latitude?: number | null;
  longitude?: number | null;
  property_type?: string;
}) {
  return request("/api/v1/properties", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getProperty(propertyId: string | number) {
  return request(`/api/v1/properties/${propertyId}`);
}

export async function getAssessments(propertyId: string | number) {
  return request(`/api/v1/properties/${propertyId}/assessments`);
}

export async function createAssessment(
  propertyId: string | number,
  payload: {
    infrastructure: number;
    lighting: number;
    noise: number;
    insolation: number;
    development: number;
    notes?: string;
  }
) {
  return request(`/api/v1/properties/${propertyId}/assessments`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function computeScore(propertyId: string | number) {
  return request(`/api/v1/properties/${propertyId}/compute-score`, {
    method: "POST",
  });
}

export async function getComputedScores(propertyId: string | number) {
  return request(`/api/v1/properties/${propertyId}/computed-scores`);
}