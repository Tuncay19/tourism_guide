import { Stack } from "expo-router";
import { AuthProvider } from "../src/context/AuthContext";

// Bu fayl BÜTÜN app-ın "çərçivəsidir" — hər səhifə bunun içində açılır.
// AuthProvider sayəsində hər səhifə "kim giriş edib?" məlumatına çata bilir.
export default function RootLayout() {
  return (
    <AuthProvider>
      <Stack screenOptions={{ headerShown: false }} />
    </AuthProvider>
  );
}
