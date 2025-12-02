#comando de gestion para ejecutar la tabla enfermedades desde un archivo csv - codigo javascript para que reaccione al cambio en la seleccion de la enfermedad
import csv
from django.core.management.base import BaseCommand
from usuario.models import Enfermedades

class Command(BaseCommand):
    help = 'Importa enfermedades desde un archivo CSV a la base de datos.'

    def add_arguments(self, parser):
        parser.add_argument('ruta_csv', type=str, help='La ruta completa al archivo CSV.')

    def handle(self, *args, **kwargs):
        ruta_csv = kwargs['ruta_csv']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importación desde {ruta_csv}'))

        try:
            with open(ruta_csv, mode='r', encoding='utf-8') as csv_file:
                lector_csv = csv.reader(csv_file, delimiter=';')
                # Omitir la fila de encabezado
                next(lector_csv, None)

                for fila in lector_csv:
                    codigo, nombre, descripcion, cat_grupom, grupo_m = fila
                    
                    enfermedad, creada = Enfermedades.objects.update_or_create(
                        codigo_cie10=codigo,
                        defaults={
                            'nombre_enfermedad': nombre,
                            'descripcion': descripcion,
                            'categoria_grupom': cat_grupom,
                            'grupo_mortalidad': grupo_m,
                        }
                    )
                    if creada:
                        self.stdout.write(self.style.SUCCESS(f'Se creó la enfermedad: {codigo} - {nombre}'))
                    else:
                        self.stdout.write(self.style.NOTICE(f'Se actualizó la enfermedad: {codigo} - {nombre}'))

            self.stdout.write(self.style.SUCCESS('¡Importación completada con éxito!'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Error: No se encontró el archivo en la ruta especificada: {ruta_csv}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocurrió un error inesperado: {e}'))
