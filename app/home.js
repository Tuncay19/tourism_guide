import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
} from "react-native";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../src/context/AuthContext";

const TABS = [
  { key: "shops", label: "Mağazalar" },
  { key: "restaurants", label: "Restoranlar" },
  { key: "hotels", label: "Otellər" },
];

export default function HomeScreen() {
  const router = useRouter();
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState("shops");
  const [searchText, setSearchText] = useState("");

  const activeLabel = TABS.find((t) => t.key === activeTab)?.label;

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* --- Üst hissə: sol tərəfdə app adı, sağda profil ikonu --- */}
      <View style={styles.header}>
        <Text style={styles.appName}>AzTurizm Guide</Text>
        <TouchableOpacity onPress={() => router.push("/profile")}>
          <View style={styles.profileCircle}>
            <Ionicons name="person" size={20} color="#fff" />
          </View>
        </TouchableOpacity>
      </View>

      {/* --- Axtarış sistemi --- */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={18} color="#888" style={{ marginRight: 8 }} />
        <TextInput
          style={styles.searchInput}
          placeholder="Məkan, restoran, otel axtar..."
          value={searchText}
          onChangeText={setSearchText}
        />
      </View>

      {/* --- Tablar: Mağazalar / Restoranlar / Otellər --- */}
      <View style={styles.tabsContainer}>
        {TABS.map((tab) => (
          <TouchableOpacity
            key={tab.key}
            style={[styles.tab, activeTab === tab.key && styles.tabActive]}
            onPress={() => setActiveTab(tab.key)}
          >
            <Text style={[styles.tabText, activeTab === tab.key && styles.tabTextActive]}>
              {tab.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* --- Məzmun sahəsi (hələlik boş, sonra real data gələcək) --- */}
      <View style={styles.content}>
        <Ionicons name="map-outline" size={48} color="#ccc" />
        <Text style={styles.placeholderText}>
          {activeLabel} tezliklə burada görünəcək
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: "#fff" },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 8,
  },
  appName: { fontSize: 20, fontWeight: "bold", color: "#1b1b1b" },
  profileCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#2e7d32",
    justifyContent: "center",
    alignItems: "center",
  },

  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#f2f2f2",
    borderRadius: 10,
    paddingHorizontal: 14,
    marginHorizontal: 20,
    marginTop: 8,
    height: 44,
  },
  searchInput: { flex: 1, fontSize: 15 },

  tabsContainer: {
    flexDirection: "row",
    marginHorizontal: 20,
    marginTop: 18,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: "center",
    borderBottomWidth: 2,
    borderBottomColor: "transparent",
  },
  tabActive: { borderBottomColor: "#2e7d32" },
  tabText: { fontSize: 14, color: "#888", fontWeight: "500" },
  tabTextActive: { color: "#2e7d32", fontWeight: "700" },

  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingBottom: 80,
  },
  placeholderText: { marginTop: 12, color: "#999", fontSize: 14 },
});
