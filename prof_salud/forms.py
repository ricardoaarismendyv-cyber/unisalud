#para diligenciar la HC
from django import forms
from usuario.models import Consulta, Pacientes, Enfermedades, AntecedentesPaciente, OrdenMedica, Servicios
from django.forms import formset_factory

class ConsultaForm(forms.ModelForm):
    # Campo para seleccionar un paciente
    paciente = forms.ModelChoiceField(
        queryset=Pacientes.objects.all(),
        label="Paciente",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Seleccione el paciente que está siendo atendido."
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
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'anamnesis': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'examen_fisico': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'revision_sistemas': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'impresion_diagnostica': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'plan_tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notas_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
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
        ]
        # Añadimos los campos de medicamento a la lista de exclusión
        exclude.extend(['dosis', 'duracion_tratamiento', 'frecuencia', 'cantidad'])
        widgets = {
            'id_paciente': forms.Select(attrs={'class': 'form-control mb-2'}),
            'id_tipo_orden': forms.Select(attrs={'class': 'form-control mb-2'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
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

class OrdenMedicamentoForm(forms.ModelForm):
    """
    Formulario específico para crear órdenes de medicamentos.
    """
    class Meta:
        model = OrdenMedica
        fields = [
            'id_paciente',
            'id_medicamento',
            'dosis',
            'duracion_tratamiento',
            'frecuencia',
            'cantidad',
            'indicaciones'
        ]
        widgets = {
            'id_paciente': forms.Select(attrs={'class': 'form-control mb-2'}),
            'id_medicamento': forms.Select(attrs={'class': 'form-control mb-2'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(OrdenMedicamentoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control mb-2'
        self.fields['duracion_tratamiento'].label = "Duración del Tratamiento"
        self.fields['id_paciente'].label = "Paciente"
        self.fields['id_medicamento'].label = "Medicamento"

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

        # Si se selecciona un servicio, el ID del servicio es obligatorio.
        if (cleaned_data.get('codigo_servicio_select') or cleaned_data.get('nombre_servicio_select') or cleaned_data) and not cleaned_data.get('id_servicio'):
            self.add_error('id_servicio', 'Este campo es obligatorio si se especifica un servicio.')
        return cleaned_data

serviciosFormSet = formset_factory(TipoOrdenForm, extra=1, can_delete=True) 