import React, { useRef, useState } from "react";
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
  SafeAreaView,
  Dimensions,
} from "react-native";
import i18n from "../../i18n";
import Markdown from "react-native-markdown-display";

export default function ChatScreen() {
  const screenWidth = Dimensions.get("window").width;
  const isLargeSreen = screenWidth >= 600;

  const [messages, setMessages] = useState([
    { id: "1", sender: "assistant", text: i18n.t("assistantGreeting") },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    Keyboard.dismiss();

    try {
      const response = await fetch("http://192.168.1.12:8000/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pregunta: input }),
      });

      const data = await response.json();

      const botMessage = {
        id: (Date.now() + 1).toString(),
        sender: "assistant",
        text: data.respuesta || "lo siento, no entendí eso.",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: (Date.now() + 2).toString(),
        sender: "assistant",
        text: "Hubo un error al contactar al servidor.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const renderItem = ({ item }: any) => (
    <View
      style={[
        styles.message,
        item.sender === "user" ? styles.user : styles.assistant,
      ]}
    >
      <Markdown
        style={{
          body: { fontSize: 14.5 },
        }}
      >
        {item.text}
      </Markdown>
    </View>
  );

  const flatListRef = useRef<FlatList>(null);

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#424242" }}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        keyboardVerticalOffset={80}
      >
        <View style={styles.chatContainer}>
          <FlatList
            ref={flatListRef}
            data={messages}
            keyExtractor={(item) => item.id}
            renderItem={renderItem}
            contentContainerStyle={styles.messagesContainer}
            onContentSizeChange={() =>
              flatListRef.current?.scrollToEnd({ animated: true })
            }
          />
        </View>
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder={i18n.t("placeholder")}
            value={input}
            onChangeText={setInput}
            onSubmitEditing={sendMessage}
            placeholderTextColor="#999"
          />
          <TouchableOpacity onPress={sendMessage} style={styles.sendButton}>
            <Text style={styles.sendText}>{i18n.t("send")}</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  chatContainer: {
    flex: 1,
  },
  messagesContainer: {
    padding: 10,
    paddingBottom: 80,
    maxWidth: 800,
    width: "95%",
    alignSelf: "center",
  },
  message: {
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
  },
  user: {
    backgroundColor: "#DCF8C6",
    alignSelf: "flex-end",
  },
  assistant: {
    backgroundColor: "#EAEAEA",
    alignSelf: "flex-start",
  },
  messageText: {
    fontSize: 16,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 15,
    maxWidth: 850,
    width: "90%",
    backgroundColor: "transparent",
    alignSelf: "center",
  },
  input: {
    flex: 1,
    fontSize: 16,
    paddingHorizontal: 15,
    paddingVertical: 10,
    backgroundColor: "#fff",
    borderRadius: 20,
  },
  sendButton: {
    justifyContent: "center",
    paddingHorizontal: 15,
  },
  sendText: {
    color: "#007AFF",
    fontWeight: "bold",
  },
});
