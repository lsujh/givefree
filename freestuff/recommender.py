import redis
from django.conf import settings
from .models import Things


# r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
#
# class Recommender(object):
#     def get_thing_key(self, id):
#         return 'thing:{}:purchased_with'.format(id)
#
#     def things_bought(self, things):
#         things_ids = [p.id for p in things]
#         for thing_id in things_ids:
#             for with_id in things_ids:
#                 if thing_id != with_id:
#                     r.zincrby(self.get_thing_key(thing_id), with_id, amount=1)
#
#     def suggest_things_for(self, things, max_results=6):
#         things_ids = [p.id for p in things]
#         if len(things) == 1:
#             suggestions = r.zrange(self.get_thing_key(things_ids[0]), 0, -1, desc=True)[:max_results]
#         else:
#             flat_ids = ''.join([str(id) for id in things_ids])
#             tmp_key = 'tmp_{}'.format(flat_ids)
#             keys = [self.get_thing_key(id) for id in things_ids]
#             r.zunionstore(tmp_key, keys)
#             r.zrem(tmp_key, *things_ids)
#             suggestions = r.zrange(tmp_key, 0, -1 , desc=True)[:max_results]
#             r.delete(tmp_key)
#         suggested_things_ids = [int(id) for id in suggestions]
#         suggested_things = list(Things.objects.filter(id__in=suggested_things_ids))
#         suggested_things.sort(key=lambda x: suggested_things_ids.index(x.id))
#         return suggested_things
#
#     def clear_purchases(self):
#         for id in Things.objects.value_list('id', flat=True):
#             r.delete(self.get_thing_key(id))


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_thing_key(self, id):
        return 'thing:{}:purchased_with'.format(id)

    def things_bought(self, things):
        thing_ids = [p.id for p in things]
        for ting_id in thing_ids:
            for with_id in thing_ids:
                # get the other things bought with each product
                if ting_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_thing_key(ting_id),
                              with_id,
                              amount=1)

    def suggest_things_for(self, things, max_results=6):
        thing_ids = [p.id for p in things]
        if len(things) == 1:
            # only 1 product
            suggestions = r.zrange(
                             self.get_thing_key(thing_ids[0]),
                             0, -1, desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in thing_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # multiple things, combine scores of all things
            # store the resulting sorted set in a temporary key
            keys = [self.get_thing_key(id) for id in thing_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the things the recommendation is for
            r.zrem(tmp_key, *thing_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_things_ids = [int(id) for id in suggestions]

        # get suggested things and sort by order of appearance
        suggested_things = list(Things.objects.filter(id__in=suggested_things_ids))
        suggested_things.sort(key=lambda x: suggested_things_ids.index(x.id))
        return suggested_things

    def clear_purchases(self):
            for id in Things.objects.values_list('id', flat=True):
                r.delete(self.get_thing_key(id))