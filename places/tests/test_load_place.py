import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from places.models import Place


class LoadPlaceTestCase(TestCase):
    def setUp(self) -> None:
        self.url_1 = 'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/' \
                '%D0%90%D0%BD%D1%82%D0%B8%D0%BA%D0%B0%D1%84%D0%B5%20Bizone.json'
        self.url_2 = 'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/' \
                '%D0%90%D1%80%D1%82-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82' \
                '%D0%B2%D0%BE%20%C2%AB%D0%91%D1%83%D0%BD%D0%BA%D0%B5%D1%80%20703%C2%BB.json'
        self.JSONs_to_load = {
            self.url_1: '''
            {
                "title": "Антикафе Bizone",
                "imgs": [
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1f09226ae0edf23d20708b4fcc498ffd.jpg",
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/6e1c15fd7723e04e73985486c441e061.jpg",
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/be067a44fb19342c562e9ffd815c4215.jpg",
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/f6148bf3acf5328347f2762a1a674620.jpg",
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b896253e3b4f092cff47a02885450b5c.jpg",
                    "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/605da4a5bc8fd9a748526bef3b02120f.jpg"
                ],
                "description_short": "Настольные и компьютерные игры, виртуальная реальность и насыщенная программа мероприятий — новое антикафе Bizone предлагает два уровня удовольствий для вашего уединённого отдыха или радостных встреч с родными, друзьями, коллегами.",
                "description_long": "<p>Рядом со станцией метро «Войковская» открылось антикафе Bizone, в котором создание качественного отдыха стало делом жизни для всей команды. Создатели разделили пространство на две зоны, одна из которых доступна для всех посетителей, вторая — только для совершеннолетних гостей.</p><p>В Bizone вы платите исключительно за время посещения. В стоимость уже включены напитки, сладкие угощения, библиотека комиксов, большая коллекция популярных настольных и видеоигр. Также вы можете арендовать ВИП-зал для большой компании и погрузиться в мир виртуальной реальности с помощью специальных очков от топового производителя.</p><p>В течение недели организаторы проводят разнообразные встречи для меломанов и киноманов. Также можно присоединиться к английскому разговорному клубу или посетить образовательные лекции и мастер-классы. Летом организаторы запускают марафон настольных игр. Каждый день единомышленники собираются, чтобы порубиться в «Мафию», «Имаджинариум», Codenames, «Манчкин», Ticket to ride, «БЭНГ!» или «Колонизаторов». Точное расписание игр ищите в группе антикафе <a class=\"external-link\" href=\"https://vk.com/anticafebizone\" target=\"_blank\">«ВКонтакте»</a>.</p><p>Узнать больше об антикафе Bizone и забронировать стол вы можете <a class=\"external-link\" href=\"http://vbizone.ru/\" target=\"_blank\">на сайте</a> и <a class=\"external-link\" href=\"https://www.instagram.com/anticafe.bi.zone/\" target=\"_blank\">в Instagram</a>.</p>",
                "coordinates": {
                    "lng": "37.50169",
                    "lat": "55.816591"
                }
            }''',
            self.url_2: '''
            {
            "title": "Арт-пространство «Бункер 703»",
            "imgs": [
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/35cbdddf2799337d8b571d141edec616.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/9fec5106b0b52aa04667c4c9f4a2b622.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/32f0549e0af14659087719e072162bcd.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/e2bcb901757f5b7bf49c2820d09e5bea.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/75639a006a9fcffd304b8ef5e4f2812f.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/a27adfcfda93117f83711f71a7e54fd9.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b00507f1e14b77720e8e9eabb91cfc33.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/e73f6c12c9dbfaeb0a8d2420d4965e58.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/ea092237d318e15c9a2d96685fe2eabf.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/2a766585cca37aef29cc248f0445ce3e.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/ad149dd86d0c61709eb5922e47247d5c.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/78acafb9aca4ee8d317d4c59e46fbb56.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/65f044002c045d852d6263eff4676d45.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/6c8da6e947b4d4a2300c8c407579101d.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/001c31be31452f136e9af152c5666f46.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/42c874a96874a16d4fc6138804ca1fee.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/ce3685386dfad734fc034ab39472772b.jpg",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/95843658f18c16e869646b7e6f14fc32.JPG",
                "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/567f1e5c18fadcdd97f87cbd37570edd.JPG"
            ],
            "description_short": "«Бункер 703» — музей современной фортификации, расположенный на глубине 43 метров под землёй. Раньше здесь находился защищённый спецархив МИДа, где хранились документы особой государственной важности. Сегодня место сочетает в себе уникальный музей и креативное театральное пространство и открыто для посещения.",
            "description_long": "<p>Туристы и жители столицы, случайные прохожие и зеваки, прогуливаясь по улочкам Замоскворечья, даже не подозревают, что у них под ногами скрыт когда-то секретный «Бункер 703». И сегодня туда может спуститься любой желающий.</p><h3><strong>Узнаём историю таинственного бункера</strong></h3><p>Экскурсия в «Бункер 703» даёт возможность узнать, как в действительности устроена Москва ниже уровня земли</p><p>Музей современной фортификации «Бункер 703» находится в пространстве, где несколько десятилетий размещался защищённый спецархив Министерства иностранных дел. Архив создали во времена, когда появилось оружие массового поражения, — было необходимо защищать документы особой государственной важности. Их решили хранить в заглублённом сооружении, для чего и был построен бункер. </p><p>Ещё недавно здесь работали засекреченные эксперты и хранились важнейшие международные тайны нашей страны. Посетителей сюда допустили только в 2018 году, когда власти признали объект технически устаревшим.</p><p>За массивными защитными дверями скрывается аутентичное оборудование советских времён. Посетителям предстоит познакомиться с технологиями и артефактами фортификационного объекта, увидеть рабочие системы жизнеобеспечения, заглянуть в глубокую шахту сталинской эпохи.</p><p>Вы сможете прогуляться по чугунному тоннелю, похожему на те, по которым ходят поезда на кольцевой линии Московского метрополитена, и своими руками запустить сирену оповещения о ядерном нападении</p><p> </p><p>Ещё одна часть экспозиции — макеты защитных сооружений ядерной эпохи, спецоборудование и рассекреченные документы, в которых отражено, как создавались первые советские бункеры глубокого заложения.</p><p>Главный принцип музея — достоверность информации. Вокруг музея сложилось экспертное сообщество по современной подземной фортификации. В него вошли историки, инженеры, архивисты, тоннелестроители и спелестологи.</p><h3><strong>Спускаемся на 43 метра под землю</strong></h3><p>Внимание! Участники экскурсий спускаются на глубину 43 метров и поднимаются на поверхность пешком. Рассчитывайте свои силы</p><p> </p><p>Сегодня в бункере проходят экскурсии — обзорные, тематические, для взрослых и школьных групп. Вы можете выбрать подходящий для вас формат.</p><ul><li><strong>Стандартная экскурсия</strong></li></ul><p>После подробного осмотра бункера под руководством гида участникам выделяют свободное время, чтобы прогуляться по бункеру, сделать снимки или задать вопросы экскурсоводу. Экскурсия длится 70-80 минут и рассчитана на группу не более 12 человек.</p><ul><li><strong>Экскурсия для суровых технарей</strong></li></ul><p>Гид-инженер проведёт полную экскурсию по бункеру и расскажет об инженерных системах. Зачем нужны те или иные вентили, куда идёт столько кабелей, как открыть десятитонную дверь? Участники экскурсии узнают ответы на эти и другие вопросы и смогут сами запустить некоторые механизмы. Экскурсия проводится для небольшой группы и длится на 10-15 минут дольше стандартной.</p><ul><li><strong>Диггерская экскурсия</strong></li></ul><p>Экскурсия проходит в темноте с фонариками. Участникам предстоит почувствовать себя исследователями таинственных подземных пространств, познакомиться с субкультурой диггеров и узнать технические тонкости процесса. Вам расскажут, какие опасности могут ожидать исследователя под землёй и как с ними справляться.</p><ul><li><strong>English Tour</strong></li></ul><p>Экскурсия English Tour («Инглиш Тур») проходит на английском языке с переводом на русский, если это необходимо. Участники смогут проверить уровень радиации, разобрать автомат Калашникова, примерить защитный костюм и противогаз и посмотреть видео об истории подземной фортификации. Прогулка длится 70-80 минут и рассчитана на группу из 10-12 человек.</p><ul><li><strong>Экскурсия «Гражданская оборона»</strong></li></ul><p>Главная тема экскурсии — защита населения. Участники смогут осмотреть бункер, узнать, где укрыться от ядерного взрыва и как спастись от радиации и химического оружия, потренироваться проводить дозиметрическую разведку местности и пользоваться приборами связи и услышать сигнал воздушной тревоги. Экскурсия подходит для взрослых и детей.</p><ul><li><strong>Обзорная экскурсия</strong></li></ul><p>Эта программа подходит для больших групп — до 24 участников. Экскурсия проходит по тому же маршруту, что и стандартная, но дополнительное свободное время не предоставляется. Прогулка по бункеру длится 50-60 минут.</p><ul><li><strong>Школьная экскурсия</strong></li></ul><p>Программа адаптирована для детских групп от 20 человек. Можно заказать экскурсию в формате выездного урока по истории или ОБЖ, который проведёт профильный специалист. Экскурсия длится 50-70 минут. Стоимость — 15 тысяч рублей.</p><p>На территории «Бункера 703» можно увидеть не только спецприборы советских времён, но и современное искусство! Здесь расположился театр классического иммерсива «Бункер». Это театральная площадка инновационного формата — современные режиссёры и артисты театра и кино из Москвы и других городов России представляют свои работы в атмосфере секретного архива. Пространство бункера становится местом действия для самых разных постановок — от классики до современной драматургии.</p><p>Вскоре здесь планируют проводить и иммерсивные спектакли, в которых зритель сможет стать полноценным участником шоу и влиять на развитие сюжета. Такой формат разрушает границу между сценой и зрительным залом, действие будет разворачиваться вокруг вас, погружая в особый замкнутый мир «Бункера».</p><p>С театральным искусством в «Бункере 703» соседствует фотографическое. Здесь можно провести стильную и концептуальную фотосъёмку в аутентичном интерьере глубинного спецархива. Подземное пространство площадью 1000 метров готово принять самые смелые идеи для снимков.</p><p>Подробнее о «Бункере 703» узнавайте <a class=\"external-link\" href=\"https://www.gorod-bunker.ru/\" target=\"_blank\">на сайте</a>. За обновлениями следите <a class=\"external-link\" href=\"https://www.facebook.com/bunker703/?_rdc=1&amp;_rdr\" target=\"_blank\">в Facebook</a> или <a class=\"external-link\" href=\"https://www.instagram.com/bunker703/\" target=\"_blank\">в Instagram</a>.</p>",
            "coordinates": {
                "lng": "37.63032099999984",
                "lat": "55.73436900000009"
            }
        }
        '''
        }
        self.place_1_data = json.loads(self.JSONs_to_load[self.url_1])
        self.place_2_data = json.loads(self.JSONs_to_load[self.url_2])

    def call_command(self, *args, **options):
        out = StringIO()
        call_command(
            "load_place",
            self.url_1,
            *args,
            stdout=out,
            stderr=StringIO(),
            **options,
        )
        return out.getvalue()

    def test_load_one(self):
        out = self.call_command('load_place', self.url_1)
        place = Place.objects.get(title=self.place_dict['title'])
        self.assertIsNotNone(place)
        self.assertEqual(self.place_1_data['title'], place.title)
        self.assertEqual(self.place_1_data['description_short'], place.description_short)
        self.assertEqual(self.place_1_data['description_long'], place.description_long)
        self.assertEqual('Successfully loaded 1 places', out)
