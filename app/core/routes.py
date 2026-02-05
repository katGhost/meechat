from datetime import datetime
import random
from flask import request, render_template, redirect, url_for, session, flash
from app.core import core

def generate_guest_username() -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"Guest-{ts}-{random.randint(1000, 9999)}"


@core.route('/')
def home():
    session.clear()

    if 'username' not in session:
        session['username'] = generate_guest_username()
        flash(f"Assigned guest username: {session['username']}", 'info')
    return render_template(
        'core/home.html',
        username=session['username'] if 'username' in session else None
    )