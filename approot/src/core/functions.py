import os
import qrcode
from typing import OrderedDict
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

    img: qrcode = qrcode.make(data_str.strip())
    img.save(os.path.join(BASE_DIR, f'src/entities/qrcodes/qrcode_{pk}.png'))
