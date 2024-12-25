import re
from time import time  # time()を使って現在時刻を取得する

CODE_TEXTS = {
    "0": "Small Mario ：",
    "1": "Big Mario ：",
    "2": "Fire Mario ：",
    "3": "Fish ：",
    "4": "Nokonoko ：",
    "5": "Kuribo ：",
    "6": "Hatena Block ：",
    "7": "Kinoko ：",
    "8": "Pipe ：",
    "9": "P Flower ：",
    "10": "Togezo ：",
    "11": "Star ：",
    "12": "Hummer Bros ：",
    "13": "Hummer ：",
    "14": "Blooper ：",
    "15": "Kuppa ：",
    "16": "Killer ：",
    "17": "Patapata ：",
    "18": "Met ：",
    "19": "Scaffold Normal ：",
    "20": "Scaffold Sky ：",
    "21": "Scaffold Kuppa ：",
    "22": "Fire Ball ：",
    "23": "Fire Stick ：",
    "24": "Fire Kuppa ：",
    "25": "Lava ：",
    "26": "Elevator ：",
    "27": "Kuppa Hummer ：",
}


def process_game_info(game_info, current_time):
    # global death_time, death_message  # グローバル変数を使用

    mario_state = None
    hatena_block_time = None
    elements = []  # マリオ以外の要素を格納するリスト
    environment = []  # ステージの環境を格納するリスト
    bros_y_coordinate = []  # ハンマーブロスの環境を格納するリスト
    mario_history = []  # マリオの位置履歴を格納
    collision_message = "問題なし"
    


    # マリオの状態を特定し、他の要素をelementsに格納
    for (
        element
    ) in (
        game_info
    ):              # 間違えやすいが、ここのelementは格納されるelementsとは別のことである
        # マリオの状態を判定し、マリオの状態を設定
        if "Small Mario" in element["code"]:
            mario_state = {
                "state": "Small Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        elif "Big Mario" in element["code"]:
            mario_state = {
                "state": "Big Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        elif "Fire Mario" in element["code"]:
            mario_state = {
                "state": "Fire Mario",
                "x": element["x"],
                "y": element["y"],
                "width": element["width"],
                "height": element["height"],
            }
        else:
            # マリオ以外の要素は elements に追加
            elements.append(element)

        # ハテナブロックがあった場合、ハテナブロックのタイムスタンプを記録
        if "Hatena Block" in element["code"]:
            hatena_block_time = element.get("timestamp")  # ハテナブロックの時間を記録

        # 空中の足場の座礁を記録
        if "Scaffold Normal" in element["code"]:
            environment.append({"y": element["y"]})  # ステージの種類とy座標を追加

        # ハンマーブロスの座標を記録
        if "Hummer Bros" in element["code"]:
            bros_y_coordinate.append({"y": element["y"]})  # ステージの種類とy座標を追加

    # マリオの状態が設定されていない場合はエラーメッセージを返す
    if mario_state is None:
        collision_message = "巻き戻し中！"

    print("--------------------------------")

    # マリオの状態を元に衝突判定　まあこれ自体別で一個関数つくってもいいしね
    if mario_state is not None:
        
        if(mario_state["y"] >= 408):
            collision_message = "ええ？落ちたの？　気のせいでしょう、巻き戻してください"
            return collision_message
            
        # 衝突判定の余裕を持たせる距離（ピクセル単位）
        tolerance_x = 20  # X軸方向
        tolerance_y = 20  # Y軸方向

        # マリオの矩形の左上隅と右下隅を計算
        mario_left = mario_state["x"] - mario_state["width"] / 2
        mario_right = mario_state["x"] + mario_state["width"] / 2
        mario_top = mario_state["y"] - mario_state["height"] / 2
        mario_bottom = mario_state["y"] + mario_state["height"] / 2

        for element in elements:
            # elementのコードからラベルを抽出
            default_label = element["code"]
            label = default_label.split("：")[0].strip()

            # elementの矩形の左上隅と右下隅を計算
            element_left = element["x"] - element["width"] / 2
            element_right = element["x"] + element["width"] / 2
            element_top = element["y"] - element["height"] / 2
            element_bottom = element["y"] + element["height"] / 2
            
            

            # 衝突判定
            if (
                abs(mario_state["y"] - element["y"]) <= 20  # y座標がほぼ同じ
                and (
                    ( #マリオが右側
                        mario_state["x"] > element["x"] and mario_left - tolerance_x < element_right
                    )  
                    or ( #マリオが左側
                        mario_state["x"] < element["x"] and mario_right + tolerance_x > element_left
                    )  
                )
            ) or (
                abs(mario_state["x"] - element["x"]) <= 20  # x座標がほぼ同じ
                and (
                    (  #マリオが下
                        mario_state["y"] < element["y"] and mario_top - tolerance_y < element_bottom
                    )  
                    or ( #マリオが上
                        mario_state["y"] > element["y"] and mario_bottom + tolerance_y > element_top
                    )  
                )
            ):
                
                print(f"衝突判定へ{label}")
                print(f"ｙ差：{mario_state["y"] - element["y"]}，マリオｙ：{mario_state["y"]}　elementｙ：{element["y"]}")
                print(f"ｘ差：{mario_state["x"] - element["x"]}，マリオｘ：{mario_state["x"]}　elementｘ：{element["x"]}")
                print(f"空中の足場{environment}")
                print(f"マリオ状態　{mario_state['state']}　マリオ右　{mario_right}　,マリオ左　{mario_left} ,マリオ上　{mario_top}  ,マリオした {element_bottom}")
                print(f"element名　{label}　element右　{element_right}　,element左　{element_left} ,element上　{element_top}　,element下 {element_bottom}")

                # 衝突メッセージの設定
                if "Kuribo" in label or "Kinoko" in label:
                    if "Fire Mario" in mario_state["state"]:
                        collision_message = (
                            "ファイヤーマリオでクリボーに当たってしまいました\n"
                            "ファイヤーマリオなら、ファイアボールを使ってクリボーを倒すことができます。\n"
                            "次は火を使って進むと良いでしょう"
                        )
                    else:
                        collision_message = (
                            "クリボーにぶつかって死亡しました！\n"
                            "さては落ちついていないですね…\n"
                            "見なかったことにしますので、戻って再挑戦しましょう！"
                        )

                # ハンマーブロスにぶつかった場合
                elif "Hummer Bros" in label:
                    if (
                        mario_state["y"] < bros_y_coordinate[0]["y"]
                    ):  # マリオより上にブロスがいる時
                        collision_message = (
                            "上にいるハンマーブロスで死んでしまいました\n"
                            "下に通り抜けるチャンスがあります。ハンマーブロスが上に上るタイミングを見計らって通り抜けてみましょう\n"
                            "また、上の足場を叩いて倒すことも可能です。戻って再挑戦！"
                        )
                    else:
                        collision_message = (
                            "ハンマーブロスのに当たって死亡しました！\n"
                            "ハンマーの動きを注意深く見て近づき、ハンマーのわっかの中にいて，"
                            "ハンマーブロスがジャンプするタイミングで通り抜けてみましょう\n"
                            "踏みつけて倒すこともできますよ、再挑戦してみてください！"
                        )

                # げっそー（Blooper）の動き
                elif "Blooper" in label:
                    # ゲッソーの判定もできるようにしたかったのですけどね
                    # if 'escape' in blooper_state:  # 逃げるタイプのげっそー
                    #     collision_message = (
                    #         "げっそーにやられました！\n"
                    #         "逃げるタイプのげっそーは近づいても問題ありませんが、慎重に進んでください。\n"
                    #         "足場があれば、冷静に進みましょう。戻って再挑戦してください！"
                    #     )
                    # elif 'aggressive' in blooper_state:  # 近づいてくるタイプのげっそー
                    #     collision_message = (
                    #         "げっそーにやられました！\n"
                    #         "近づいてくるタイプのげっそーには、逃げられなくなることが多いです。\n"
                    #         "そのため、○○秒前に戻って安全な場所を探しながら進みましょう。"
                    #     )
                    # else:
                    #     collision_message = (
                    #         "げっそーにやられました！\n"
                    #         "どちらのタイプか不明ですが、足場を活用して回避するのが重要です。\n"
                    #         "戻って、安全な場所を探しながら進んでみましょう。"
                    #     )
                    collision_message = (
                        "ゲッソーにやられました！\n"
                        "ゲッソーには逃げるタイプと近づいてくるタイプがいるので，どちらのタイプなのかを慎重に見極めよう！\n"
                        "近づいてくるタイプは戻って避けながら，避けるタイプはあえて近づいてみるのも方法のひとつですよ！\n"
                        "戻って、安全な場所を探しながら進んでみましょう。"
                    )

                # パックンフラワーに近づきすぎた場合
                elif "P Flower" in label:
                    if (
                        "Fire Mario" in mario_state["state"]
                    ):  # ファイヤーマリオが有効な場合
                        collision_message = (
                            "パックンフラワーにぶつかってしまいました！\n"
                            "ファイヤーマリオなら、ファイアボールでパックンフラワーを倒せます。\n"
                            "安全に進むために、土管から出てくるタイミングでジャンプして火の玉を出してみましょう！\n"
                            "戻って再挑戦してみましょう。"
                        )
                    else:
                        collision_message = (
                            "パックンフラワーぶつかって死亡しました！\n"
                            "パックンフラワーは出てくるタイミングを見計らってジャンプして避けていく必要があります。\n"
                            "方法としては土管の近くに立っていればその土管からはパックンフラワーが出てこなくなるので、"
                            "一旦待ってからジャンプして避けてみましょう！。戻って慎重に進んでみましょう。"
                        )

                # トゲゾーにぶつかった場合
                elif "Togezo" in label:
                    if mario_state["y"] < environment[0]["y"]:  # 空中に足場がある場合
                        collision_message = (
                            "トゲゾーにぶつかって死亡しました！\n"
                            "上に足場があるので，トゲゾーを上の足場に落として，下側を駆け抜けていきましょう！\n"
                            "戻って再挑戦してみましょう！"
                        )
                    else:  # 地面の足場がある場合
                        collision_message = (
                            "トゲゾーにぶつかって死亡しました！\n"
                            "トゲゾーは、マリオに向かって直進してきます，避けやすい場所で集めてから一気にジャンプして避けるとやりやすいですよ\n"
                            "周囲に穴があればうまいこと、そこに落として見ましょう。戻って再挑戦！"
                        )

                # エレベーターで死亡した場合
                elif "Elevator" in label:
                    collision_message = (
                        "エレベーターは不安定な足場なので、急がず落ち着いて移動しましょう。\n"
                        "急がずに直前の安全地帯でエレベーターの動きを把握して，ルート確認をするとよいでしょう！\n"
                        "戻って再挑戦！"
                    )

                # ノコノコに遭遇した場合
                elif "Nokonoko" in label:
                    if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
                        collision_message = (
                            "ノコノコにぶつかってしまいました\n"
                            "ファイヤーマリオなら、ノコノコをファイアボールで倒せます！惜しまずに死なないようにファイアーボールをどんどん使ってみましょう！\n"
                            "戻って、再挑戦してみましょう"
                        )
                    else:
                        collision_message = (
                            "ノコノコにぶつかって死亡しました！\n"
                            "ノコノコはジャンプで踏みつけて倒せます。ただ狭いところで倒すと危険なので避けていきましょう\n"
                            "また、踏みつけると甲羅の状態になりますので，蹴って他の敵に当てると倒せますよ，危ないときに利用してみるのも手です\n"
                            "戻って再挑戦！"
                        )

                # パタパタに遭遇した場合
                elif "Patapata" in label:
                    if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
                        collision_message = (
                            "パタパタにぶつかって死亡しました！\n"
                            "ファイヤーマリオなら、パタパタを倒すためにファイアボールを使うことができます。"
                            "ただし当てるタイミングが難しいので無理せずに避けるのを最優先しましょう\n"
                            "戻って進みましょう！"
                        )
                    else:
                        collision_message = (
                            "パタパタにぶつかって死亡しました！\n"
                            "パタパタは難しいですが、タイミングをよく見てジャンプで踏みつけて倒すか，ジャンプしているタイミングで避けていきましょう\n"
                            "ただしジャンプした瞬間に通り抜けようとするとあたることが多いので，少し早いくらいのタイミングで行くとよいでしょう\n"
                            "また、その甲羅を利用して遠くの敵を倒すことができます。戻って再挑戦！"
                        )

                # メットに遭遇した場合
                elif "Met" in label:
                    if "Fire Mario" in mario_state["state"]:  # ファイヤーマリオなら
                        collision_message = (
                            "メットにぶつかってしまいました！\n"
                            "メットはファイヤーマリオの火を防ぎます。\n"
                            "倒す方法は踏みつけることのみです！動きが遅いので避けてみるのもいいかもしれません。\n"
                            "戻って再挑戦しましょう！"
                        )
                    else:
                        collision_message = (
                            "メットにぶつかって死亡しました！\n"
                            "メットは難しいですが、タイミングをよく見てジャンプで踏みつけて倒せます。\n"
                            "ただし無理に倒すよりも動きが遅いので避けるのを最優先してみてもいいでしょう\n"
                            "戻って再挑戦！"
                        )

                # クッパにぶつかった場合
                elif "Kuppa" in label:
                    if (
                        "Fire Mario" in mario_state["state"]
                        or "Big Mario" in mario_state["state"]
                    ):  # ファイヤーマリオかつビッグマリオ
                        if (
                            mario_state["y"] < environment[0]["y"]
                        ):  # マリオのy座標が足場より高い場合
                            collision_message = (
                                "クッパに倒されました！\n"
                                "基本的にクッパは踏みつけて倒すことができないので，クッパがジャンプしたタイミングで通り抜けるのが攻略方法になります！\n"
                                "ここでは上に足場があるのでこれを利用して上側から安全に避けてみましょう\n！"
                                "戻って再挑戦してみましょう"
                            )
                        else:
                            collision_message = (
                                "クッパに倒されました！\n"
                                "今の状態ならば、クッパにぶつかってみても一瞬無敵になれます。この時間を利用してそのままゴールする方法もありますよ！\n"
                                "またファイヤーマリオであれば何発もファイアーボールをクッパ当てても勝つことができますよ，安全な位置からファイアーボールを飛ばしてみましょう！"
                                "戻って再挑戦！"
                            )
                    else:
                        collision_message = (
                            "クッパに倒されました！\n"
                            "クッパの攻撃を避けるためには、安全地帯からクッパの行動パターンを観察してみましょう！大きくジャンプするタイミングがあるのでそこに合わせて駆け抜けて行く準備をしてみましょう\n"
                            "戻って慎重に進んでください！"
                        )

                elif (
                    hatena_block_time is not None
                    and current_time - hatena_block_time <= 10
                ):
                    if (
                        "Big Mario" not in mario_state["state"]
                        and "Fire Mario" not in mario_state["state"]
                    ):
                        collision_message += (
                            "ちなみに10秒以内はてなブロックがありました、\n"
                            "今の状態で叩いてフラワーやキノコが入っていればスーパーマリオやファイヤーマリオに変身してよりパワーアップした状態になれます！\n"
                        )
                        
                elif "Fish" in label:  # 魚にぶつかった場合
                    if "Scaffold Sky" in element["code"]:
                        collision_message = (
                            "空プクプクにぶつかって死亡しました！\n"
                            "プクプクは足元をめがけて飛んでくるものと少し追い越し気味に飛んでくるモノいます\n"
                            "基本的にはプクプクの着地位置を判別しながらゆっくり進んでみよう"
                            )
                    else:
                        collision_message = (
                            "水中のプクプクにぶつかって死亡しました！\n"
                            "水中ではまっすぐ泳いてくるため，先に自身の動線とプクプクの動線を確認してみましょう。\n"
                            "進むコースを定めたらゲッソーなどの他の敵に気を付けなら進みましょう"
                            "ジャンプボタンの押す間隔で泳ぐ速度を調整できるので落ち着いて，戻って再挑戦してみましょう"
                        )

                elif "Killer" in label:  # キラーにぶつかった場合
                    collision_message = (
                        "キラーにぶつかって死亡しました！\n"
                        "キラーは直線的に動くため、タイミングを見て進むことが重要です。\n"
                        "また、大砲の位置を意識して動くのも有効です。戻って再挑戦！"
                    )


    print("-------------------------------------")
    return collision_message
