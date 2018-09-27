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
            quality_param = data[2]
            summary_param = data[3]

            self.set_font('Arial', 'B', 10)
            row_height = 1.05* self.font_size

            col_width_model = [self.w /3, self.w /8]
            col_width_readdata = [self.w /6, self.w /8]
            col_width_quality = [self.w /2.5, self.w /8]
            col_width_summary = self.w / 7

            # Params do modelo
            self.set_font('Arial', 'B', 10)
            self.cell(0, row_height, 'Parâmetros do Modelo')
            self.ln(row_height)

            self.set_font('Arial', '', 10)
            for row in model_param:
                for i in [0,1]:
                    self.cell(col_width_model[i], row_height,
                             txt=row[i], border=1)
                self.ln()
            self.ln(5)

            # Params da leitura do arquivo
            self.set_font('Arial', 'B', 10)
            self.cell(0, row_height, 'Parâmetros para Leitura do Arquivo \n\n')
            self.ln(row_height)

            self.set_font('Arial', '', 10)
            for row in readdata_param:
                for i in [0,1]:
                    self.cell(col_width_readdata[i], row_height,
                             txt=row[i], border=1)
                self.ln()
            self.ln(5)

            # Params da Qualidade dos Dados de Entrada
            self.set_font('Arial', 'B', 10)
            self.cell(0, row_height, 'Qualidade dos Dados de Entrada \n\n')
            self.ln(row_height)

            self.set_font('Arial', '', 10)
            for row in quality_param:
                for i in [0,1]:
                    self.cell(col_width_quality[i], row_height,
                             txt=row[i], border=1)
                self.ln()
            self.ln(5)

            # Params da sumarização
            self.set_font('Arial', 'B', 10)
            self.cell(0, row_height, 'Sumarização da série principal \n\n')
            self.ln(row_height)

            self.set_font('Arial', '', 10)
            k = 0
            for row in summary_param:
                if k == 2:
                    self.ln(3)

                for item in row:
                    self.cell(col_width_summary, row_height,
                             txt=item, border=1)
                self.ln()
                k = k+1
            self.ln()

            self.set_font('Arial', 'I', 7)
            self.set_text_color(80,80,80)
            av1 = '(1) IQR (inter-quantile range) = 1.5 * (Q75 - Q25) \n'
            av2 = '(2) LBO (lower bound outliers) = quantidade de valores menores que (Q25 - IQR) \n'
            av3 = '(3) UBO (upper bound outliers) = quantidade de valores maiores que (Q75 + IQR) \n'

            self.multi_cell(0, self.font_size, av1+av2+av3)

        else:
            pass

    def print_chapter(self, title, data, image):
        self.add_page()
        self.chapter_title(title)
        if data:
            self.chapter_body(data)
        elif image:
            self.image(image[1:], 10, 50, 190)


def create_report(title, model_param, readdata_param, quality_param, summary_param, images, file_title):
    report = Report()
    report.alias_nb_pages()
    report.set_title(title)

    # Dados de Entrada
    report.print_chapter('Dados de Entrada', data = [model_param, readdata_param, quality_param, summary_param], image = None)
    for image in images:
        report.print_chapter('Resultados - Gráficos',data = None, image = image)
    str_title = '%s_%s.pdf' % (file_title, secrets.token_hex(6))
    report.output('static/reports/'+str_title, 'F')

    return str_title
