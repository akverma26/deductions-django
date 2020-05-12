from bs4 import BeautifulSoup

def get_context(content):
    linux_commands = []
    f= open(content, 'r').read()
    soup = BeautifulSoup(f, 'lxml')
    blocks = soup.find_all('block')
    for block in blocks:
        title = block.find('title').text
        commands = block.find_all('command')
        cm = []
        for command in commands:
            c = command.find('c').text
            i = command.find('i').text
            cm.append({'command': c, 'info': i})
        linux_commands.append({'title': title, 'commands': cm})

    return {'commands': linux_commands}