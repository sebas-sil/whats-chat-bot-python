from os import path
from sys import exc_info

from selenium import webdriver
from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from datetime import datetime

"""
msg.txt: arquivo texto comum com uma listas de telefones. ex:
4199887766
4199876543
1199223344

mensagens de erro serão gravadas no arquivo log_err.log
se não for passado um caminho para a imagem, ele enviará o texto, caso contrário enviará a imagem
"""


def get_txt_box():
    sleep(10)
    ''' pega o text box para envio de mensagem'''
    txt_msg = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    return txt_msg


def get_wrong_number():
    ''' pega o text box para envio de mensagem'''
    try:
        element = driver.find_element_by_xpath('//div[div/div[@role="button"]]/div[1]')
        return 'inválido' in element.text
    except StaleElementReferenceException:
        try:
            element = driver.find_element_by_xpath('//div[div/div[@role="button"]]/div[1]')
            return 'inválido' in element.text
        except NoSuchElementException:
            return False
    except NoSuchElementException:
        return False


# load Chrome drive
driver = webdriver.Chrome()
driver.get('http://web.whatsapp.com')

# v1.0.2: correcao do encode de leitura e multiplas linhas de mensagem
# v1.0.3: correcao de excecoes no laço de repeticao de envio de mensagem para nao para-la quando der err em um numero.
# v1.1.0: cria um arquivo de log com os erros
# v1.1.1: removidos os tempos de espera e corrigido erro para numero nao existe no whats
# v1.1.2: corrigido erro de alerta de saida da pagina
# v1.1.3: ignorado linhas vazias
# v1.1.4: tratamento do alerta do navegador quando a mensagem nao foi enviada antes do proximo numero ser chamado
# v1.1.5: adicionado hardcoded o DDI do brasil no link e mais logs
# v1.2.0: adicionado confirmação de 'continuar pela web' ao enviar mensagesn
# v1.2.1: Acertado problema de nao carregar a tela de enviar mensagem por uma trava no Whatsapp
# v1.3.0: Adcionado envio de mensagens de imagem
print('v1.3.0')

f = open(file='msg.txt', encoding='utf8', mode='r')
msg = f.readlines()
f.close()

# type of message
img_path = input('Image path: ')
input('Please Scan the QR Code and press enter')

e = open(file='log_err.log', encoding='utf8', mode='a')

# read the list of  phone numbers
f = open('list.txt', 'r')
content = f.readlines()

# para cada numero na lista
for i, phone in enumerate(content):
    try:
        phone = phone.strip()
        if len(phone) == 0:
            continue
        url = 'https://web.whatsapp.com/send?phone=55' + phone
        print(url)
        driver.get(url)

        is_wrong = False
        was_sent = False
        stop_when = 0
        # continue tentando enquanto nao for numero invalido ou conseguir pegar a caixa de texto
        while not is_wrong and not was_sent:
            stop_when += 1
            if stop_when > 10:
                raise Exception('Too many tries')
            try:
                if(len(img_path) == 0):
                    txt_msg = get_txt_box()
                    for message in msg:
                        txt_msg.send_keys(message.replace('\n', ''))
                        txt_msg.send_keys(Keys.SHIFT + Keys.ENTER)
                    txt_msg.send_keys(Keys.ENTER)
                    # tempo necessario para evitar alerta de "deseja sair sem salvar"
                    sleep(1)
                else:
                    # clica no botão de enviar anexo
                    sleep(1)
                    inp_img = driver.find_element_by_xpath("//div[@role='button' and @title='Anexar']")
                    inp_img.click()
                    # clica no botão enviar imagem
                    sleep(1)
                    inp_img = driver.find_elements_by_xpath("//input[@type='file']")[0]
                    inp_img.send_keys(img_path)
                    # escreve uam descrição para a imagem
                    sleep(1)
                    inp_desc = driver.find_elements_by_xpath("//div[@class='_3u328 copyable-text selectable-text']")[0]
                    inp_desc.send_keys('Enviado por Unidade Escola UTFPR - Nutrição Esportiva')
                    # clica em enviar
                    inp_img = driver.find_element_by_xpath("//span[@data-icon='send-light']")
                    inp_img.click()
                    sleep(2)
                was_sent = True

            except NoSuchElementException as err:
                print(stop_when, 'trying to get the textbox')
                sleep(1)
                is_wrong = get_wrong_number()
        if is_wrong:
            is_wrong = False
            raise Exception('Number is not a whats client')
    except Exception as err:
        exc_type, exc_obj, exc_tb = exc_info()
        fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(i + 1, phone, exc_type, fname, exc_tb.tb_lineno)
        e.write(f'[{datetime.now()}]\t[{i + 1}\t{phone}]\t[{exc_type}]\t[{str(err).replace(chr(10), "")}]\t[{fname} ({exc_tb.tb_lineno})]\n')

e.close()
print('FIM')