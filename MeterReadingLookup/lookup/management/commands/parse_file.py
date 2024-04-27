from django.core.management.base import BaseCommand
from lookup.models import ParsedData
from datetime import datetime

MNAP_CORES: str = '026'
METER_TYPES: str = '028'
REGISTER_READING: str = '030'


class Command(BaseCommand):
    help = 'Parses a file and saves its content into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the file to parse')

    def handle(self, *args, **options):
        ParsedData.objects.all().delete()
        file_path = options['file_path']
        file_name = file_path.split('/')[-1]
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                num_lines = len(lines)
                starts = [lines.index(l) for l in lines if l.startswith(MNAP_CORES)]
                for i, line_index in enumerate(starts):
                    try:
                        split_lines = lines[line_index].split('|')
                        # check for length = 3
                        mpan = split_lines[1]
                        validation_status = split_lines[2]
                        while i < len(starts) and line_index < num_lines-1:
                            line_index += 1
                            if lines[line_index].startswith(MNAP_CORES):
                                break

                            split_lines = lines[line_index].split('|')
                            if split_lines[0] == METER_TYPES:
                                serial_num = split_lines[1]
                                reading_status = split_lines[2]
                            if split_lines[0] == REGISTER_READING:
                                meter_id = split_lines[1]
                                date_time = datetime.strptime(split_lines[2], '%Y%m%d%H%M%S')
                                register_read = split_lines[3]
                                reading_method = split_lines[6]
                                reading_flag = split_lines[7]
                                self.stdout.write(f'filename = {file_name} MNAP = {mpan} validation = {validation_status}'
                                                  f'serial = {serial_num} reading = {reading_status}'
                                                  f'master_id = {meter_id} date_time = {date_time}'
                                                  f'register_read = {register_read}'
                                                  f'reading_method = {reading_method} reading_flag = {reading_flag}')
                                ParsedData.objects.create(file_name=file_name,MPAN_Core=mpan,
                                                    validation_status=validation_status,serial_number=serial_num,reading_status=reading_status,
                                                    meter_id=meter_id,reading_date_time=date_time,
                                                  register_reading=register_read, reading_method=reading_method,
                                                reading_flag=reading_flag),
                    except ValueError:
                        self.stdout.write(self.style.ERROR('Error parsing line. Skipping...'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
        self.stdout.write(self.style.SUCCESS(f'File "{file_path}" parsed and content saved into the database.'))

