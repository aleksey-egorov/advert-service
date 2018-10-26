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
    ]
}

EMAIL_SIGN = '<br><br>Администрация Advert'