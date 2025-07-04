from flask import Flask, request
import smtplib

app = Flask(__name__)

@app.route("/hook", methods=["POST"])
@app.route("/hook/", methods=["POST"])
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
@app.route("/", methods=["GET", "POST"])
def root():
    return "App is alive", 200
if __name__ != "__main__":
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
@app.before_request
def log_request_info():
    print(f"Incoming request: {request.method} {request.path}")
@app.errorhandler(404)
def not_found(e):
    return f"Custom 404: {request.method} {request.path}", 404
