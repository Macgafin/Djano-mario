
# CODE_TEXTS = {
#     '1': 'Small Mario ：',
#     '2': 'Big Mario ：',
#     '3': 'Fire Mario ：',
#     '4': 'Fish ：',
#     '5': 'Nokonoko ：',
#     '6': 'Kuribo ：',
#     '7': 'Hatena Block ：',
#     '8': 'Kinoko ：',
#     '9': 'Pipe ：',
#     '10': 'P Flower ：',
#     '11': 'Togezo ：',
#     '12': 'Star ：',
#     '13': 'Hummer Bros ：',
#     '14': 'Hummer ：',
#     '15': 'Blooper ：',
#     '16': 'Kuppa ：',
#     '17': 'Killer ：',
#     '18': 'Patapata ：',
#     '19': 'Met ：',
#     '20': 'Scaffold Normal ：',
#     '21': 'Scaffold Sky ：',
#     '22': 'Scaffold Kuppa ：',
#     '23': 'Fire Ball ：',
#     '24': 'Fire Stick ：',
#     '25': 'Fire Kuppa ：',
#     '26': 'Lava ：',
#     '27': 'Elevator ：',
#     '28': 'Kuppa Hummer ：',
# }

CODE_TEXTS = {
    '0': 'Small Mario ：',
    '1': 'Big Mario ：',
    '2': 'Fire Mario ：',
    '3': 'Fish  ：',
    '4': 'Nokonoko  ：',
    '5': 'Coin ：',
    '6': 'Kuribo  ：',
    '7': 'Hatena Block：',
    '8': 'Kinoko ：',
    '9': 'Scaffold ：',
    '10': 'Pipe ：',
    '11': 'P Flower ：',
    '12': 'Togezo ：',
    '13': 'Mario S to B ：',
    '14': 'Star Mario ：',
    '15': 'Star ：',
}

def process_game_info(game_info, current_time):
    mario_state = None
    hatena_block_time = None
    collision_message = "問題はなし"

    for item in game_info:
    # 'code'キーが存在するか確認してから処理を進める
        if 'code' in item:
            print(game_info)
            
            # Marioの状態を確認し、適切な状態を設定
            if any(mario_code in item['code'] for mario_code in ['Small Mario', 'Big Mario', 'Fire Mario']):
                mario_state = item  # Marioの状態を設定

            # ハテナブロックのタイムスタンプを取得
            elif item['code'] == '7':  # 'Hatena Block'のコード
                hatena_block_time = item.get('timestamp', current_time)
                print("計測開始")

    # Marioの状態がない場合のメッセージ
    if not mario_state:
        return "数値がバグっているorマリオが消えています"

    for element in game_info:
        # Marioと重ならない他の要素をチェック
        if element != mario_state:
            # ラベルの取得
            label = CODE_TEXTS.get(element['code'], '')

            # 衝突判定の条件
            if (
                mario_state['x'] < element['x'] + element['width'] and
                mario_state['x'] + mario_state['width'] > element['x'] and
                mario_state['y'] < element['y'] + element['height'] and
                mario_state['y'] + mario_state['height'] > element['y']
            ):
                # ラベルに基づいて衝突メッセージを設定
                if 'Kuribo' in label:
                    collision_message = (
                        "クリボーにぶつかって死亡しました！\n"
                        "ゲームオーバーになったので、5秒前に戻って再挑戦してください。\n"
                        "クリボーはジャンプで避けるか、踏みつけて倒せます。"
                    )
                elif 'Hummer Bros' in label:
                    collision_message = (
                        "ハンマーブロスのハンマーに当たって死亡しました！\n"
                        "ハンマーを避けるためにはタイミングよくジャンプし、または下をくぐって回避できます。\n"
                        "5秒前に戻って、もう一度挑戦してみてください。"
                    )
                elif 'Fire Ball' in label:
                    collision_message = (
                        "ファイアボールに当たって死亡しました！\n"
                        "ファイアボールはジャンプで避けることができます。ジャンプのタイミングを調整して再挑戦してください。\n"
                        "5秒前に戻って、もう一度チャレンジ！"
                    )
                elif 'P Flower' in label:
                    collision_message = (
                        "パックンフラワーに近づきすぎて死亡しました！\n"
                        "パックンフラワーは出てくるタイミングを見計らって、注意深く進んでください。\n"
                        "5秒前に戻り、パックンフラワーの攻撃を避けながら進んでみましょう。"
                    )
                elif 'Kuppa' in label:
                    collision_message = (
                        "クッパに倒されました！\n"
                        "クッパの攻撃を避けるためには、ジャンプで火の玉を避けつつ、クッパの動きを見極めて進むことが重要です。\n"
                        "クッパ戦ではタイミングと位置取りがカギです。5秒前に戻って挑戦しましょう。"
                    )
                elif hatena_block_time is not None and current_time - hatena_block_time <= 10:
                    if 'Big Mario' not in mario_state['code'] and 'Fire Mario' not in mario_state['code']:
                        collision_message = (
                            "ハテナブロックに触れると、ファイヤーマリオになれます！\n"
                            "10秒以内にブロックを取ることでファイヤーマリオに変身し、強力な攻撃を使えます。\n"
                            "10秒前に戻って、ブロックを取りに行きましょう！"
                        )
                elif 'Met' in label:
                    collision_message = (
                        "メットにぶつかって死亡しました！\n"
                        "メットはジャンプで踏みつけることができます。\n"
                        "タイミングを見てジャンプし、メットを倒して進んでください。\n"
                        "5秒前に戻って、もう一度チャレンジ！"
                    )
                elif 'Togezo' in label:
                    collision_message = (
                        "トゲゾーにぶつかって死亡しました！\n"
                        "トゲゾーは動いている場合が多いので、上手にタイミングを見計らって避けましょう。\n"
                        "トゲゾーが地面や天井から降りてきたときに進むか、ジャンプして避けることが必要です。\n"
                        "5秒前に戻って、もう一度チャレンジ！"
                    )
                break  # 最初の衝突を検出したらループを終了

    return collision_message


