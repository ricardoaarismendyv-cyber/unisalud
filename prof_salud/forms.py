from django import forms
from usuario.models import Consulta, Pacientes, DiagnosticoPaciente, Enfermedades, OrdenMedica

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

class OrdenMedicaForm(forms.ModelForm):
    """
    Formulario para crear órdenes médicas.
    Permite seleccionar medicamentos O servicios según el tipo de orden.
    """
    
    # Campo para buscar paciente por documento
    buscar_paciente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de documento del paciente'
        }),
        label='Buscar paciente'
    )
    
    class Meta:
        model = OrdenMedica
        fields = [
            'id_paciente',
            'id_consulta',
            'id_tipo_orden',
            'id_medicamento',
            'id_servicio',
            'dosis',
            'frecuencia',
            'duracion_tratamiento',
            'cantidad',
            'indicaciones',
            'fecha_cumplimiento',
        ]
        widgets = {
            'id_paciente': forms.Select(attrs={'class': 'form-select'}),
            'id_consulta': forms.Select(attrs={'class': 'form-select'}),
            'id_tipo_orden': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_orden'}),
            'id_medicamento': forms.Select(attrs={'class': 'form-select', 'id': 'id_medicamento'}),
            'id_servicio': forms.Select(attrs={'class': 'form-select', 'id': 'id_servicio'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 500mg'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cada 8 horas'}),
            'duracion_tratamiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7 días'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 21'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_cumplimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'id_paciente': 'Paciente',
            'id_consulta': 'Consulta relacionada (opcional)',
            'id_tipo_orden': 'Tipo de orden',
            'id_medicamento': 'Medicamento',
            'id_servicio': 'Servicio/Examen',
            'dosis': 'Dosis',
            'frecuencia': 'Frecuencia',
            'duracion_tratamiento': 'Duración del tratamiento',
            'cantidad': 'Cantidad',
            'indicaciones': 'Indicaciones',
            'fecha_cumplimiento': 'Fecha límite de cumplimiento',
        }
    
    def __init__(self, *args, **kwargs):
        # Obtener profesional actual de la sesión
        self.profesional = kwargs.pop('profesional', None)
        super().__init__(*args, **kwargs)
        
        # Hacer campos condicionales según el tipo
        self.fields['id_medicamento'].required = False
        self.fields['id_servicio'].required = False
        self.fields['id_consulta'].required = False
        
        # Filtrar consultas del centro médico del profesional
        if self.profesional:
            self.fields['id_consulta'].queryset = Consulta.objects.filter(
                id_profesional=self.profesional,
                id_centro_medico=self.profesional.id_centro_medico
            ).order_by('-fecha_programada')[:50]  # Últimas 50
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_orden = cleaned_data.get('id_tipo_orden')
        medicamento = cleaned_data.get('id_medicamento')
        servicio = cleaned_data.get('id_servicio')
        
        # Validar que si es medicamento, tenga medicamento seleccionado
        if tipo_orden and tipo_orden.nombre_tipo.lower() == 'medicamentos':
            if not medicamento:
                raise forms.ValidationError('Debe seleccionar un medicamento para este tipo de orden.')
            cleaned_data['id_servicio'] = None  # Limpiar servicio
        
        # Validar que si es examen/procedimiento, tenga servicio
        elif tipo_orden and tipo_orden.nombre_tipo.lower() in ['examenes', 'procedimientos']:
            if not servicio:
                raise forms.ValidationError('Debe seleccionar un servicio/examen para este tipo de orden.')
            cleaned_data['id_medicamento'] = None  # Limpiar medicamento
        
        return cleaned_data
