# 🎭 Sentiment Analysis Tool — Frontend

This is the **frontend** part of the **Sentiment Analysis Tool** project.  
It provides an interactive web interface where users can input text and get real-time **sentiment predictions** (Positive, Negative, or Neutral) powered by the backend model API.

---

## 🚀 About the Project

The Sentiment Analysis Tool helps analyze emotions in text using machine learning.  
This frontend connects with the **FastAPI backend** (found in the `model-lab` folder) to display predictions in a clean, user-friendly interface.

---

## ⚙️ Tech Stack
- **Next.js** — React-based frontend framework  
- **TypeScript** — for type-safe coding  
- **Tailwind CSS** *(if used)* — for responsive styling  
- **FastAPI (Backend)** — handles the ML model and API  

---

## 🧩 Project Structure
frontend/
├── app/
├── components/
├── public/
├── styles/
├── package.json
└── README.md

---

## 🧠 Features
- Simple input box for text or data entry  
- Connects to backend to get emotion predictions  
- Displays results in real time  
- Built with Next.js for high performance and scalability  

---

## 🪄 Connecting to the Backend
Before running the frontend, ensure that the backend (from the `model-lab` folder) is up and running:

```bash
uvicorn app.main:app --reload
Once running, update the API endpoint in your frontend configuration if required.

🧰 Getting Started
This project was bootstrapped with create-next-app

1️⃣ Install Dependencies
Inside the frontend directory:
npm install

2️⃣ Run the Development Server
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
Open http://localhost:3000
 in your browser to see the result.

You can start editing the page by modifying app/page.tsx. The page auto-updates as you edit the file.

This project uses next/font
 to automatically optimize and load Geist
, a new font family from Vercel.

📚 Learn More
To learn more about Next.js, check these resources:

Next.js Documentation
 — learn about Next.js features and API.

Learn Next.js
 — an interactive Next.js tutorial.

You can check out the Next.js GitHub repository
 — your feedback and contributions are welcome!

 🚀 Deploy on Vercel
The easiest way to deploy your Next.js app is to use the Vercel Platform
 from the creators of Next.js.

Check out Next.js deployment documentation
 for more details.

 🤝 Contributing
If you’d like to contribute, feel free to open issues or pull requests to enhance the UI or documentation.

👩‍💻 Author
Developed by @diptipradeep
 as part of the Sentiment Analysis Tool open-source project.