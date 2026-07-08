import json
import urllib.request
import re

print("Fetching latest remote jobs...")

# 1. API से रिमोट जॉब्स का डेटा निकालना (फ्री API)
url = "https://remoteok.com/api"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    # पहले एलिमेंट में लीगल इंफॉर्मेशन होती है, उसे हटाकर सिर्फ जॉब्स लेंगे
    jobs = data[1:6]  # टॉप 5 लेटेस्ट जॉब्स
    
    jobs_html = ""
    for job in jobs:
        title = job.get('position', 'Remote Role')
        company = job.get('company', 'Global Tech')
        logo = job.get('logo', 'https://remoteok.com/assets/jobs/74021674485523.png')
        job_url = job.get('url', '#')
        tags = ", ".join(job.get('tags', [])[:3])
        
        # हर जॉब के लिए सुंदर कार्ड डिजाइन
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
        
    # 2. index.html फाइल को रीड करना और उसमें जॉब्स को अपडेट करना
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # पुराना जॉब सेक्शन हटाकर नया सेक्शन डालना
    start_placeholder = "<!-- JOBS_START -->"
    end_placeholder = "<!-- JOBS_END -->"
    
    pattern = f"{start_placeholder}.*?{end_placeholder}"
    replacement = f"{start_placeholder}\n{jobs_html}\n{end_placeholder}"
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
        
    print("Success: Website updated with latest jobs!")

except Exception as e:
    print(f"Error fetching jobs: {e}")
