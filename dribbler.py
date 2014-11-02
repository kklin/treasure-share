from datetime import date, timedelta

class Dribbler:
    def __init__(self, donations):
        self._donations = donations
        self._currday = get_currday()

    def get_currday():
        return date.today()

    def days_between(self, start_day, end_day):
        delta = start_day - end_day
        return delta.days

    def dribble_all():
        for d in _donations:
            if dribble_time(d):
                dribble(d)

    def dribble_time(self, donation):
        dribble = donation.get_dribble()
        if donation.last_dribbled == 0:
            if dribble.delay <= days_between(donation.creation_time, _currday):
                return True
        elif dribble.frequency <= days_between(donation.last_dribbled, _currday):
            return True
        return False

    def dribble(self, donation):
        new_amount = donation.amount * (1 - donation.get_dribble().percentage)
        donation.amount = new_amount
        donation.last_dribbled == _currday
