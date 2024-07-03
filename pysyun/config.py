# Configs for APScheduler

# '../../flows/pizza/persistent_data.pickle' for Pizza test project
class SchedulerConfig:
    interval = 1  # In minutes

    persistence_file = '../../flows/pizza/persistent_data.pickle'
    minutes = 0
    hours = 24
    days = 0

    message = "You've been inactive recently"
