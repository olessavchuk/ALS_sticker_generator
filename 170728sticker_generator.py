import os, re
from datetime import date
from time import sleep





def generate_sticker(sticker_directory, template, date, sign):
    file_endings = ['aux', 'log', 'tex'] #File types to delete after LaTeX compilation.

    with open(template, 'r') as f:
        tex_text = f.read()
    print(tex_text)

    tex_text = tex_text.replace('[DATE]', '{0}'.format(date))
    tex_text = tex_text.replace('[SIGN]', '{0}'.format(sign))

    with open(os.path.join(sticker_directory, '{0}_{1}.tex'.format(date, sign.replace('å','a'))), 'w') as f:
        f.write(tex_text)

    for f in os.listdir(sticker_directory):
        if '.tex' in f:
            os.system('pdflatex  {0} ;'.format(f))

    for f in file_endings:
        os.system('del {0}_{1}.{2}'.format(date, sign, f))


#TODO
def cleanup(end_of_day=False):
    pass


def remove_old_files(date_today, sticker_directories):
    for d in sticker_directories:
        try:
            os.chdir(d)
            files = os.listdir(d)
            for f in files:
                if f.endswith('.pdf') == True and f.startswith(date_today) == False:
                    os.system('del {0}'.format(f))
        except FileNotFoundError:
            pass


def main():
    signs = ['asah', 'rosa', 'nive', 'yvwi', 'late', 'nema', 'masu', 'liso', 'atja', 'misw', 'olsa', 'syku', 'kaso', 'yaya']
    #Stopped working at ALS, went back to Australia.:   'mael'
    #Long time leave:                                   'naka'

    templ_path = 'F:/PUBLIC/ROUZBEH/python_prog/sticker_generator/templ'
    templates = [os.path.join(templ_path, f) for f in os.listdir(templ_path) if f.endswith('.tex') == True]

    sticker_base_directory = 'F:/PUBLIC/ROUZBEH/stickers/'
    sticker_directories = [os.path.join(sticker_base_directory, os.path.basename(templ_path)[:-4]) for templ_path in
                           templates]

    while True:
        date_today = date.today().strftime('%Y%m%d')
        remove_old_files(date_today, sticker_directories)

        for t in templates:
            folder_name = os.path.basename(t)[:-4]
            sticker_directory = os.path.join(sticker_base_directory, folder_name)

            if os.path.exists(sticker_directory):
                os.chdir(sticker_directory)
            else:
                os.mkdir(sticker_directory)
                os.chdir(sticker_directory)

            for s in signs:
                generate_sticker(sticker_directory, t, date_today, s)

        while date_today == str(date.today()).replace('-', ''):
            sleep(3600)

        for d in sticker_directories:
            pass




main()