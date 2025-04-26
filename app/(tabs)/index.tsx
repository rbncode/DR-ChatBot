import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Keyboard,
} from "react-native";
import i18n from "../../i18n";

export default function ChatScreen() {
  const [messages, setMessages] = useState([
    { id: "1", sender: "assistant", text: i18n.t("assistantGreeting") },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: input,
    };
    const botResponse = {
      id: (Date.now() + 1).toString(),
      sender: "assistant",
      text: `Dijiste: "${input}"`,
    };

    setMessages((prev) => [...prev, userMessage, botResponse]);
    setInput("");
    Keyboard.dismiss();
  };

  const renderItem = ({ item }: any) => (
    <View
      style={[
        styles.message,
        item.sender === "user" ? styles.user : styles.assistant,
      ]}
    >
      <Text style={styles.messageText}>{item.text}</Text>
    </View>
  );

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.messagesContainer}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder={i18n.t("placeholder")}
          value={input}
          onChangeText={setInput}
          onSubmitEditing={sendMessage}
        />
        <TouchableOpacity onPress={sendMessage} style={styles.sendButton}>
          <Text style={styles.sendText}>{i18n.t("send")}</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#424242" },
  messagesContainer: { padding: 10, paddingBottom: 80 }, // Ensure there is space for the input bar
  message: {
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
    maxWidth: "75%",
  },
  user: {
    backgroundColor: "#DCF8C6",
    alignSelf: "flex-end",
  },
  assistant: {
    backgroundColor: "#EAEAEA",
    alignSelf: "flex-start",
  },
  messageText: { fontSize: 16 },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderTopWidth: 1,
    borderColor: "#ccc",
    backgroundColor: "#f1f1f1",
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
  },
  input: {
    flex: 1,
    fontSize: 16,
    padding: 10,
    backgroundColor: "#fff",
    borderRadius: 20,
  },
  sendButton: { justifyContent: "center", paddingHorizontal: 15 },
  sendText: { color: "#007AFF", fontWeight: "bold" },
});
