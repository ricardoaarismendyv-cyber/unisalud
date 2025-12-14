from django import forms
from usuario.models import ResultadosLaboratorio, Pacientes, Servicios

class ResultadoLaboratorioForm(forms.ModelForm):
    # El campo del modelo se convierte en un campo oculto que llenaremos con JavaScript.
    id_paciente = forms.ModelChoiceField(queryset=Pacientes.objects.all(), widget=forms.HiddenInput(), required=True)
    
    # Añadimos campos no ligados al modelo para la interacción en la plantilla.
    numero_documento_paciente = forms.CharField(label="Documento del Paciente", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite documento y presione Enter'}))
    nombre_paciente = forms.CharField(label="Nombre del Paciente", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    class Meta:
        model = ResultadosLaboratorio
        fields = [
            'id_paciente', 
            'fecha_solicitud',
            'fecha_registro_resultado',
            'observaciones_resultados', 
            'archivo_pdf',
            ]
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'fecha_registro_resultado': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'observaciones_resultados': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones', 'rows': 3}),
            'archivo_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }
