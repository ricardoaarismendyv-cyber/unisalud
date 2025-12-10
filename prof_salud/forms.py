#para diligenciar la HC
from django import forms
from usuario.models import Consulta, Pacientes, Enfermedades, AntecedentesPaciente, OrdenMedica, Servicios, Medicamentos
from django.forms import formset_factory

class ConsultaForm(forms.ModelForm):
    # Campo para seleccionar un paciente
    paciente = forms.ModelChoiceField(
        queryset=Pacientes.objects.all(),
        label="Paciente",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione el paciente que está siendo atendido."
    )

    class Meta:
        model = Consulta
        # Incluir todos los campos relevantes del modelo Consulta
        fields = [
            'paciente',
            'motivo_consulta',
            'anamnesis',
            'examen_fisico',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'temperatura',
            'saturacion_oxigeno',
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'peso',
            'talla',
            'imc',
            'habitos_fumador',
            'habitos_alcohol',
            'habitos_ejercicio',
            'revision_sistemas',
            'impresion_diagnostica',
            'plan_tratamiento',
            'notas_adicionales',
        ]
        widgets = {
            # Usar Textarea para campos de texto largos
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dolor de cabeza, fiebre...'}),
            'anamnesis': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción detallada de los síntomas y su evolución...'}),
            'examen_fisico': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Hallazgos durante el examen físico...'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'lpm'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'rpm'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '°C'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '%'}),
            'presion_arterial_sistolica': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mmHg'}),
            'presion_arterial_diastolica': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mmHg'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'm'}),
            'imc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Índice de Masa Corporal'}),
            'habitos_fumador': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describir hábitos de tabaquismo...'}),
            'habitos_alcohol': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describir consumo de alcohol...'}),
            'habitos_ejercicio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describir rutina de ejercicio...'}),
            'revision_sistemas': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Revisión por sistemas (cardiovascular, respiratorio, etc.)...'}),
            'impresion_diagnostica': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Diagnóstico principal o diferencial basado en la evaluación...'}),
            'plan_tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Pasos a seguir, medicamentos recetados, terapias...'}),
            'notas_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cualquier otra observación relevante...'}),
        }

    # Añadir clases de Bootstrap a todos los campos
    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.fields[field].widget.attrs.get('class', '') + ' form-control mb-2'


class EnfermedadChoiceField(forms.ModelChoiceField):
    """
    Campo personalizado para mostrar el código CIE-10 y el nombre de la enfermedad en las opciones.
    """
    def label_from_instance(self, obj):
        return f"{obj.codigo_cie10} - {obj.nombre_enfermedad}"

class CodigoCIE10ChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.codigo_cie10

class NombreEnfermedadChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre_enfermedad

