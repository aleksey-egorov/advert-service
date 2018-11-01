EMAIL_TEMPLATES = {
    'sign_up': [
        'Advert - registration',
        'Hello!<br>You are now signed up. Your login: <%LOGIN%> <br><br>'
    ],
    'brand_message': [
        'Помощь в подборе',
        '<table>\
          <tr><td>Имя:</td><td><%NAME%></td></tr>\
          <tr><td>Телефон:</td><td><%PHONE%></td></tr>\
          <tr><td>E-mail:</td><td><%EMAIL%></td></tr>\
          <tr><td>Сообщение:</td><td><%MESSAGE%></td></tr>\
        </table>'
    ],
    'supplier_message': [
        'Сообщение поставщику',
        '<table>\
          <tr><td>Имя:</td><td><%NAME%></td></tr>\
          <tr><td>Телефон:</td><td><%PHONE%></td></tr>\
          <tr><td>E-mail:</td><td><%EMAIL%></td></tr>\
          <tr><td>Сообщение:</td><td><%MESSAGE%></td></tr>\
        </table>'
    ],
    'credit_message': [
        'Заявка на покупку в кредит',
        '<table>\
          <tr><td>Имя:</td><td><%NAME%></td></tr>\
          <tr><td>Телефон:</td><td><%PHONE%></td></tr>\
          <tr><td>E-mail:</td><td><%EMAIL%></td></tr>\
        </table>'
    ],
    'leasing_message': [
        'Заявка на лизинг',
        '<table>\
          <tr><td>Имя:</td><td><%NAME%></td></tr>\
          <tr><td>Телефон:</td><td><%PHONE%></td></tr>\
          <tr><td>E-mail:</td><td><%EMAIL%></td></tr>\
          <tr><td>Авансовый платеж:</td><td><%PREPAYMENT%></td></tr>\
        </table>'
    ],
    'rent_message': [
        'Заявка на аренду',
        '<table>\
          <tr><td>Имя:</td><td><%NAME%></td></tr>\
          <tr><td>Телефон:</td><td><%PHONE%></td></tr>\
          <tr><td>E-mail:</td><td><%EMAIL%></td></tr>\
        </table>'
    ]
}

EMAIL_SIGN = '<br><br>Администрация Advert'