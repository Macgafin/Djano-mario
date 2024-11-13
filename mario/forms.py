# mainproject/mario/forms.py
from django import forms

class QuestionnaireForm(forms.Form):
    rating_experience = forms.ChoiceField(
        label="システム利用しての総合評価",
        choices=[(i, f"{i} - {'非常に悪い' if i == 1 else '非常に良い' if i == 5 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_usability = forms.ChoiceField(
        label="システムの使いやすさ",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_efficiency = forms.ChoiceField(
        label="作業効率への効果",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_comparison = forms.ChoiceField(
        label="システム利用時と未使用時の違い",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    feedback = forms.CharField(
        label="システム利用の感想",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': '具体的な感想をお聞かせください'}),
        required=False
    )
    suggestions = forms.CharField(
        label="改善点",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': '改善してほしい点など'}),
        required=False
    )
