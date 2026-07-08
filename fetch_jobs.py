import requests
import json

def fetch_remote_jobs():
    print("Fetching jobs from remote API...")
    # Remote jobs ke liye public API call
    url = "https://www.arbeitnow.com/api/job-board-api"
    
    try:
        response = requests.get(url, headers={"User-Agent": "GlobalCareerHubBot/1.0"})
        if response.status_code == 200:
            data = response.json()
            raw_jobs = data.get('data', [])
            
            jobs_list = []
            # Sirf top 10 fresh jobs ko filter karna
            for job in raw_jobs[:10]:
                job_data = {
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": "Remote (" + job.get("location", "Global") + ")",
                    "url": job.get("url"),
                    "logo": "https://via.placeholder.com/50/1e293b/38bdf8?text=" + job.get("company_name")[0] # Default clean logo placeholder
                }
                jobs_list.append(job_data)
            
            # jobs.json file me data write karna
            with open("jobs.json", "w", encoding="utf-8") as f:
                json.dump(jobs_list, f, indent=4)
                
            print(f"Success! Saved {len(jobs_list)} jobs to jobs.json")
        else:
            print(f"Failed to fetch jobs. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_remote_jobs()
