# Firebase Backup Script with RAID 1 Setup

## Overview
This project includes:
- A Node.js script to back up Firebase Realtime Database data.
- RAID 1 setup instructions to ensure data redundancy.

## Setup
1. Clone this repository:
git clone <repository-url>
2. Install dependencies:
npm install
3. Add your `serviceAccountKey.json` file (not included in the repository).
4. Run the script:
npm start

## Crontab Automation
Add the following line to your crontab to automate backups daily at midnight:
0 0 * * * /usr/bin/node /path-to-project/index.js