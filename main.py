import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
import os

from utils import encode_image_to_base64, get_mime_type

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@cl.on_chat_start
async def start():
    await cl.Message(content="""
📈 Welcome to the **Crypto Q&A & Chart Explainer Agent**!

---

🙋‍♂️ **Ask me anything about:**
- 📖 Blockchain Basics  
- 🪙 Bitcoin, Ethereum, Altcoins  
- 📊 Technical Analysis  
- 💰 Trading Strategies  
- 🧠 DeFi, NFTs, Web3  
- 📉 Market Trends, Whales, Price Predictions
- 📸 Add image for chart details

Go ahead and try it!
""").send()


@cl.on_message
async def handle_message(message: cl.Message):
    try:
        user_prompt = message.content.strip()
        image = message.elements[0] if message.elements else None

        if image:
            image_data = encode_image_to_base64(image.path)
            mime_type = get_mime_type(image.path)

            instruction = (
                "You are a professional crypto chart analyst. The user uploaded a chart image from TradingView. "
                "Explain the trend (bullish/bearish), visible patterns (e.g., flag, wedge), and indicators like MACD, RSI, EMA, volume. "
                "Give a beginner-friendly explanation.\n"
            )
            final_prompt = instruction + f"\nUser prompt: {user_prompt}" if user_prompt else instruction
            response = model.generate_content([
                final_prompt,
                {"mime_type": mime_type, "data": image_data}
            ])

            await cl.Message(content="📊 Chart Insight:\n\n" + response.text).send()

        else:
            response = model.generate_content(user_prompt)
            await cl.Message(content=response.text).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {e}").send()
