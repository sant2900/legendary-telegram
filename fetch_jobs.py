- name: Install Requests
      run: pip install requests

    - name: Run Job Scraper Bot
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python fetch_jobs.py
