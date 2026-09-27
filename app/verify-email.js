import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import { verifyEmailRequest, resendCodeRequest } from "../src/api/client";

export default function VerifyEmailScreen() {
  const router = useRouter();
  const { email } = useLocalSearchParams(); // signup.js-dən "email" bura ötürülür
  const [code, setCode] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [resending, setResending] = useState(false);

  async function handleVerify() {
    if (!code) {
      Alert.alert("Xəta", "Kodu daxil edin.");
      return;
    }
    setSubmitting(true);
    try {
      await verifyEmailRequest(email, code);
      Alert.alert("Uğurlu!", "Email təsdiqləndi.", [
        { text: "Davam et", onPress: () => router.replace("/home") },
      ]);
    } catch (err) {
      const message = err.response?.data?.detail || "Kod yanlışdır və ya vaxtı bitib.";
      Alert.alert("Xəta", String(message));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleResend() {
    setResending(true);
    try {
      await resendCodeRequest(email);
      Alert.alert("Göndərildi", "Yeni kod email-inizə göndərildi.");
    } catch (err) {
      Alert.alert("Xəta", "Kod göndərilə bilmədi, bir az sonra yenidən cəhd edin.");
    } finally {
      setResending(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Email-i təsdiqləyin</Text>
      <Text style={styles.subtitle}>
        {email} ünvanına göndərilən 6 rəqəmli kodu daxil edin.
      </Text>

      <TextInput
        style={styles.input}
        placeholder="123456"
        keyboardType="number-pad"
        maxLength={6}
        value={code}
        onChangeText={setCode}
      />

      <TouchableOpacity style={styles.button} onPress={handleVerify} disabled={submitting}>
        {submitting ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Təsdiqlə</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={handleResend} disabled={resending}>
        <Text style={styles.link}>
          {resending ? "Göndərilir..." : "Kod gəlmədi? Yenidən göndər"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 8, textAlign: "center" },
  subtitle: { fontSize: 14, color: "#555", marginBottom: 24, textAlign: "center" },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 14,
    marginBottom: 14,
    fontSize: 24,
    textAlign: "center",
    letterSpacing: 8,
  },
  button: {
    backgroundColor: "#2e7d32",
    padding: 16,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 8,
  },
  buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" },
  link: { color: "#2e7d32", textAlign: "center", marginTop: 20 },
});
