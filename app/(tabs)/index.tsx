import React, { useRef, useState, useEffect } from "react";
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
import Markdown from "react-native-markdown-display";

export default function ChatScreen() {
  const screenWidth = Dimensions.get("window").width;
  const [showHelp, setShowHelp] = useState(true);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => {
    if (messages.length > 0) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages]);

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
          text: { color: item.sender === "user" ? "#000" : "#fff" },
        }}
      >
        {item.text}
      </Markdown>
    </View>
  );

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
            contentContainerStyle={[
              styles.messagesContainer,
              {
                flexGrow: 1,
                justifyContent: "flex-end",
              },
            ]}
            onContentSizeChange={() => {
              flatListRef.current?.scrollToEnd({ animated: false });
            }}
            onLayout={() => {
              flatListRef.current?.scrollToEnd({ animated: false });
            }}
          />
        </View>
        <View style={styles.inputWrapper}>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder={"¡Pregúnta algo!"}
              value={input}
              onChangeText={setInput}
              onSubmitEditing={sendMessage}
              placeholderTextColor="#999"
            />
            <TouchableOpacity onPress={sendMessage} style={styles.sendButton}>
              <Text style={styles.sendIcon}>➤</Text>
            </TouchableOpacity>
          </View>
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
    paddingBottom: 15,
    maxWidth: 800,
    width: "95%",
    alignSelf: "center",
  },
  message: {
    padding: 10,
    paddingVertical: 6,
    paddingHorizontal: 14,
    marginVertical: 10,
    borderRadius: 20,
    maxWidth: "75%",
  },
  user: {
    backgroundColor: "#d9d9d9",
    alignSelf: "flex-end",
  },
  userText: {
    color: "#fffff",
  },
  assistant: {
    backgroundColor: "#252525",
    alignSelf: "flex-start",
  },
  assistantText: {
    color: "#000",
  },

  messageText: {
    fontSize: 16,
  },
  inputWrapper: {
    backgroundColor: "transparent",
    paddingHorizontal: 10,
    paddingVertical: 8,
    marginBottom: 10,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 1,
    maxWidth: 850,
    width: "90%",
    backgroundColor: "#fff",
    alignSelf: "center",
    borderRadius: 50,
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
    paddingHorizontal: 5,
  },
  sendIcon: {
    fontSize: 50,
    color: "#525252",
  },
  helpPopup: {
    position: "absolute",
    alignContent: "flex-end",
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
