import json
import redis

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_prev_coords(ip_address):
    data = redis_db.get(ip_address)
    if data:
        prev_coords = json.loads(data)


        prev_x = prev_coords.get('prev_x')
        right_movement_counter = prev_coords.get('right_movement_counter')
        left_movement_counter = prev_coords.get('left_movement_counter')

    else:
        prev_x = None
        right_movement_counter = 0
        left_movement_counter = 0

    return prev_x, right_movement_counter, left_movement_counter


def check_motion(original_x, prev_x, right_movement_counter, left_movement_counter):
    direction = None

    if prev_x is not None:
        if original_x < prev_x:
            right_movement_counter += 1
            left_movement_counter = 0
        elif original_x > prev_x:
            left_movement_counter += 1
            right_movement_counter = 0
        else:
            right_movement_counter = 0
            left_movement_counter = 0

        if right_movement_counter >= 15:
            direction = 'right'

            right_movement_counter = 0


        elif left_movement_counter >= 15:
            direction = 'left'

            left_movement_counter = 0


    prev_x = original_x
    return direction, prev_x, right_movement_counter, left_movement_counter


def update_bd_info(ip_address, prev_x, right_movement_counter, left_movement_counter):
    movement_data = {
        'prev_x': prev_x,
        'right_movement_counter': right_movement_counter,
        'left_movement_counter': left_movement_counter
    }
    redis_db.set(ip_address, json.dumps(movement_data))


def get_direction(ip_address, original_x):
    # извлечем из бд информацию о движении на пред.кадрах(если они есть)
    prev_x, right_movement_counter, left_movement_counter = get_prev_coords(ip_address)

    # вычислим движение
    (direction, prev_x, right_movement_counter,
     left_movement_counter) = check_motion(original_x, prev_x, right_movement_counter, left_movement_counter)

    # обновим данные в бд
    update_bd_info(ip_address, prev_x, right_movement_counter, left_movement_counter)

    return direction
