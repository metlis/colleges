class Seo():

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {'city': 'Colleges and universities in {}, {}',
                     'ownership': '{} colleges and universities in {}',
                     'degree': 'Colleges and universities with {} as the highest in {}',
                     'religion': '{} colleges and universities in {}',
                     'level': 'Colleges and universities of {} institutional level in {}',
                     }

        template = templates[key]
        return template.format(value, geo)