class DiagnosticoPacienteForm(forms.Form):
    """Formulario para un único diagnóstico."""
    # Campo oculto que guardará el ID de la enfermedad seleccionada.
    id_enfermedad = forms.ModelChoiceField(queryset=Enfermedades.objects.all(), widget=forms.HiddenInput(), required=False)

    codigo_cie10_select = CodigoCIE10ChoiceField(
        queryset=Enfermedades.objects.all(),
        label="Código CIE-10",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un código",
        required=False
    )
    nombre_enfermedad_select = NombreEnfermedadChoiceField(
        queryset=Enfermedades.objects.all(),
        label="Nombre Enfermedad",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione una enfermedad",
        required=False
    )
    tipo_diagnostico = forms.ChoiceField(
        choices=[('', 'Seleccione un tipo'), ('Principal', 'Principal'), ('Presuntivo', 'Presuntivo'), ('Secundario', 'Secundario')],
        label="Tipo de Diagnóstico",
        initial='', # Asegura que la opción por defecto sea la vacía
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False # Lo hacemos opcional para que los formsets vacíos pasen la validación
    )
    notas = forms.CharField(
        label="Notas del Diagnóstico",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
    categoria_grupom = forms.CharField(
        label="Categoría Grupo Mortalidad",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )
    grupo_mortalidad = forms.CharField(
        label="Grupo Mortalidad",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        # Si el formulario se va a eliminar, no se requiere validación adicional.
        if cleaned_data.get('DELETE'):
            return cleaned_data

        # Si se selecciona un tipo de diagnóstico, el ID de la enfermedad es obligatorio.
        if cleaned_data.get('tipo_diagnostico') and not cleaned_data.get('id_enfermedad'):
            self.add_error('id_enfermedad', 'Este campo es obligatorio si se especifica un tipo de diagnóstico.')
        return cleaned_data

DiagnosticoFormSet = formset_factory(DiagnosticoPacienteForm, extra=1, can_delete=True)

class AntecedenteForm(forms.ModelForm):
    """Formulario para un único antecedente."""
    class Meta:
        model = AntecedentesPaciente
        fields = ['tipo_antecedente', 'descripcion', 'severidad', 'estado_antecedente']
        widgets = {
            'tipo_antecedente': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describa el antecedente...'}),
            'severidad': forms.Select(attrs={'class': 'form-control'}),
            'estado_antecedente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AntecedenteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' mb-2'

        # Personalizar el texto para la opción vacía
        self.fields['tipo_antecedente'].empty_label = "Seleccione un tipo"
        self.fields['severidad'].empty_label = "Seleccione una severidad"
        self.fields['estado_antecedente'].empty_label = "Seleccione un estado"

AntecedenteFormSet = formset_factory(AntecedenteForm, extra=1, can_delete=True)

class OrdenMedicaForm(forms.ModelForm):
    class Meta:
        model = OrdenMedica
        # Excluimos los campos que se asignarán automáticamente en la vista o que no se usan en este formulario.
        exclude = [
            'id_orden', 
            'id_profesional',
            'id_centro_medico',
            'id_estado_orden',
            'fecha_emision',
            'fecha_cumplimiento',
            'codigo_qr',
            'id_consulta',
            'id_medicamento', # Excluimos medicamento
            'id_servicio',    # Excluimos servicio
            'indicaciones',   # Excluimos indicaciones, se manejan por servicio
        ]
        # Añadimos los campos de medicamento a la lista de exclusión
        exclude.extend(['dosis', 'duracion_tratamiento', 'frecuencia', 'cantidad'])
        widgets = {
            'id_paciente': forms.Select(attrs={'class': 'form-control mb-2'}),
            'id_tipo_orden': forms.Select(attrs={'class': 'form-control mb-2'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrdenMedicaForm, self).__init__(*args, **kwargs)
        # Añadimos la clase de Bootstrap a todos los campos que no son widgets personalizados.
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control mb-2'
        
        # Personalizamos las etiquetas para que sean más amigables
        self.fields['id_paciente'].label = "Paciente"
        self.fields['id_tipo_orden'].label = "Tipo de Orden"

class ServiciosForm(forms.ModelChoiceField):
    """
    Campo personalizado para mostrar el código y nombre del servicio en las opciones.
    """
    def label_from_instance(self, obj):
        return f"{obj.codigo_servicio} - {obj.nombre_servicio} - {obj.tipo_servicio}"

class codigoServicioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.codigo_servicio

class nombreServicioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre_servicio

# Nuevos ChoiceFields para Medicamentos
class codigoMedicamentoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.codigo_medicamento

class nombreGenericoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre_generico

class TipoServicioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.tipo_servicio

class TipoOrdenForm(forms.Form):
    """Formulario para un único servicio en la orden médica."""
    # Campo oculto que guardará el ID del servicio seleccionado.
    id_servicio = forms.ModelChoiceField(queryset=Servicios.objects.all(), widget=forms.HiddenInput(), required=False)

    codigo_servicio_select = codigoServicioChoiceField(
        queryset=Servicios.objects.all(),
        label="Código Servicio",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un código",
        required=False
    )
    nombre_servicio_select = nombreServicioChoiceField(
        queryset=Servicios.objects.all(),
        label="Nombre Servicio",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un servicio",
        required=False
    )

    tipo_servicio = forms.CharField(
        label="Tipo de Servicio",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )

    indicaciones = forms.CharField(
        label="Indicaciones",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )   

    def clean(self):
        cleaned_data = super().clean()
        # Si el formulario se va a eliminar, no se requiere validación adicional.
        if cleaned_data.get('DELETE'):
            return cleaned_data

        # Solo validamos si el usuario ha interactuado con los campos principales.
        codigo_select = cleaned_data.get('codigo_servicio_select')
        nombre_select = cleaned_data.get('nombre_servicio_select')

        if (codigo_select or nombre_select) and not cleaned_data.get('id_servicio'):
            self.add_error(None, 'Debe seleccionar un servicio válido usando el autocompletado.')
        return cleaned_data

serviciosFormSet = formset_factory(TipoOrdenForm, extra=1, can_delete=True) 

class OrdenMedicamentoForm(forms.ModelForm):
    """
    Formulario específico para crear órdenes de medicamentos con autocompletado.
    """
    # Campo oculto que guardará el ID del medicamento seleccionado. Renombrado para claridad.
    id_medicamento = forms.ModelChoiceField(
        queryset=Medicamentos.objects.all(), 
        widget=forms.HiddenInput(), 
        required=False, # Se valida en el método clean
        label=""
    )

    codigo_medicamento_select = codigoMedicamentoChoiceField(
        queryset=Medicamentos.objects.all(),
        label="Código Medicamento",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un código",
        required=False
    )
    nombre_generico_select = nombreGenericoChoiceField(
        queryset=Medicamentos.objects.all(),
        label="Nombre Genérico",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un medicamento",
        required=False
    )

    principio_activo = forms.CharField(label="Principio Activo", widget=forms.TextInput(attrs={'readonly': True}), required=False)
    concentracion = forms.CharField(label="Concentración", widget=forms.TextInput(attrs={'readonly': True}), required=False)
    forma_farmaceutica = forms.CharField(label="Forma Farmacéutica", widget=forms.TextInput(attrs={'readonly': True}), required=False)

    class Meta:
        model = OrdenMedica
        fields = [
            'dosis',
            'duracion_tratamiento',
            'frecuencia',
            'cantidad',
            'indicaciones'
        ]
        widgets = {
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mg'}),
            'duracion_tratamiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'días'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'día/hora'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12 tabletas'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrdenMedicamentoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control mb-2'
        self.fields['duracion_tratamiento'].label = "Duración del Tratamiento"

    def clean(self):
        cleaned_data = super().clean()
        # Si el formulario se va a eliminar, no se requiere validación adicional.
        if self.has_changed() and not cleaned_data.get('DELETE'):
            id_medicamento = cleaned_data.get('id_medicamento')
            codigo_select = cleaned_data.get('codigo_medicamento_select')
            nombre_select = cleaned_data.get('nombre_generico_select')

            # Un medicamento es requerido si el formulario no está vacío
            if not id_medicamento and (codigo_select or nombre_select):
                self.add_error(None, 'Debe seleccionar un medicamento válido de la lista.')
            elif not id_medicamento:
                # Si no hay medicamento pero otros campos sí, también es un error.
                if any(cleaned_data.get(f) for f in ['dosis', 'cantidad', 'frecuencia']):
                    self.add_error('id_medicamento', 'Se requiere un medicamento para estos detalles.')
        return cleaned_data


MedicamentoFormSet = formset_factory(OrdenMedicamentoForm, extra=1, can_delete=True)