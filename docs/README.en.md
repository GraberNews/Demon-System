# 🎴 Demon System

> **Interactive chatbot based on Kivy/KivyMD with two AI demons**

---

## 🌍 Languages / Мови / Langues

🇬🇧 **[English](README.en.md)** | 🇺🇦 **[Українська](../README.md)** | 🇫🇷 **[Français](README.fr.md)**

---

## 🚀 Description

**Demon System** is a mobile application for Android, implemented in **Python** using the **Kivy** framework and **KivyMD** components.

The application provides an interactive interface for communicating with two virtual "demons":
- 🤖 **AI Demon** — artificial intelligence
- 💎 **Gem Demon** — second virtual assistant

*Currently, chats operate in test mode with simulated responses.*

---

## 📱 Features

✅ **Two independent dialogue systems**  
✅ **Intuitive mobile interface** (Portrait mode)  
✅ **Side navigation menu** (Navigation Drawer)  
✅ **Dark theme** (Dark mode)  
✅ **Dynamic screen management**  
✅ **Message history** (within session)

---

## 🛠️ Technology Stack

- **Python 3.x** — main language
- **Kivy** — mobile UI framework
- **KivyMD** — Material Design components
- **Buildozer** — Android compilation (optional)

---

## 📁 Project Structure

```
Demon-System/
├── main.py              # Main application (orchestrator)
├── home.py              # Home screen
├── settings.py          # Settings screen
├── mod/
│   ├── pop_ai.py        # AI demon chat
│   └── pop_gem.py       # Gem demon chat
├── assets/              # Resources (icons, images)
├── docs/
│   ├── README.en.md     # English documentation (this file)
│   └── README.fr.md     # French documentation
└── README.md            # Main README (Ukrainian)
```

---

## 🔮 Development Roadmap

🔄 **Integration of real AI models**
- OpenAI API / Google Gemini
- Local LLM models

💾 **Dialog history storage**  
📊 **Analytics and statistics**  
🎨 **Theme customization**  
🔊 **Voice messages**  
🌐 **Cross-device synchronization**

---

## 🚀 Quick Start

### Requirements
```bash
pip install kivy kivymd
```

### Running
```bash
python main.py
```

> On Android devices, use **Buildozer** to compile APK

---

## 📝 License

MIT License — free to use and modify.

---

## 👤 Author

**GraberNews** — project developer

---

## 📞 Contacts

💬 GitHub: [@GraberNews](https://github.com/GraberNews)

---

*This project is under active development. Follow for updates! 🔥*