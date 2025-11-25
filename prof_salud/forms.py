from django import forms
from usuario.models import Consulta, Pacientes, DiagnosticoPaciente, Enfermedades

#validando y personalizando los formularios para las consultas médicas y diagnósticos
class ConsultaForm(forms.ModelForm):
    # Campos de búsqueda de paciente, el numero de documento no es parte del modelo Consulta, pero se necesita para buscar el paciente
    numero_documento = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese número de documento'
        }),
        label='Número de Documento del Paciente'
    )
    #lista de campos del modelo Consulta
    class Meta:
        model = Consulta
        fields = [
            'fecha_programada', 'motivo_consulta', 'anamnesis', 'examen_fisico',
            'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura',
            'saturacion_oxigeno', 'presion_arterial_sistolica', 'presion_arterial_diastolica',
            'peso', 'talla', 'imc', 'habitos_fumador', 'habitos_alcohol',
            'habitos_ejercicio', 'revision_sistemas', 'impresion_diagnostica',
            'plan_tratamiento', 'notas_adicionales', 'estado'
        ]
        #cada campor tiene su configuracion HTML específica
        widgets = {
            'fecha_programada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el motivo de la consulta'
            }),
            'anamnesis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Historia clínica relatada por el paciente'
            }),
            'examen_fisico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Resultados del examen físico'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'lpm',
                'min': '0'
            }),
            'frecuencia_respiratoria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'rpm',
                'min': '0'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C',
                'step': '0.1'
            }),
            'saturacion_oxigeno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '%',
                'min': '0',
                'max': '100'
            }),
            'presion_arterial_sistolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg'
            }),
            'presion_arterial_diastolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg',
                'step': '0.1'
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calculado automáticamente',
                'readonly': True
            }),
            'habitos_fumador': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccione'),
                ('Si', 'Sí'),
                ('No', 'No'),
                ('Ex-fumador', 'Ex-fumador')
            ]),
            'habitos_alcohol': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccione'),
                ('Si', 'Sí'),
                ('No', 'No'),
                ('Ocasional', 'Ocasional')
            ]),
            'habitos_ejercicio': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccione'),
                ('Si', 'Sí'),
                ('No', 'No')
            ]),
            'revision_sistemas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Revisión por sistemas'
            }),
            'impresion_diagnostica': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Impresión diagnóstica'
            }),
            'plan_tratamiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Plan de tratamiento'
            }),
            'notas_adicionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas adicionales (opcional)'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('programada', 'Programada'),
                ('atendida', 'Atendida'),
                ('cancelada', 'Cancelada')
            ])
        }
        
        labels = {
            'fecha_programada': 'Fecha y Hora de Consulta',
            'motivo_consulta': 'Motivo de Consulta',
            'anamnesis': 'Anamnesis',
            'examen_fisico': 'Examen Físico',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca (FC)',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria (FR)',
            'temperatura': 'Temperatura',
            'saturacion_oxigeno': 'Saturación de Oxígeno (SpO2)',
            'presion_arterial_sistolica': 'Presión Arterial Sistólica',
            'presion_arterial_diastolica': 'Presión Arterial Diastólica',
            'peso': 'Peso',
            'talla': 'Talla',
            'imc': 'IMC',
            'habitos_fumador': '¿Fuma?',
            'habitos_alcohol': '¿Consume Alcohol?',
            'habitos_ejercicio': '¿Realiza Ejercicio?',
            'revision_sistemas': 'Revisión por Sistemas',
            'impresion_diagnostica': 'Impresión Diagnóstica',
            'plan_tratamiento': 'Plan de Tratamiento',
            'notas_adicionales': 'Notas Adicionales',
            'estado': 'Estado de la Consulta'
        }

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoPaciente
        fields = ['id_enfermedad', 'tipo_diagnostico', 'notas']
        
        widgets = {
            'id_enfermedad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_diagnostico': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('presuntivo', 'Presuntivo'),
                ('principal', 'Principal'),
                ('secundario', 'Secundario')
            ]),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas del diagnóstico'
            })
        }
