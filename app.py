from flask import Flask, request
import smtplib

app = Flask(__name__)

@app.route("/inbound", methods=["POST"])
def inbound():
    raw_message = request.form.get("body-mime")
    recipient = request.form.get("recipient")
    subject = request.form.get("subject")

    if not raw_message or not recipient:
        return "Missing data", 400

    print(f"Forwarding message to {recipient} with subject: {subject}")

    with smtplib.SMTP("68.70.225.173", 2525) as smtp:
        smtp.sendmail(
            from_addr="relay@brutomail.com",
            to_addrs=[recipient],
            msg=raw_message
        )
    return "OK", 200
