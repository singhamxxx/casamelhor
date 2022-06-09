from templated_email import send_templated_mail


def get_email_context(user, otp=None, url=None):
    return {
        "template_name": "account/confirm",
        # "from_email": "sales.shubhan@gmail.com",
        "recipient_list": [user.email],
        "context": {
            'full_name': user.get_full_name(),
            'otp': otp,
            'url': url
        },
    }


def _send_account_confirmation_email(user, otp=None, url=None):
    context = get_email_context(user, otp, url)
    send_templated_mail(**context)
