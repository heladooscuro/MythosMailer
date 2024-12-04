# MythosMailer
Simple API for storing and send mails by making API calls



Example call with data 

        curl -X POST http://127.0.0.1:5000/send-email \
        -H "Content-Type: application/json" \
        -d '{
        "recipient": "destinatario@example.com",
        "subject": "Bienvenido a MythosMailer",
        "template_name": "welcome.html",
        "variables": {
            "name": "Juan",
            "welcome_message": "Estamos emocionados de tenerte con nosotros",
            "footer": "Gracias por unirte a nuestra comunidad"
        },
        "language": "es",
        "test_mode": true
        }'


{
    "recipient": "destinatario@example.com",
    "subject": "Welcome to MythosMailer",
    "template_name": "welcome.html",
    "variables": {
        "name": "Juan",
        "welcome_message": "We are thrilled to have you here!",
        "footer": "Thanks for joining us. MythosMailer Team."
    },
    "language": "en",
    "test_mode": true
}




Run tests

pytest --cov=.


Run app
python app.py