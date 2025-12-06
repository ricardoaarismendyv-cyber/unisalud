#para diligenciar la HC
from django import forms
from usuario.models import Consulta, Pacientes, Enfermedades, AntecedentesPaciente, OrdenMedica, Medicamentos, Servicios, TipoOrden, EstadoOrden
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
            # Asegurarse de no sobreescribir clases ya definidas en widgets
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
    id_enfermedad = forms.ModelChoiceField(queryset=Enfermedades.objects.none(), widget=forms.HiddenInput(), required=True)

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
        widget=forms.Select(attrs={'class': 'form-control'})
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
    """Formulario para crear una Orden Médica."""
    class Meta:
        model = OrdenMedica
        fields = [
            'id_orden',
            'id_profesional',
            'id_paciente',
            'id_tipo_orden',
            'id_medicamento',
            'id_servicio',
            'dosis',
            'frecuencia',
            'cantidad',
            'duracion_tratamiento',
            'indicaciones',
            'id_centro_medico',
            'id_estado_orden',
            'fecha_emision',
            'fecha_cumplimiento',
            'codigo_qr',
            'id_consulta',
        ]
        widgets = {
            'id_paciente': forms.Select(attrs={'class': 'form-control'}),
            'id_tipo_orden': forms.Select(attrs={'class': 'form-control'}),
            'id_medicamento': forms.Select(attrs={'class': 'form-control'}),
            'id_servicio': forms.Select(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'id_estado_orden': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'id_paciente': 'Paciente',
            'id_profesional': 'Profesional de Salud',
            'id_centro_medico': 'Centro Médico',
            'id_consulta': 'Consulta Asociada',
            'id_tipo_orden': 'Tipo de Orden',
            'id_medicamento': 'Medicamento',
            'id_servicio': 'Servicio Solicitado',
            'duracion_tratamiento': 'Duración del Tratamiento',
            'id_estado_orden': 'Estado de la Orden',
        }

    def __init__(self, *args, **kwargs):
        super(OrdenMedicaForm, self).__init__(*args, **kwargs)
        # Hacemos que el medicamento y el servicio no sean obligatorios en el formulario
        self.fields['id_medicamento'].required = False
        self.fields['id_servicio'].required = False

        # Añadimos un texto de ayuda y una opción vacía
        self.fields['id_paciente'].empty_label = "Seleccione un paciente"
        self.fields['id_tipo_orden'].empty_label = "Seleccione el tipo"
        self.fields['id_medicamento'].empty_label = "N/A - No aplica medicamento"
        self.fields['id_servicio'].empty_label = "N/A - No aplica servicio"
        self.fields['id_estado_orden'].empty_label = "Seleccione un estado"
    
