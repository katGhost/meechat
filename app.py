


"""@chat_bp.route("/chat/<room>")
def chat_room(room):
    if "username" not in session:
        session["username"] = generate_guest_username()
        logger.info("Generated username: %s", session["username"])

    if room not in Config.CHAT_ROOMS:
        logger.warning("Attempt to access invalid room: %s", room)
        return "Room not found", 404

    return render_template(
        "chat_room.html",
        username=session["username"],
        room=room,
    )"""