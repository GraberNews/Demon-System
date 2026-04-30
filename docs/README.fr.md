# 🎴 Demon System

> **Chatbot interactif basé sur Kivy/KivyMD avec deux démons IA**

---

## 🌍 Langues / Languages / Мови

🇫🇷 **[Français](README.fr.md)** | 🇬🇧 **[English](README.en.md)** | 🇺🇦 **[Українська](../README.md)**

---

## 🚀 Description

**Demon System** est une application mobile pour Android, implémentée en **Python** en utilisant le framework **Kivy** et les composants **KivyMD**.

L'application fournit une interface interactive pour communiquer avec deux "démons" virtuels :
- 🤖 **AI Demon** — intelligence artificielle
- 💎 **Gem Demon** — deuxième assistant virtuel

*Actuellement, les chats fonctionnent en mode test avec des réponses simulées.*

---

## 📱 Fonctionnalités

✅ **Deux systèmes de dialogue indépendants**  
✅ **Interface mobile intuitive** (mode Portrait)  
✅ **Menu de navigation latéral** (Navigation Drawer)  
✅ **Thème sombre** (Dark mode)  
✅ **Gestion dynamique des écrans**  
✅ **Historique des messages** (au cours de la session)

---

## 🛠️ Pile technologique

- **Python 3.x** — langage principal
- **Kivy** — framework pour interface mobile
- **KivyMD** — composants Material Design
- **Buildozer** — compilation Android (optionnel)

---

## 📁 Structure du projet

```
Demon-System/
├── main.py              # Application principale (orchestrateur)
├── home.py              # Écran d'accueil
├── settings.py          # Écran des paramètres
├── mod/
│   ├── pop_ai.py        # Chat du démon IA
│   └── pop_gem.py       # Chat du démon Gem
├── assets/              # Ressources (icônes, images)
├── docs/
│   ├── README.en.md     # Documentation en anglais
│   └── README.fr.md     # Documentation en français (ce fichier)
└── README.md            # README principal (Ukrainien)
```

---

## 🔮 Feuille de route de développement

🔄 **Intégration de modèles IA réels**
- OpenAI API / Google Gemini
- Modèles LLM locaux

💾 **Stockage de l'historique des dialogues**  
📊 **Analyses et statistiques**  
🎨 **Personnalisation des thèmes**  
🔊 **Messages vocaux**  
🌐 **Synchronisation entre appareils**

---

## 🚀 Démarrage rapide

### Exigences
```bash
pip install kivy kivymd
```

### Exécution
```bash
python main.py
```

> Sur les appareils Android, utilisez **Buildozer** pour compiler l'APK

---

## 📝 Licence

Licence MIT — libre d'utilisation et de modification.

---

## 👤 Auteur

**GraberNews** — développeur du projet

---

## 📞 Contacts

💬 GitHub : [@GraberNews](https://github.com/GraberNews)

---

*Ce projet est en développement actif. Suivez les mises à jour ! 🔥*