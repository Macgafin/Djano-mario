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
    rating_sougou = forms.ChoiceField(
        label="場面を総合的に判断したフィードバックでしたか",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_jyoukyou = forms.ChoiceField(
        label="やられた状態に基づいたフィードバックは学習を向上させることができましたか？",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_approach = forms.ChoiceField(
        label="本システムのアプローチは学習を向上させることのできるもと考えられますか？",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_jyoutatu = forms.ChoiceField(
        label="本システムを経てどれくらいの上達が得られたと感じますか？",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_moura = forms.ChoiceField(
        label="ゲーム自体に対してどれほど網羅できているフィードバックであると感じますか",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_mae = forms.ChoiceField(
        label="システム利用前の自身のゲームに関する練度はいくつであると感じますか",
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )
    rating_ato = forms.ChoiceField(
        label="システム利用後にゲームに関する練度はどれくらい上達したとかんじますか",
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
