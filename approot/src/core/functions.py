import os
import qrcode
from typing import OrderedDict
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from rest_framework.exceptions import ValidationError
from config.settings import BASE_DIR


def make_qrcode(serializer_data: OrderedDict, pk: int) -> None:
    """ Generates and saves QR code image. """

    data_list: list = []

    for key, value in dict(serializer_data).items():
        data_list.append(value)

    address_dict: dict = dict(data_list[1])
    data_list.pop()

    for value in address_dict.values():
        data_list.append(value)

    data_str: str = f'email: {data_list[0]}\n' \
                    f'country: {data_list[1]}\n' \
                    f'city: {data_list[2]}\n' \
                    f'street: {data_list[3]}\n' \
                    f'house: {data_list[4]}\n'

    image: qrcode = qrcode.make(data_str.strip())
    image.save(os.path.join(BASE_DIR, f'src/entities/qrcodes/qrcode_{pk}.png'))


def send(user_email, pk):
    """ Sends email to request user with QR code image. """

    if user_email is None:
        raise ValidationError({"detail": "Set email in your account to get QR code to your email."})

    html_content = \
        f"""
        <!doctype html>
            <html lang=en>
                <head>
                    <meta charset=utf-8>
                    <title>Some title.</title>
                </head>
                <body>
                    <p>
                    Here is my nice image.<br>
                    <img src='cid:qrcode_{pk}.png'/>
                    </p>
                </body>
            </html>
        """

    email = EmailMultiAlternatives(subject='QR code', body='QR code', to=(user_email,))

    email.attach_alternative(html_content, "text/html")
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'

    with open(os.path.join(BASE_DIR, f'src/entities/qrcodes/qrcode_{pk}.png'), mode='rb') as file:
        image = MIMEImage(file.read())
        email.attach(image)

    email.send()
