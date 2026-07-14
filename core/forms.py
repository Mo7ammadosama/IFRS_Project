from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = [
            'name', 'description', 'price',
            'calories', 'protein', 'carbs', 'fat',
            'allergens', 'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control'}),
            'allergens': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }




from django import forms

MOOD_CHOICES = [
    ("Happy", "Happy"),
    ("Neutral", "Neutral"),
    ("Sad", "Sad"),
    ("Angry / Stressed", "Angry / Stressed"),
    ("Tired", "Tired"),
]

YES_NO = [("Yes", "Yes"), ("No", "No")]

ENERGY = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]

FOCUS = [("Yes", "Yes"), ("Partially", "Partially"), ("No", "No")]

DAY_CHOICES = [
    ("Relaxed", "Relaxed"),
    ("Difficult", "Difficult"),
    ("Normal", "Normal"),
    ("Exciting", "Exciting"),
    ("Exhausting", "Exhausting"),
]

class CustomerQuizForm(forms.Form):
    q1 = forms.ChoiceField(choices=MOOD_CHOICES)
    q2 = forms.ChoiceField(choices=YES_NO)
    q3 = forms.ChoiceField(choices=ENERGY)
    q4 = forms.ChoiceField(choices=FOCUS)
    q5 = forms.ChoiceField(choices=YES_NO)
    q6 = forms.ChoiceField(choices=YES_NO)
    q7 = forms.ChoiceField(choices=DAY_CHOICES)
