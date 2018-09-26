from fpdf import FPDF
import secrets

class Report(FPDF):
    def header(self):
        # Logo
        self.image('favicon.png', 10, 8, 8)
        # Arial bold 15
        self.set_font('Arial', '', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(10, 5, 'Análises de Séries Temporais - %s' % (self.title), 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, data):
        #Identify if it's the results chapter or the parameters chapter

        if data:
            model_param = data[0]
            readdata_param = data[1]

            string1 = 'Parâmetros do Modelo \n'
            for elem in model_param:
                string1 = string1 + '%s: %s\n' % (elem, model_param[elem])

            string2 = 'Parâmetros para Leitura do Arquivo \n'
            for elem in readdata_param:
                string2 = string2 + '%s: %s\n' % (elem, readdata_param[elem])

            txt = string1 + '\n' + string2
            
            # Times 12
            self.set_font('Times', '', 12)
            # Output justified text
            self.multi_cell(0, 5, txt)
            # Line break
            self.ln()
        else:
            pass

    def print_chapter(self, title, data, image):
        self.add_page()
        self.chapter_title(title)
        if data:
            self.chapter_body(data)
        elif image:
            self.image(image[1:], 10, 50, 190)


def create_report(title, model_param, readdata_param, images, file_title):
    report = Report()
    report.alias_nb_pages()
    report.set_title(title)

    # Dados de Entrada
    report.print_chapter('Dados de Entrada', data = [model_param, readdata_param], image = None)
    for image in images:
        report.print_chapter('Resultados - Gráficos',data = None, image = image)
    str_title = '%s_%s.pdf' % (file_title, secrets.token_hex(6))
    report.output('static/reports/'+str_title, 'F')

    return str_title
