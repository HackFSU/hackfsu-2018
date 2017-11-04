"""
    Outputs generated csv file.
    https://docs.djangoproject.com/en/1.10/howto/outputting-csv/
"""

from hackfsu_com.views.generic import ControlledView
from django.http import StreamingHttpResponse
import csv


class Echo(object):
    @staticmethod
    def write(value):
        return value


class StreamedCsvView(ControlledView):
    http_method_names = ['get']
    column_names = []
    file_name = 'data.csv'

    def process(self, request, input_data):
        writer = csv.writer(Echo(), quoting=csv.QUOTE_ALL)
        response = StreamingHttpResponse(self.write_rows(request, writer), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.file_name)

        return response

    def write_rows(self, request, writer):
        for row in self.row_generator(request):
            yield writer.writerow(row)

    @staticmethod
    def row_generator(request):
        """ Should yield rows """
        yield []
