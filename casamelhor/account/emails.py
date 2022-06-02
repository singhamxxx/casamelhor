from templated_email import send_templated_mail


def get_email_context(user, url):
    return {
        "template_name": "account/confirm",
        "from_email": "sales.shubhan@gmail.com",
        "recipient_list": [user.email],
        "context": {
            'username': user.username,
            'full_name': user.get_full_name(),
            'url': url
        },
    }


def _send_account_confirmation_email(user, url):
    context = get_email_context(user, url)
    send_templated_mail(**context)
