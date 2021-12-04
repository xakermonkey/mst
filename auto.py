import cityflow




config_path = 'config.json'


eng = cityflow.Engine(config_path, thread_num=1)
eng.set_save_replay(True)
while eng.get_current_time()  < 500:
    eng.next_step()