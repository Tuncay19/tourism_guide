// Bu fayl "kim giriş edib, edilməyib" məlumatını bütün app boyu yadda saxlayır.
// React-də "Context" — bir dəyəri hər ekrandan əlçatan etməyin üsuludur.
// Yəni token/user-i hər ekrana əl ilə ötürmək əvəzinə, buradan "oxuyuruq".

import React, { createContext, useState, useContext, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { loginRequest, signupRequest, getMeRequest } from "../api/client";

const AuthContext = createContext(null);

// Bütün app-ı bu komponentlə "sarmalayacağıq" (App.js-də görəcəksiniz)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true); // app ilk açılanda yoxlayır: token yadda qalıbmı?

  // App ilk açılanda telefonun yaddaşında saxlanmış token varmı, yoxlayırıq
  useEffect(() => {
    async function loadStoredToken() {
      try {
        const storedToken = await AsyncStorage.getItem("token");
        if (storedToken) {
          const currentUser = await getMeRequest(storedToken);
          setToken(storedToken);
          setUser(currentUser);
        }
      } catch (err) {
        // Token etibarsızdırsa, sadəcə giriş ekranında qalır
        await AsyncStorage.removeItem("token");
      } finally {
        setLoading(false);
      }
    }
    loadStoredToken();
  }, []);

  async function login(email, password) {
    const data = await loginRequest(email, password);
    await AsyncStorage.setItem("token", data.token);
    setToken(data.token);
    setUser(data.user);
  }

  async function signup(email, password, fullName) {
    const data = await signupRequest(email, password, fullName);
    await AsyncStorage.setItem("token", data.token);
    setToken(data.token);
    setUser(data.user);
  }

  async function logout() {
    await AsyncStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Ekranlarda bu funksiyanı çağıraraq user/token/login/signup/logout-a çatacağıq
export function useAuth() {
  return useContext(AuthContext);
}