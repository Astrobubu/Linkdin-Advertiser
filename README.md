# LinkedIn Advertiser - AI-Powered Multi-Agent System

An intelligent LinkedIn content generation system that uses a multi-agent pipeline powered by GPT-4 to analyze your products and generate highly engaging, viral-optimized LinkedIn posts.

## 🚀 Features

### Multi-Agent Pipeline
1. **Agent 1: Web Scraper & Extractor**
   - Uses Playwright to scrape product pages
   - Extracts features, value props, and target audience
   - Powered by GPT-4 for intelligent extraction

2. **Agent 2: Deep Analyzer**
   - Market analysis and positioning
   - Uniqueness scoring (0-10)
   - Target persona identification
   - LinkedIn content angle suggestions

3. **Agent 3: Critic & Refiner**
   - Critical evaluation of analysis
   - Identifies weaknesses
   - **Intelligent Looping**: Automatically triggers re-analysis if quality is insufficient
   - Uses keyword triggers: `needs_refinement`, `unclear_value_prop`, `iterate`, etc.

4. **Agent 4: Post Generator**
   - Generates 7-10 LinkedIn post variations
   - Text posts, carousel concepts, and video scripts
   - Optimal timing based on 2025 research (Tuesday-Thursday, 9-11 AM, 12 PM)
   - Hook-Body-CTA structure optimized for engagement

### Based on Real LinkedIn Research (2025)
- Carousel posts: 45.85% engagement rate
- Optimal posting times: Tuesday-Thursday, 9-11 AM and noon
- 150-300 word posts perform best
- First 2 lines are critical (only part visible in feed)
- Personal stories + data-driven insights = highest engagement

### Tech Stack
**Backend:**
- Python 3.11+
- FastAPI
- OpenAI GPT-4
- Playwright (web scraping)
- SQLAlchemy + SQLite

**Frontend:**
- Next.js 14
- React
- TypeScript
- TailwindCSS
- Axios

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- OpenAI API key (GPT-4 access)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Linkdin-Advertiser
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Initialize database
python -c "from database import init_db; init_db()"
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

### 4. Environment Variables

The `.env` file has already been created with your OpenAI API key. Verify it exists:

```bash
# Backend .env (already configured)
cat ../.env
```

Frontend `.env.local` (already configured):
```bash
cat .env.local
```

## 🚀 Running the Application

### Start Backend Server

```bash
# From the backend directory
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

Backend will run on `http://localhost:8000`

### Start Frontend

```bash
# From the frontend directory (in a new terminal)
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📖 Usage

1. **Open the web interface** at `http://localhost:3000`

2. **Analyze a product:**
   - Enter your product URL (e.g., `https://your-saas-product.com`)
   - Click "Analyze & Generate Posts"
   - Wait 30-60 seconds for the multi-agent pipeline to complete

3. **Review the results:**
   - See market and uniqueness scores
   - Review target audience analysis
   - View 7-10 generated LinkedIn posts with optimal timing

4. **Copy and schedule posts:**
   - Click "Copy Post" for any generated post
   - Post on LinkedIn at the suggested date/time
   - Track engagement

## 🔄 How the Multi-Agent Loop Works

The system uses intelligent looping to ensure high-quality analysis:

```
URL Input → Agent 1 (Scrape) → Agent 2 (Analyze) → Agent 3 (Critique)
                                       ↑                    ↓
                                       └────[Loop if needed]────┘
                                                 ↓
                                          Agent 4 (Generate Posts)
```

**Loop Triggers:**
- Agent 3 detects quality issues using keywords
- Maximum 3 iterations to prevent infinite loops
- Each iteration improves analysis based on critique

## 📊 API Endpoints

### `POST /api/analyze`
Analyze a product URL and generate posts
```json
{
  "url": "https://your-product.com"
}
```

### `GET /api/ideas`
Get all analyzed products

### `GET /api/ideas/{idea_id}`
Get detailed information about a specific product

### `GET /api/posts/{idea_id}`
Get all generated posts for a product

### `DELETE /api/ideas/{idea_id}`
Delete a product and all its posts

## 🎯 Best Practices

### For Best Results:
1. Use product landing pages with clear value propositions
2. Pages with feature lists and benefits work best
3. Include target audience information on your page
4. B2B SaaS products get the best analysis

### Post Scheduling Tips:
- Follow the suggested timing (Tuesday-Thursday, 9-11 AM)
- Space posts 2-3 days apart
- Mix post types (text, carousel, video)
- Engage with comments in the first 60-90 minutes

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# OpenAI settings
openai_model = "gpt-4-turbo-preview"  # or "gpt-4", "gpt-4o"
openai_temperature = 0.7

# Agent settings
max_loop_iterations = 3  # Max times Agent 3 can trigger a loop
loop_keywords = [
    "needs_refinement",
    "unclear_value_prop",
    "iterate",
    "needs_improvement"
]
```

## 📁 Project Structure

```
Linkdin-Advertiser/
├── backend/
│   ├── agents/
│   │   ├── base_agent.py          # Base agent class
│   │   ├── agent1_scraper.py      # Web scraper agent
│   │   ├── agent2_analyzer.py     # Analysis agent
│   │   ├── agent3_critic.py       # Critic agent (with looping)
│   │   └── agent4_post_generator.py # Post generation agent
│   ├── config.py                  # Configuration
│   ├── database.py                # SQLAlchemy models
│   ├── orchestrator.py            # Pipeline orchestrator
│   ├── main.py                    # FastAPI server
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Main page
│   │   ├── layout.tsx             # Layout
│   │   └── globals.css
│   ├── components/
│   │   ├── AnalyzeForm.tsx        # URL input form
│   │   ├── IdeaList.tsx           # Product list sidebar
│   │   └── IdeaDetails.tsx        # Post display
│   └── package.json
├── .env                           # Backend environment variables
└── README.md
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify Python version: `python --version` (should be 3.11+)
- Ensure virtual environment is activated
- Check `.env` file exists with OpenAI API key

### Frontend won't start
- Check if port 3000 is available
- Verify Node version: `node --version` (should be 18+)
- Run `npm install` again
- Check `.env.local` has correct API URL

### Playwright errors
```bash
playwright install chromium
```

### Database errors
```bash
# Reinitialize database
cd backend
python -c "from database import init_db; init_db()"
```

## 📈 Future Enhancements

- [ ] Add image generation for carousel posts
- [ ] LinkedIn API integration for direct posting
- [ ] A/B testing framework
- [ ] Analytics dashboard
- [ ] Multi-product comparison
- [ ] Content calendar view
- [ ] Engagement prediction ML model
- [ ] Support for other platforms (Twitter, Medium)

## 📝 License

MIT License

## 🙏 Acknowledgments

Built on research from:
- Sprout Social's 2025 LinkedIn Best Times report
- Analysis of 1,884 LinkedIn posts with AI
- LinkedIn algorithm insights from Hootsuite
- SaaS content strategies from Assembly

---

**Built with GPT-4 • Multi-Agent Architecture • Optimized for 2025**
