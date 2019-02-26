import models


m = models.get_2019_detection_probability_model()

i = -10
while i < 75:
    print(i, m.f(i))
    i += 0.25
