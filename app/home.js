import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import { useAuth } from "../src/context/AuthContext";

export default function HomeScreen() {
  const router = useRouter();
  const { user, logout } = useAuth();

  async function handleLogout() {
    await logout();
    router.replace("/login");
  }

  return (
    <View style={styles.container}>
      <Text style={styles.welcome}>Xoş gəldin, {user?.full_name}! 👋</Text>
      <Text style={styles.subtitle}>Qarabağ Turizm Guide app-ına daxil oldunuz.</Text>

      <TouchableOpacity style={styles.button} onPress={handleLogout}>
        <Text style={styles.buttonText}>Çıxış et</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 24, backgroundColor: "#fff" },
  welcome: { fontSize: 22, fontWeight: "bold", marginBottom: 8, textAlign: "center" },
  subtitle: { fontSize: 15, color: "#555", marginBottom: 32, textAlign: "center" },
  button: { backgroundColor: "#c62828", padding: 14, borderRadius: 8, paddingHorizontal: 32 },
  buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" },
});
