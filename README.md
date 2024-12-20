# Donna - Your AI-Powered Secretary

Donna is your personal AI-powered secretary that intelligently manages your calls, filters out spam, and shares your scheduling link when you're busy. Using OpenAI's [Realtime API](https://openai.com/index/introducing-the-realtime-api/) with function calling to Google Calendar and Twilio, Donna handles calls dynamically, supporting 85 languages with real-time updates.

**What's New:**
- **AI Orchestration with LangGraph**: Seamlessly orchestrates multiple AI agents for call management, scheduling coordination, and real-time status reporting.

## **Monorepo Stack**

### **Backend (FastAPI, Python)**
- **Phone Call Management**: Handles both incoming and outgoing calls via Twilio and OpenAI using WebSockets.
- **Google Calendar Integration**: Reads your calendar in real-time to check your availability.
- **Message Scheduling**: Sends automated text messages with scheduling links.
- **Call Status Reporting**: Displays live call progress.

### **Frontend (Next.js, TypeScript)**
- **Live Call Visualization**: Real-time call status page.
- **User Preferences Management**: Integrated with EdgeDB for storing user settings.

## **Running the Application**

### **Environment Variables (`.env` file):**
```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=   # Dedicated Twilio number
USER_PHONE_NUMBER=     # Your personal phone number
STREAM_URL=            # Backend WebSocket URL
OPENAI_API_KEY=
CALENDLY_URL=          # Your scheduling link
