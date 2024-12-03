from django import forms

class QuestionnaireForm(forms.Form):
    # ゲーム進行のスムーズさ
    game_progression = forms.ChoiceField(
        label="システムを使うことで、ゲームが進めやすくなったと感じましたか？",
        choices=[ 
            (1, "1 - 全く進めまない"),
            (2, "2 - あまり進まない"),
            (3, "3 - 普通"),
            (4, "4 - 進めやすくなった"),
            (5, "5 - とても進めやすくなった"),
        ],
        widget=forms.RadioSelect,
    )

    # フィードバックの有用性
    feedback_usefulness = forms.ChoiceField(
        label="やられた瞬間に巻き戻すことで、フィードバックは役立ちましたか？",
        choices=[ 
            (1, "1 - 全く役立たなかった"),
            (2, "2 - あまり役立たなかった"),
            (3, "3 - 普通"),
            (4, "4 - 役立った"),
            (5, "5 - とても役立った"),
        ],
        widget=forms.RadioSelect,
    )

    # 学習効果
    learning_effect = forms.ChoiceField(
        label="やられた後のフィードバックは、学習を向上させたと思いますか？",
        choices=[ 
            (1, "1 - 全く向上しなかった"),
            (2, "2 - あまり向上しなかった"),
            (3, "3 - 普通"),
            (4, "4 - 向上した"),
            (5, "5 - とても向上した"),
        ],
        widget=forms.RadioSelect,
    )
    
    # 進捗効果
    learning_progress = forms.ChoiceField(
        label="システムを通じてゲームの進捗状況は改善されたと感じますか？",
        choices=[ 
            (1, "1 - 全く改善しなかった"),
            (2, "2 - あまり改善しなかった"),
            (3, "3 - 普通"),
            (4, "4 - 改善した"),
            (5, "5 - かなり改善した"),
        ],
        widget=forms.RadioSelect,
    )
    
    # 組み合わせ
    learning_combination = forms.ChoiceField(
        label="巻き戻し機能とフィードバックの組み合わせは有効と感じましたか？",
        choices=[ 
            (1, "1 - 全く有効ではない"),
            (2, "2 - あまり有効ではなかった"),
            (3, "3 - 普通"),
            (4, "4 - 有効であった"),
            (5, "5 - とても有効であった"),
        ],
        widget=forms.RadioSelect,
    )
    
    # システムの使いやすさ
    system_usability = forms.ChoiceField(
        label="ゲームプレイ中において，システムは使いやすかったですか？",
        choices=[ 
            (1, "1 - とても使いにくかった"),
            (2, "2 - 少々使いにくかった"),
            (3, "3 - 普通"),
            (4, "4 - 使いやすかった"),
            (5, "5 - とても使いやすかった"),
        ],
        widget=forms.RadioSelect,
    )

    # システム利用しての総合評価
    overall_experience = forms.ChoiceField(
        label="システムを使ってみて、全体的にどう感じましたか？",
        choices=[ 
            (1, "1 - 全く良くなかった"),
            (2, "2 - あまり良くなかった"),
            (3, "3 - 普通"),
            (4, "4 - 良かった"),
            (5, "5 - とても良かった"),
        ],
        widget=forms.RadioSelect,
    )
    
    #　発展性評価
    System_Development = forms.ChoiceField(
        label="本システムの観点は将来的にほかのゲームにおいても影響を与えられると思いますか？",
        choices=[ 
            (1, "1 - 全く効果はない"),
            (2, "2 - あまり効果はない"),
            (3, "3 - 普通"),
            (4, "4 - 効果がある"),
            (5, "5 - かなり効果がある"),
        ],
        widget=forms.RadioSelect,
    )

    # システム前の状態について
    pre_system_feedback = forms.CharField(
        label="システム利用前のゲームに関する状態や感想",
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "システムを使う前の状況や感じたことを教えてください"}
        ),
        required=False,
    )

    # システム利用後の状態について
    post_system_feedback = forms.CharField(
        label="システム利用後の状態や感想",
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "システムを使った後の状況や感じたことを教えてください"}
        ),
        required=False,
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