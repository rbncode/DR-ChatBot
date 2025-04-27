import * as Localization from "expo-localization";
import { I18n } from "i18n-js";

const i18n = new I18n(); // ✅ only declare once

i18n.translations = {
  es: {
    assistantGreeting: "¡Hola! ¿En qué puedo ayudarte?",
    placeholder: "Escribe un mensaje...",
    send: "Enviar",
  },
};

i18n.locale = "es"; // Directly set the locale to Spanish
i18n.fallbacks = true;

export default i18n;
