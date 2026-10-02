// Bu fayl backend-imizlə "danışan" bütün sorğuları bir yerdə saxlayır.
// Beləcə backend linki dəyişsə, yalnız BURADA dəyişmək kifayət edir.

import axios from "axios";

// DİQQƏT: bura öz Render linkinizi yazın (sonunda "/" OLMASIN)
export const API_URL = "https://tourism-guide-stsh.onrender.com";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// --- Backend-ə göndərəcəyimiz funksiyalar ---

// Qeydiyyat (signup)
export async function signupRequest(email, password, fullName) {
  const response = await apiClient.post("/api/auth/signup", {
    email,
    password,
    full_name: fullName,
  });
  return response.data; // { message, token, user }
}

// Giriş (login)
export async function loginRequest(email, password) {
  const response = await apiClient.post("/api/auth/login", {
    email,
    password,
  });
  return response.data; // { message, token, user }
}

// Cari istifadəçini token ilə tapmaq
export async function getMeRequest(token) {
  const response = await apiClient.get("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data; // user
}

// Email təsdiqləmə kodunu göndərmək
export async function verifyEmailRequest(email, code) {
  const response = await apiClient.post("/api/auth/verify-email", { email, code });
  return response.data; // { message }
}

// Yeni təsdiqləmə kodu istəmək
export async function resendCodeRequest(email) {
  const response = await apiClient.post("/api/auth/resend-code", { email });
  return response.data; // { message }
}

export default apiClient;
