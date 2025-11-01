from .base_agent import BaseAgent
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Dict, Any
import json


class WebScraperAgent(BaseAgent):
    """Agent 1: Scrapes web pages and extracts product/idea information."""

    def __init__(self):
        system_prompt = """You are an expert web content analyzer specializing in SaaS and web app products.

Your task is to analyze web page content and extract comprehensive information about the product or idea.

Extract and structure the following information:
1. Product/Idea Title
2. Description (2-3 sentences)
3. Key Features (list of features with descriptions)
4. Target Audience (who is this for?)
5. Value Proposition (main benefit/selling point)
6. Category (SaaS, web app, tool, platform, etc.)
7. Pain Points Addressed (what problems does it solve?)

Return your response as a valid JSON object with these keys:
{
    "title": "...",
    "description": "...",
    "features": ["feature1", "feature2", ...],
    "target_audience": "...",
    "value_proposition": "...",
    "category": "...",
    "pain_points": ["pain1", "pain2", ...]
}

Be thorough but concise. Focus on the core value and unique aspects."""

        super().__init__("WebScraperAgent", system_prompt)

    def scrape_url(self, url: str) -> str:
        """Use Playwright to scrape the web page."""
        self.log(f"Scraping URL: {url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=30000)

                # Wait a bit for dynamic content
                page.wait_for_timeout(2000)

                # Get the full HTML
                content = page.content()
                browser.close()

                # Parse with BeautifulSoup to clean it up
                soup = BeautifulSoup(content, 'lxml')

                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()

                # Get text
                text = soup.get_text()

                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)

                # Limit to reasonable size (GPT-4 context)
                text = text[:15000]

                self.log(f"Successfully scraped {len(text)} characters")
                return text

        except Exception as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a URL and extract product information.

        Input: {"url": "https://..."}
        Output: {"url": "...", "extracted_data": {...}, "raw_content": "..."}
        """
        url = input_data.get("url")
        if not url:
            raise ValueError("URL is required")

        # Scrape the page
        raw_content = self.scrape_url(url)

        # Analyze with GPT-4
        self.log("Analyzing content with GPT-4...")
        prompt = f"""Analyze the following web page content and extract product/idea information.

Web page content:
{raw_content}

Return the information as a valid JSON object as specified in your system prompt."""

        response = self.call_gpt(prompt, response_format="json_object")

        # Parse the JSON response
        try:
            extracted_data = json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse GPT-4 response as JSON")

        self.log(f"Successfully extracted data for: {extracted_data.get('title', 'Unknown')}")

        return {
            "url": url,
            "extracted_data": extracted_data,
            "raw_content": raw_content[:5000]  # Store limited raw content for reference
        }
