def form_fill(form):
    form.birth_date.month.data = 'January'
    form.birth_date.day.data = '13'
    form.birth_date.year.data = '1992'
    form.name.last.data = 'Hennessy'
    form.name.first.data = "O'Shack"
    form.name.initial.data = 'D'
    form.address.addr_num.data = '1234'
    form.address.street.data = 'Aaron Street'
    form.address.apt_num.data = '23'
    form.address.city.data = 'Oakland'
    form.address.state.data = 'California'
    form.address.zip_code.data = '94610'
    form.phone.data = '510-555-1212'
    form.email.data = 'oshennessy@fake.org'

def mock_record():
    return {
        # "expirationDate": str(expiration_date) set to arbitrary past date,
        "expirationDate": '2001-01-01',
        "patronCodes": {
            # age level
            "pcode1": "1",
            # not used for online reg
            "pcode2": "-",
            # library jurisdiction
            "pcode3": 1
        },
        "varFields": [{
            # school
            "fieldTag": "c",
            "content": "SIERRA ELEMENTARY"
        },
                      {
                          # unique ID
                "fieldTag": "u",
                          "content": "CS{}".format(
                              datetime.now().strftime('%y%m%d%H%M%S'))
                      },
                      {
                          # parent name
                "fieldTag": "e",
                          "content": "TEST PARENT"
                      },
                      {
                          # language
                "fieldTag": "k",
                          "content": "MALTESE"
                      },
                      {
                          # self reg info
                "fieldTag": "d",
                          "content": "|t ID_PASSPORT"
                      },
        ]
        ,
        "patronType": 18,
        # "birthDate": str(birth_date),
        # dates should be in the format YYYY-MM-DD
        "birthDate": '2006-12-01',
        # Home Library
        "homeLibraryCode": 'xxa',
        "names": [
            'PATLASTNAME' + ', ' + 'PATFIRSTNAME' + ' ' + 'M'
        ],
        # 3 lines if apt number exists, else 2 lines
        "addresses": [{
            "lines": [
                '125 14TH ST',
                'APT 2',
                'OAKLAND, CA 94612'
            ],
            "type": "a"
        }],
        # format xxx-xxx-xxxx
        "phones": [{
            "number": '510-999-9999',
            "type": "t"
        }],
        "emails": [
            "devnullexplorer@aol.com"
        ],
    }

