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
  const [showHelp, setShowHelp] = useState(true);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    if (showHelp) {
      setShowHelp(false);
    }

    const userMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    Keyboard.dismiss();

    try {
      const response = await fetch("http://192.168.6.152:8000/chatbot/", {
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
        text: data.respuesta || "Lo siento, no entendí eso.",
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
          body: { fontSize: 16 },
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
        {showHelp && (
          <View style={styles.helpPopup}>
            <Text style={styles.helpText}>
              ¿Necesitas saber noticias, clima, valor del dólar o UF?
              ¡Pregúntame para resolver tu duda! Puedes especificar el area del
              clima o noticias que necesites :)
            </Text>
          </View>
        )}

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
    paddingVertical: 6,
    paddingHorizontal: 14,
    marginVertical: 2,
    borderRadius: 20,
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
  helpPopup: {
    position: "absolute",
    top: 80,
    alignSelf: "center",
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 10,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
    maxWidth: "80%",
    zIndex: 10,
  },
  helpText: {
    fontSize: 16,
    textAlign: "center",
    color: "#333",
  },
});
