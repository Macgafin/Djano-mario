from django import forms


class QuestionnaireForm(forms.Form):
    # システム利用しての総合評価
    rating_experience = forms.ChoiceField(
        label="システム利用しての総合評価",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システムの使いやすさ
    rating_usability = forms.ChoiceField(
        label="システムの使いやすさ",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # 作業効率への効果
    rating_efficiency = forms.ChoiceField(
        label="作業効率への効果",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システム利用時と未使用時の違い
    rating_comparison = forms.ChoiceField(
        label="システム利用時と未使用時の違い",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # 場面を総合的に判断したフィードバック
    rating_sougou = forms.ChoiceField(
        label="場面を総合的に判断したフィードバックでしたか",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # 学習向上に関するフィードバック
    rating_jyoukyou = forms.ChoiceField(
        label="やられた状態に基づいたフィードバックは学習を向上させることができましたか？",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # 学習向上のアプローチ
    rating_approach = forms.ChoiceField(
        label="本システムのアプローチは学習を向上させることのできるもと考えられますか？",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システムを経て上達が得られたか
    rating_jyoutatu = forms.ChoiceField(
        label="本システムを経てどれくらいの上達が得られたと感じますか？",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # ゲーム自体に対するフィードバック
    rating_moura = forms.ChoiceField(
        label="ゲーム自体に対してどれほど網羅できているフィードバックであると感じますか",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システム利用前のゲームに関する練度
    rating_mae = forms.ChoiceField(
        label="システム利用前の自身のゲームに関する練度はいくつであると感じますか",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システム利用後のゲームに関する練度
    rating_ato = forms.ChoiceField(
        label="システム利用後にゲームに関する練度はどれくらい上達したとかんじますか",
        choices=[
            (1, "1 - 非常に悪い"),
            (2, "2 - 悪い"),
            (3, "3 - 普通"),
            (4, "4 - 良い"),
            (5, "5 - 非常に良い"),
        ],
        widget=forms.RadioSelect,
    )

    # システム利用の感想
    feedback = forms.CharField(
        label="システム利用の感想",
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "具体的な感想をお聞かせください"}
        ),
        required=False,
    )

    # 改善点
    suggestions = forms.CharField(
        label="改善点",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "改善してほしい点など"}),
        required=False,
    )
