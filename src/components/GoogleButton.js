import React, { useState } from "react";
import { TouchableOpacity, Text, StyleSheet, Alert, ActivityIndicator, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import * as WebBrowser from "expo-web-browser";
import * as Linking from "expo-linking";
import { useRouter } from "expo-router";
import { API_URL } from "../api/client";
import { useAuth } from "../context/AuthContext";

WebBrowser.maybeCompleteAuthSession();

// Bu düymə backend-dəki Google girişini brauzer pəncərəsində açır.
// Giriş bitəndə backend bizi tokenlə birlikdə app-a geri qaytarır.
export default function GoogleButton() {
  const router = useRouter();
  const { loginWithToken } = useAuth();
  const [busy, setBusy] = useState(false);

  async function handlePress() {
    setBusy(true);
    try {
      // Expo Go-da exp://..., hazır app-da azturizm://... ünvanı yaranır
      const redirectUrl = Linking.createURL("oauth-success");
      const authUrl = `${API_URL}/api/auth/google?app_redirect=${encodeURIComponent(redirectUrl)}`;

      const result = await WebBrowser.openAuthSessionAsync(authUrl, redirectUrl);

      if (result.type === "success" && result.url) {
        const { queryParams } = Linking.parse(result.url);
        const token = queryParams?.token;
        if (token) {
          await loginWithToken(String(token));
          router.replace("/home");
          return;
        }
        Alert.alert("Xəta", "Google ilə giriş tamamlanmadı.");
      }
      // İstifadəçi pəncərəni özü bağlayıbsa (cancel/dismiss), heç nə göstərmirik
    } catch (err) {
      Alert.alert("Xəta", "Google ilə giriş alınmadı. Bir az sonra yenidən cəhd edin.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <View>
      <View style={styles.dividerRow}>
        <View style={styles.line} />
        <Text style={styles.dividerText}>və ya</Text>
        <View style={styles.line} />
      </View>

      <TouchableOpacity style={styles.button} onPress={handlePress} disabled={busy}>
        {busy ? (
          <ActivityIndicator color="#444" />
        ) : (
          <>
            <Ionicons name="logo-google" size={20} color="#DB4437" style={{ marginRight: 10 }} />
            <Text style={styles.text}>Google ilə davam et</Text>
          </>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  dividerRow: { flexDirection: "row", alignItems: "center", marginTop: 24, marginBottom: 16 },
  line: { flex: 1, height: 1, backgroundColor: "#e0e0e0" },
  dividerText: { marginHorizontal: 12, color: "#888", fontSize: 13 },
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 14,
    backgroundColor: "#fff",
  },
  text: { fontSize: 16, fontWeight: "600", color: "#333" },
});
