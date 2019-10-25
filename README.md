# ldap_api_python

What this project does:
1. Send HTTP request to get employees list or Active Directory groups
2. This project connects to Directory System Agent (DSA) via LDAP (Lightweight Directory Access Protocol) and retrieves response
3. Project modifies recieved data to suitable data structures and sends them back to HTTP request

Tech Stack:
- Django 2.2.6
- Django REST Framework 3.10.3
- python-ldap 3.2
