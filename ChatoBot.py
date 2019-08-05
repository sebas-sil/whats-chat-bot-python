from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Firefox()
driver.get('http://web.whatsapp.com')
print('Please Scan the QR Code and press enter')
input()

week_days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Doming']


def compare(x):
    ret = x.value_of_css_property('transform')
    index = int(ret.rindex(' '))
    ret = int(ret[index + 1:-1])
    return ret


try:
    # pega a lista de contatos
    chats = driver.find_elements_by_xpath('.//div[@class="X7YrQ"]')
    # remove os chats não lidos (chats nao lidos tem um marcador númerico)
    chats = [c for c in chats if  not str(c.find_element_by_xpath('./div/div/div[2]/div[2]/div[2]/span').text).isnumeric()]

    for index, chat in enumerate(chats):
        name_txt = chat.find_element_by_xpath('./div/div/div[2]/div[1]/div').text
        date_txt = str(chat.find_element_by_xpath('./div/div/div[2]/div[1]/div[2]').text)
        print(index, date_txt, name_txt)

    chats = sorted(chats, key=compare)


    for index, chat in enumerate(chats):
        name_txt = chat.find_element_by_xpath('./div/div/div[2]/div[1]/div').text
        date_txt = str(chat.find_element_by_xpath('./div/div/div[2]/div[1]/div[2]').text)
        print(index, date_txt, name_txt)

    sleep(2)
    for index, chat in enumerate(chats):
        # clica sobre o chat para abrir a concersa
        chat.click()

        # clica na foto do perfil para abrir a janela de status do contato
        profile = driver.find_elements_by_xpath('.//header/div[1]')[1]
        profile.click()

        # pega o telefone para compor a chave primaria
        # grupos não tem essa configuracao
        try:
            sleep(2)
            name_span = chat.find_element_by_xpath('./div/div/div[2]/div[1]/div').text
            tel_span = driver.find_element_by_xpath('.//header/parent::div/div/div/div[4]/div[3]/div/div/span').text

            print(index, name_span, tel_span)
        except NoSuchElementException as err:
            print(index, name_span, 'grupo')

    actions = ActionChains(driver)
    actions.move_to_element(chats[-1])
    actions.perform()

    # pega os contatos que estao aparecendo na listagem na tela
    # chats = el.find_element_by_xpath('div/div[@tabindex=-1]/div')
    # for chat in chats:
    #     nome = chat.find_element_by_xpath('div[1]')
    #     print(f'nome: {}')

    while True:

        try:
            xpath = input('digite o xpath: ')
            el = chat.find_element_by_xpath(xpath)
            print(f'{el.text}')
            print('-' * 20)

        except Exception as er:
            print(er)
        # content.click()
        # input_form = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
        # print(f'form: {input_form}')
        # v = input_form.send_keys(str(datetime.now()),Keys.RETURN)
        # print(f'v: {v}')
except NoSuchElementException as err:
    print(err)
    pass
