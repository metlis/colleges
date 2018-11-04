class Seo():

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {'city': 'Colleges and universities in {}, {}, USA',
                     'ownership': '{} colleges and universities in {}, USA',
                     'degree': 'Colleges and universities with {} as the highest in {}, USA',
                     'religion': '{} colleges and universities in {}, USA',
                     'level': 'Colleges and universities of {} institutional level in {}, USA',
                     'carnegie': '{} in {}, USA',
                     }
        try:
            template = templates[key]
            return template.format(value, geo)
        except:
            return 'Colleges'