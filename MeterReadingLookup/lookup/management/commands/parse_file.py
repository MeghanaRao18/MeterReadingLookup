from django.core.management.base import BaseCommand
from lookup.models import ParsedData, RegisterReadings
from datetime import datetime


# predefined headers for each level of flow file data as per  D00010 specification
MPAN_CORES: str = '026'
METER_TYPES: str = '028'
REGISTER_READING: str = '030'
VALIDATION_RESULTS: str = '032'
VISIT_CHECK_STATUS: str = '033'

# field length of each flow file line as per D0010 specification
MPAN_SIZE = 2
METERS_SIZE = 2
REGISTERS_SIZE = 7


class Command(BaseCommand):
    help = 'Parses a file and saves its content into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='comma seperated list of Path to the file to parse')

    def handle(self, *args, **options):

        file_path_list = options['file_path'].split(',')
        if file_path_list is None:
            self.stdout.write(self.style.ERROR('Please provide a list of file paths'))
            assert ValueError
        for file_path in file_path_list:

            file_name = file_path.split('/')[-1]
            self.file_parser(file_name,file_path=file_path)

    def file_parser(self,file_name,file_path=None, file_content=None):

        if file_name in ParsedData.objects.values_list('file_name', flat=True).distinct():
            # Overwrite if file name already exist in database
            RegisterReadings.objects.all().delete()
            ParsedData.objects.all().delete()

        try:
            if file_path is not None:
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    f.close()
                except FileNotFoundError:
                    self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
                    raise FileNotFoundError
            else:
                lines = file_content
            num_lines = len(lines)

            # extract all the lines and indices for each mpan
            starts = [lines.index(l) for l in lines if l.startswith(MPAN_CORES)]
            if not starts:
                self.stdout.write(self.style.ERROR(f'NON D0010 standard file content: {file_path}'))
                raise ValueError
            for i, line_index in enumerate(starts):
                try:
                    split_lines = lines[line_index].split('|')
                    if split_lines and len(split_lines) > MPAN_SIZE:  # need at-least 2 fields for mpan data

                        mpan = split_lines[1]
                        validation_status = split_lines[2]
                        # mpan is the unique identifier for each reading
                        self.stdout.write(self.style.SUCCESS(f'Adding MPAN and Validation status to the database for '
                                                             f'file {file_name}'))
                        try:
                            ParsedData.objects.create(file_name=file_name, MPAN_Core=mpan,
                                                      validation_status=validation_status)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(e))
                            raise e
                    else:
                        raise ValueError('MPAN core line does not contain required Info')

                    # extracting all the data for each mpan reading
                    while i < len(starts) and line_index < num_lines - 1:
                        line_index += 1
                        if lines[line_index].startswith(MPAN_CORES):
                            break

                        split_lines = lines[line_index].split('|')
                        if split_lines:

                            if len(split_lines) > METERS_SIZE and split_lines[0] == METER_TYPES:
                                serial_num = split_lines[1]
                                reading_type = split_lines[2]
                                for obj in ParsedData.objects.filter(file_name=file_name,MPAN_Core=mpan):
                                    obj.serial_number = serial_num
                                    obj.reading_type = reading_type
                                    obj.save()

                            if len(split_lines) > REGISTERS_SIZE and split_lines[0] == REGISTER_READING:
                                meter_id = split_lines[1]
                                date_time = datetime.strptime(split_lines[2], '%Y%m%d%H%M%S')
                                register_read = split_lines[3]
                                reading_method = split_lines[6]
                                reading_flag = split_lines[7]
                                mpan_obj = ParsedData.objects.filter(file_name=file_name, MPAN_Core=mpan)
                                try:
                                    self.stdout.write(
                                        self.style.SUCCESS(f'Adding Read registry entry to the database for '
                                                           f'file {file_name}'))
                                    RegisterReadings.objects.create(meter_id=meter_id, reading_date_time=date_time,
                                                                    register_reading=register_read,
                                                                    reading_method=reading_method,
                                                                    reading_flag=reading_flag,
                                                                    mpan=mpan_obj[0])
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(e))
                                    raise e

                            if len(split_lines) > METERS_SIZE and split_lines[0] == VALIDATION_RESULTS:
                                reading_reason = split_lines[1]
                                reading_status = split_lines[2]
                                mpan_obj = ParsedData.objects.filter(file_name=file_name,MPAN_Core=mpan)
                                for obj in RegisterReadings.objects.filter(mpan=mpan_obj[0]):
                                    if obj.reading_reason is None:
                                        obj.update(reading_reason=reading_reason, reading_status=reading_status)
                                        obj.save()

                            if split_lines[0] == VISIT_CHECK_STATUS:
                                visit_check = split_lines[1]
                                mpan_obj = ParsedData.objects.filter(file_name=file_name,MPAN_Core=mpan)
                                for obj in RegisterReadings.objects.filter(mpan=mpan_obj[0]):
                                    if obj.site_visit_check_code is None:
                                        obj.update(site_visit_check_code=visit_check)
                                        obj.save()
                    if not RegisterReadings.objects.filter(mpan__file_name=file_name):
                        # if no read registry against any MPAN, update the registry database  entries
                        mpan_obj = ParsedData.objects.filter(file_name=file_name)

                        try:
                            RegisterReadings.objects.create(meter_id="",
                                                            reading_date_time=datetime.strptime("11111111111111",
                                                                                                '%Y%m%d%H%M%S'),
                                                            register_reading=0.0, reading_method="", reading_flag="",
                                                            reading_reason_code="",
                                                            reading_status="", site_visit_check_code="", mpan=mpan_obj[0])
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(e))
                            raise e
                except ValueError:
                    self.stdout.write(self.style.ERROR('Error parsing line. Skipping...'))
        except ValueError:
            self.stdout.write(self.style.ERROR('Error parsing the file....'))
            raise ValueError
        self.stdout.write(self.style.SUCCESS(f'File "{file_path}" parsed and content saved into the database.'))
