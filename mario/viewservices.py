# services.py
import time

def process_game_info(game_info, current_time):
    mario = None
    hatena_block_time = None
    collision_message = "その他の状況"

    for item in game_info:
        if 'Mario' in item['code']:
            mario = item
        elif 'Hatena Block' in item['code']:
            hatena_block_time = item.get('timestamp', current_time)

    if not mario:
        return "Marioが見つかりませんでした"

    for element in game_info:
        if element != mario and 'Mario' not in element['code']:
            if (mario['x'] < element['x'] + element['width'] and
                mario['x'] + mario['width'] > element['x'] and
                mario['y'] < element['y'] + element['height'] and
                mario['y'] + mario['height'] > element['y']):
                
                if 'Kuribo' in element['code'] or 'Nokonoko' in element['code']:
                    collision_message = "クリボーにぶつかって死んでいるので５秒前に戻ってやり直してください"
                    break
                elif hatena_block_time is not None:
                    if 'small Mario' not in mario['code']:
                        if current_time - hatena_block_time <= 5:
                            collision_message = "ハテナブロックがあったので取ればファイヤーマリオになれましたよ、５秒ほど戻ってください"
                            break

    return collision_message