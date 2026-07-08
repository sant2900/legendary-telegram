import os
import requests
import json
import urllib.request
import re

def send_to_telegram(job_title, company, apply_url):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram credentials missing in secrets!")
        return

    message = (
        f"🚀 **NEW REMOTE JOB OPENING!**\n\n"
        f"📌 **Role:** {job_title}\n"
        f"🏢 **Company:** {company}\n\n"
        f"👉 **Apply via Global Career Hub (Click Below):**\n"
        f"🔗 https://sant2900.github.io/legendary-telegram/"
    )
    
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        # टेलीग्राम भेजने के लिए 10 सेकंड का timeout
        response = requests.post(telegram_url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"Successfully posted to Telegram: {job_title}")
        else:
            print(f"Failed to send to Telegram: {response.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

print("Fetching latest remote jobs...")

url = "https://remoteok.com/api"
# बढ़िया ब्राउज़र जैसा Headers ताकि API ब्लॉक न करे
req = urllib.request.Request(
    url, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
)

try:
    # यहाँ timeout=15 जोड़ा है ताकि API अटके तो 15 सेकंड में बंद हो जाए
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode())
        
    jobs = data[1:6]  # टॉप 5 लेटेस्ट जॉब्स
    
    jobs_html = ""
    for job in jobs:
        title = job.get('position', 'Remote Role')
        company = job.get('company', 'Global Tech')
        logo = job.get('logo', 'https://remoteok.com/assets/jobs/74021674485523.png')
        job_url = job.get('url', '#')
        tags = ", ".join(job.get('tags', [])[:3])
        
        jobs_html += f"""
        <div class="job-card">
            <img src="{logo}" alt="{company} Logo" onerror="this.src='https://via.placeholder.com/50?text=Job'">
            <div class="job-info">
                <h3>{title}</h3>
                <p class="company">{company} • <span style="color:#38bdf8;">{tags}</span></p>
            </div>
            <a href="{job_url}" target="_blank" class="apply-btn">Apply Now</a>
        </div>
        """
        
        send_to_telegram(title, company, job_url)
        
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        
    start_placeholder = "<!-- JOBS_START -->"
    end_placeholder = "<!-- JOBS_END -->"
    
    pattern = f"{start_placeholder}.*?{end_placeholder}"
    replacement = f"{start_placeholder}\n{jobs_html}\n{end_placeholder}"
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
        
    print("Success: Website updated and jobs sent to Telegram!")

except Exception as e:
    print(f"Error fetching jobs: {e}")
