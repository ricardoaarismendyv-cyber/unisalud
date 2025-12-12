from django import forms
from usuario.models import ResultadosLaboratorio, Pacientes, Servicios

class PacienteChoiceField(forms.ModelChoiceField):
    """
    Campo personalizado para mostrar el nombre y documento del paciente.
    """
    #muestre el nombre y el número de documento del paciente
    def label_from_instance(self, obj):
        return f"{obj.nombre1} {obj.apellido1} - CC: {obj.numero_documento}"

class ResultadoLaboratorioForm(forms.ModelForm):
    # Campo para seleccionar un paciente
    # El campo del modelo se convierte en un campo oculto que llenaremos con JavaScript.
    id_paciente = forms.ModelChoiceField(queryset=Pacientes.objects.all(), widget=forms.HiddenInput(), required=True)
    # Añadimos campos no ligados al modelo para la interacción en la plantilla.
    numero_documento_paciente = forms.CharField(label="Documento del Paciente", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite documento y presione Enter'}))
    nombre_paciente = forms.CharField(label="Nombre del Paciente", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    # Hacemos que la selección del paciente y del servicio sea más amigable
    id_servicio = forms.ModelChoiceField(
        queryset=Servicios.objects.filter(tipo_servicio__icontains='laboratorio'),
        label="Examen de Laboratorio",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ResultadosLaboratorio
        fields = [
            'id_paciente', 
            'id_servicio', 
            'fecha_solicitud', 
            'fecha_resultado', 
            'tipo_examen',
            'resultado', 
            'observaciones', 
            ]
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'fecha_resultado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'tipo_examen': forms.TextInput(attrs={'class': 'form-control'}),
            'resultado': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
