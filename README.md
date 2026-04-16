# Online Restaurant Ordering System API

FastAPI backend for a restaurant ordering system.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload

How to run it in VS Code

Create virtual environment

Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate

Install packages:
pip install -r requirements.txt

Run the server:
uvicorn api.main:app --reload

## Make the MySQL database

In MySQL, run:

CREATE DATABASE sandwich_maker_api;

If your MySQL username/password is not root / password123, change it in:

api/dependencies/config.py
