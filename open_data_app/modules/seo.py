class Seo():

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {'city': 'Colleges and universities in {}, {}, USA',
                     'ownership': '{} colleges and universities in {}, USA',
                     'degree': 'Colleges and universities with {} as the highest in {}, USA',
                     'religion': '{} colleges and universities in {}, USA',
                     'level': 'Colleges and universities of {} institutional level in {}, USA',
                     'carnegie': '{} in {}, USA',
                     'locale': '{} colleges and universities in {}, USA',
                     'state': 'Colleges and universities in {}, {}, USA',
                     'hist_black': '{} colleges and universities in {}, USA',
                     'predom_black': '{} colleges and universities in {}, USA',
                     'men_only': '{} colleges and universities in {}, USA',
                     'women_only': '{} colleges and universities in {}, USA',
                     'online_only': '{} colleges and universities in {}, USA',
                     'cur_operating': '{} colleges and universities in {}, USA',
                     }
        try:
            template = templates[key]
            return template.format(value, geo)
        except:
            return 'Colleges'