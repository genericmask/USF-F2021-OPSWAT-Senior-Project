def turbo_flash(message):
    from flaskr import turbo
    from flask import render_template as template

    if turbo.can_stream():
        return turbo.stream(
            turbo.replace(
                template("_turbo_flashing.html.j2", message=message, category="error"),
                target="turbo-flash",
            )
        )
    else:
        return False