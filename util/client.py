# Telle Client
# Implement atomic transactions in each method
#
from redis.exceptions import WatchError
import json


class TelleClient:

    def __init__(self, redis):
        if redis is None or redis == '':
            raise ValueError('redis can not be None or empty.')
        self.redis = redis

    def update_user_to_room_map(self, room_id, dealer_id, muted=False, client_id=None):
        if room_id is None or room_id == '':
            raise ValueError('sid can not be None or empty.')

        # Format: dealerid_roomid_room_map
        key = '{0}_{1}_{2}'.format(dealer_id, room_id, 'room_map')

        print(key)

        flag = False

        with self.redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)

                    current_value = pipe.get(key)

                    if current_value is None:
                        current_value = {'user': [client_id] if client_id is not None else [],
                                         'muted': muted}
                        flag = True
                    else:
                        current_value = json.loads(current_value)
                        if client_id is not None and client_id not in current_value['user']:
                            current_value['user'].append(client_id)
                        current_value['muted'] = muted

                    pipe.multi()
                    pipe.set(key, json.dumps(current_value))

                    pipe.execute()

                    print(current_value)

                    break
                except WatchError:
                    continue
                finally:
                    pipe.reset()

        return flag

    def delete_user_from_room_map(self, room_id, dealer_id, client_id):
        if room_id is None or room_id == '':
            raise ValueError('sid can not be None or empty.')

            # Format: dealerid_roomid_room_map
        key = '{0}_{1}_{2}'.format(dealer_id, room_id, 'room_map')

        close = False
        with self.redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)

                    current_value = pipe.get(key)

                    if current_value is not None:
                        current_value = json.loads(current_value)
                        if client_id in current_value['user']:
                            current_value['user'].remove(client_id)
                            if len(current_value['user']):
                                current_value = None

                    pipe.multi()
                    if current_value is None:
                        close = True
                        pipe.delete(key)
                    else:
                        pipe.set(key, json.dumps(current_value))

                    pipe.execute()

                    break
                except WatchError:
                    continue
                finally:
                    pipe.reset()

        return close

    def delete_user_from_user_map(self, client_id=None):
        if client_id is None or client_id == '':
            raise ValueError('client id can not be None or empty.')

        # Format: dealerid_roomid_room_map
        key = '{0}_{1}'.format(client_id, 'user_map')

        with self.redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)

                    current_value = pipe.get(key)

                    if current_value is not None:
                        ret = json.loads(current_value)
                    else:
                        ret = current_value

                    pipe.multi()

                    pipe.delete(key)

                    pipe.execute()

                    break
                except WatchError:
                    continue
                finally:
                    pipe.reset()

        return ret

    def update_user_to_user_map(self, room_id=None, dealer_id=None, client_id=None):
        if client_id is None or client_id == '':
            raise ValueError('client id can not be None or empty.')

        # Format: dealerid_roomid_room_map
        key = '{0}_{1}'.format(client_id, 'user_map')

        with self.redis.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)

                    current_value = pipe.get(key)

                    if current_value is None:
                        current_value = {}
                    else:
                        current_value = json.loads(current_value)

                    if room_id is not None:
                        current_value['room_id'] = room_id
                    if dealer_id is not None:
                        current_value['dealer_id'] = dealer_id

                    ret = current_value

                    pipe.multi()

                    pipe.set(key, json.dumps(current_value))

                    pipe.execute()

                    print(ret)

                    break
                except WatchError:
                    continue
                finally:
                    pipe.reset()

        return ret
