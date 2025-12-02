#para diligenciar la HC
from django import forms
from usuario.models import Consulta, Pacientes, Enfermedades, AntecedentesPaciente
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


class DiagnosticoPacienteForm(forms.Form):
    """Formulario para un único diagnóstico."""
    id_enfermedad = forms.ModelChoiceField(
        queryset=Enfermedades.objects.all(),
        label="Enfermedad (CIE-10)",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione una enfermedad",
        help_text="Si no aparecen enfermedades, deben ser cargadas en el sistema."
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

AntecedenteFormSet = formset_factory(AntecedenteForm, extra=1, can_delete=True)
