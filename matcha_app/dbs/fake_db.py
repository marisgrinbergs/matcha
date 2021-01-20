class FakeDb:

    data = [
            {'email': 'trponess@hotmail.com', 'profile': {
                                        'first_name': 'tristan',
                                        'last_name': 'superstar',
                                        'location': 'Mars',
                                        'msgs': [
                                                {'date': '14/08/2014 10:45:06', 'to_email': 'mariafox@hotmail.com', 'msg': 'hi your my friend bye'},
                                                {'date': '22/01/2002 19:23:06', 'to_email': 'mariafox@hotmail.com', 'msg': 'hi hi hi'},
                                                {'date': '19/08/2009 02:45:06', 'to_email': 'unknown@hotmail.com', 'msg': 'whats up'}
                                                ],
                                        'email' : 'trponess@hotmail.com',
                                        'likes': ['mariafox@hotmail.com', 'unknown@hotmail.com'],
                                        'pics': {'profile' : './matcha_app/static/pics/1.jpg', 'other' : []},
                                        'birthdate': '17/03/95',
                                        'gender': 'male',
                                        'sex_ori' : 'straight',
                                        'tags': ['C++','power'],
                                        'intro': 'im a GOD',
                                        'signed_in': False,
                                        'blocked': False,
                                        'activated': True,
                                        'pwd' : '1234'
                                }
            },

            {'email': 'mariafox@hotmail.com', 'profile': {
                                        'first_name': 'Maria',
                                        'last_name': 'Fox',
                                        'location': 'Mars',
                                        'msgs': [
                                                {'date': '14/08/2014 11:00:00', 'to_email': 'mariafox@hotmail.com', 'msg': 'hiiiiiiiiiii'},
                                                {'date': '22/01/2002 04:18:56', 'to_email': 'trponess@hotmail.com', 'msg': 'dig it'},
                                                {'date': '19/08/2009 00:00:05', 'to_email': 'unknown@hotmail.com', 'msg': 'i dont know'}
                                                ],
                                        'email': 'mariafox@hotmail.com',
                                        'likes': ['trponess@hotmail.com', 'unknown@hotmail.com'],
                                        'pics': {'profile': './matcha_app/static/pics/c.png', 'other': ['./matcha_app/static/pics/2.png']},
                                        'birthdate': '01/06/96',
                                        'gender': 'female',
                                        'sex_ori': 'straight',
                                        'tags': ['Java', 'AVGN'],
                                        'intro': 'im a GODDESS',
                                        'signed_in': False,
                                        'blocked': False,
                                        'activated': True,
                                        'pwd': '0000'
                                }
            }

    ]

def search_profile(info):
    for i in range(len(FakeDb.data)):
        dct = FakeDb.data[i]['profile']
        if is_sub_dict(info, dct):
            return dct

def is_sub_dict(dct, sub_dct):
    match = 0
    for k,v in sub_dct.items():
        if dct[k] == v:
            match += 1
    if len(sub_dct) == match:
        return True

def exec_cmd(cmd, *args):

    if cmd == 'insert':
        profile_dct = args
        FakeDb.data.append(profile_dct)
    if cmd == 'delete':
        email = args
        p = search_profile(email)
        FakeDb.data.remove(p)
    if cmd == 'get':
        info_dct = args
        return FakeDb.data.copy()

def init():






