from django import forms
from usuario.models import ResultadosLaboratorio, Pacientes, Servicios

class ResultadoLaboratorioForm(forms.ModelForm):
    # Hacemos que la selección del paciente y del servicio sea más amigable
    id_paciente = forms.ModelChoiceField(
        queryset=Pacientes.objects.all(),
        label="Paciente",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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

