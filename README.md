# DataLens 📊

An AI-powered data analysis tool that lets you chat with your datasets using natural language. Upload CSV or Excel files and get instant insights through conversational AI.

## ✨ Features

- 🔐 Secure authentication with email verification
- 📁 Support for CSV and Excel (.xls, .xlsx) files
- 💬 Natural language queries powered by GPT-4o-mini
- 📊 Automatic data visualization
- 💾 Conversation history persistence
- 🔍 Interactive data preview

## 📖 User Guide

### Sign Up

1. Enter your email address and a strong password
   - Password must contain: special characters, numbers, and letters
2. Click **Sign Up**
3. Check your email inbox for a verification email from Supabase
4. Click the verification link to activate your account

### Login

1. Log in using your registered email and password

### Using the App

1. **Upload your data**
   - Supported formats: `.csv`, `.xls`, `.xlsx`
   
2. **Select a file**
   - Use the dropdown menu to select which file to preview (if you uploaded multiple files)
   
3. **Preview your data**
   - Enter the number of rows you want to preview

4. **Chat with your data**
   - Expand the **💬 Chat with your data** section
   - Type your question and wait for the AI to process it
   
   **Example questions:**
   - "How many rows are in this data?"
   - "Create a bar chart of [column name]"
   - "What is the average value of [column name]?"
   - "Show me the distribution of [column name]"

5. **Save your work**
   - Click **Log Out** before closing the app to save your conversation history

## 🛠️ Technology Stack

### Frontend
- Streamlit
- Pillow

### Backend
- Python
- PandasAI

### AI/ML
- OpenAI GPT-4o-mini
- PandasAI >= 3.0.0

### Database & Authentication
- Supabase

## 📁 Project Structure

```
App/
│
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── login.py           # Authentication logic
├── main.py            # Main application interface
├── bot.py             # PandasAI integration
└── security.py        # Security utilities
└── README.md          # You're here
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd data-lens
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

   **Getting API Keys:**
   - **OpenAI API Key**: 
     - Sign up at [OpenAI Platform](https://platform.openai.com/)
     - Navigate to API Keys section and create a new secret key
   - **Supabase Credentials**: 
     - Create an account at [Supabase](https://supabase.com/)
     - Create a new project
     - Copy URL and anon/public key from Project Settings → API

4. **Set up Supabase database**
   
   Create a `messages` table in your Supabase project:
   ```sql
   CREATE TABLE messages (
     id BIGSERIAL PRIMARY KEY,
     username TEXT NOT NULL,
     content TEXT NOT NULL,
     role TEXT NOT NULL,
     is_image BOOLEAN DEFAULT FALSE,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
   );

   -- Add index for faster queries
   CREATE INDEX idx_messages_username ON messages(username);
   ```

5. **Run the application**
   ```bash
   streamlit run login.py
   ```
   
   The application will open in your browser at `http://localhost:8501`