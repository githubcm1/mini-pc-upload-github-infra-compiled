sudo echo '{"url_shape_predictor": "https://github.com/fbatimarco/caixa-magica-rec-facial/blob/main/share/shape_predictor_5_face_landmarks.dat", "url_face_encoder": "https://github.com/fbatimarco/caixa-magica-rec-facial/blob/main/share/dlib_face_recognition_resnet_model_v1.dat", "url_haarcascade_frontal": "https://github.com/fbatimarco/caixa-magica-rec-facial/blob/main/haarcascade_frontalface_default.xml"}' | sudo tee /home/pi/caixa-magica-vars/config_urls_bib.json

sudo echo '{"informe_sentido_habilitado": true}' | sudo tee /home/pi/caixa-magica-vars/config_sentido_viagem.json

sudo echo '{"versaoCM": 2, "usoGPSElsys": "S", "urlGPSElsys": "curl -X POST http://192.168.10.254/boafrm/formGetGps -d undefined=", "pins": {"gps": "/dev/ttyS0", "mifare": "/dev/ttyUSB0", "catraca": 12, "retorno_catraca": 26, "botao_G": 20, "botao_P": 21, "buzzer": 16, "sonar_T": 6, "sonar_E": 19, "ativa_G": true, "ativa_P": true}}' | sudo tee /home/pi/caixa-magica-vars/config_versao_cm.json

sudo echo '{"debug": true, "core": {"host": "127.0.0.1", "port": 30010, "bufsize": 1024}, "recog": {"path": "/home/pi/caixa-magica-img/"}, "rec_facial": {"min_lambda": 48000, "debug_retangulo": false, "max_dist_sonar": 85, "min_dist_sonar": 20, "min_x": -1, "max_x": 9999, "max_y": 9999, "min_y": -1, "min_width_face": 250, "min_height_face": "253", "min_rate_user": 0.44, "max_rate_user": 0.65, "check_mask": false}, "rotulo_gratuidade": "", "rotulo_dinheiro": "", "timeout_health_check": 15, "limite_espaco_pct": 97, "alerta_limite_espaco_pct": 90, "num_limite_passagens_offline": 5, "num_limite_passagens": 10, "num_regs_proximidade_facial": 1, "exibe_nome_facial": false, "exibe_nome_qrcode": false, "indice_proximidade_facial_suspeita": 0.1, "timeout_catraca": 5, "dias_expurgo_journal": 3, "dias_expurgo_hist_internet": 1, "nova_tentativa_expurgo_journal_minutos": 43600, "nova_tentativa_expurgo_hist_internet": 43600, "nova_tentativa_receber_contas": 5, "nova_tentativa_atualizar_contas": 15, "nova_tentativa_desbloquear_contas": 130, "nova_tentativa_envio_cobranca": 15, "nova_tentativa_abre_offline": 90, "nova_tentativa_fecha_offline": 120, "nova_tentativa_sinc_principal": 120, "nova_tentativa_receber_operadores": 60, "bgr2gray": true, "tamanho_pagina_novas_contas": 3000, "url_shellhub": "http://177.71.253.58/install.sh?tenant_id=9781908c-31d6-4e7d-a6e1-242550cc2c69", "path_sistema": "/home/pi/caixa-magica/", "num_threads_contas": 10, "tam_pagina_contas": 500, "dif_permitida_similaridade_facial": 0.2, "limite_regs_similaridade_facial": 5, "tempo_atualizacao_recebe_favoritos": 1800, "horario_atualizacao_de_recebe_favoritos": 3, "horario_atualizacao_ate_recebe_favoritos": 4, "nova_tentativa_importa_linhas": 1200, "horario_atualizacao_de_importa_linhas": 0, "horario_atualizacao_ate_importa_linhas": 23, "path_file_check_catraca": "/home/pi/caixa-magica-operacao/catraca_em_uso.txt", "limite_envio_cobrancas": 10, "intervalo_dias_expurgo_logs_legados": 3, "intervalo_dias_expurgo_favoritos": 15, "hora_de_expurgo_favoritos": 17, "hora_ate_expurgo_favoritos": 18, "limite_temperatura_cpu_jobs": 99, "timeout_requests": 5, "camera_cv2": 0, "expiracao_qrcode": 120, "hora_de_contingencia_contas": 4, "hora_ate_contingencia_contas": 5, "mail_alerts_to": "validador.logsbuspay@gmail.com", "smtp_address": "smtp.gmail.com", "smtp_port": "465", "mail_alerts_from": "validador.logsbuspay@gmail.com", "mail_alerts_from_pwd": "&FaYUNnP", "exibe_nome_catraca": true, "exibe_saldo_catraca": true, "exibe_nome_saldo_insuficiente": true, "intervalo_gera_arqs_logs": 300, "exibe_catraca_liberada": true}' | sudo tee /home/pi/caixa-magica-vars/config_teste.json

sudo echo '{"debug": true, "core": {"host": "127.0.0.1", "port": 30010, "bufsize": 1024}, "recog": {"path": "/home/pi/caixa-magica-img/"}, "rec_facial": {"min_lambda": 48000, "debug_retangulo": false, "max_dist_sonar": 85, "min_dist_sonar": 20, "min_x": -1, "max_x": 9999, "max_y": 9999, "min_y": -1, "min_width_face": 250, "min_height_face": 250, "min_rate_user": 0.4, "max_rate_user": 0.65, "check_mask": false}, "rotulo_gratuidade": "", "rotulo_dinheiro": "", "timeout_health_check": 15, "limite_espaco_pct": 97, "alerta_limite_espaco_pct": 90, "num_limite_passagens_offline": 5, "num_limite_passagens": 10, "num_regs_proximidade_facial": 1, "exibe_nome_facial": false, "exibe_nome_qrcode": false, "indice_proximidade_facial_suspeita": 0.1, "timeout_catraca": 5, "dias_expurgo_journal": 3, "dias_expurgo_hist_internet": 1, "nova_tentativa_expurgo_journal_minutos": 43600, "nova_tentativa_expurgo_hist_internet": 43600, "nova_tentativa_receber_contas": 5, "nova_tentativa_atualizar_contas": 20, "nova_tentativa_desbloquear_contas": 130, "nova_tentativa_envio_cobranca": 30, "nova_tentativa_abre_offline": 90, "nova_tentativa_fecha_offline": 120, "nova_tentativa_sinc_principal": 120, "nova_tentativa_receber_operadores": 60, "bgr2gray": true, "tamanho_pagina_novas_contas": 3000, "url_shellhub": "http://177.71.253.58/install.sh?tenant_id=9781908c-31d6-4e7d-a6e1-242550cc2c69", "path_sistema": "/home/pi/caixa-magica/", "num_threads_contas": 10, "tam_pagina_contas": 500, "dif_permitida_similaridade_facial": 0.2, "limite_regs_similaridade_facial": 5, "tempo_atualizacao_recebe_favoritos": 1800, "horario_atualizacao_de_recebe_favoritos": 3, "horario_atualizacao_ate_recebe_favoritos": 4, "nova_tentativa_importa_linhas": 1200, "horario_atualizacao_de_importa_linhas": 0, "horario_atualizacao_ate_importa_linhas": 5, "path_file_check_catraca": "/home/pi/caixa-magica-operacao/catraca_em_uso.txt", "limite_envio_cobrancas": 10, "intervalo_dias_expurgo_logs_legados": 3, "intervalo_dias_expurgo_favoritos": 15, "hora_de_expurgo_favoritos": 10, "hora_ate_expurgo_favoritos": 12, "limite_temperatura_cpu_jobs": 99, "timeout_requests": 5, "camera_cv2": 2, "expiracao_qrcode": 120, "hora_de_contingencia_contas": 4, "hora_ate_contingencia_contas": 6, "hora_de_contingencia_operadores": 3, "hora_ate_contingencia_operadores": 4, "mail_alerts_to": "validador.logsbuspay@gmail.com", "smtp_address": "smtp.gmail.com", "smtp_port": "465", "mail_alerts_from": "validador.logsbuspay@gmail.com", "mail_alerts_from_pwd": "&FaYUNnP1", "exibe_nome_catraca": false, "exibe_saldo_catraca": false, "exibe_nome_saldo_insuficiente": false, "intervalo_gera_arqs_logs": 1200, "exibe_catraca_liberada": false, "scaleFactor": 1.3, "minNeigh": 6, "intervalo_screenshot": 180, "liga_serial_placa": false, "intervalo_update_facial_linhas": 600, "intervalo_expurga_logs_integracao": 86400, "intervalo_dias_expurga_logs_integracao": 5, "intervalo_reintegra_viagens": 180, "num_retentativas_viagem": 100, "ativa_screenshot": false, "envia_notif": false, "nova_tentativa_atualizar_saldos": 10, "intervalo_delay_saldos_segundos": 120, "exibe_moldura": true, "num_tentativas_db": 3, "graus_inclinacao_direita": 20, "graus_inclinacao_esquerda": 340, "exibe_propaganda": false, "propaganda_apos_segundos": 2, "match_viagens": false, "intervalo_merge_facial_linhas": 500}' | sudo tee /home/pi/caixa-magica-vars/config_bkp.json

sudo echo '{"uso_auth": true, "sufixo_rota": "V3"}' | sudo tee /home/pi/caixa-magica-vars/param_auth.json

sudo echo '{"ligado": false, "limite_ear": 10, "min_ear": 0.23, "max_ear": 0.281, "path_landmarks": "/home/pi/caixa-magica-rec-facial/share/shape_predictor_68_face_landmarks.dat"}' | sudo tee /home/pi/caixa-magica-vars/params_prova_vida_olhos.json

sudo echo '{"indices_faciais": [{"prioridade": 0, "indice_dimensoes": 512, "indice_facial": "cm_face_recognition_512", "limite_regs_indice_facial": 500000, "total_particoes": 30, "limite_fotos_conta": 1, "algoritmo": "arcface", "habilita_rec": true}, {"prioridade": 1, "indice_dimensoes": 128, "indice_facial": "cm_face_recognition_128", "limite_regs_indice_facial": 500000, "total_particoes": 30, "limite_fotos_conta": 1, "algoritmo": "dlib", "habilita_rec": true}]}' | sudo tee /home/pi/caixa-magica-vars/param_elastic_indices.json

sudo echo '{"habilitado": true, "indice_dimensoes": 128, "indice_facial": "cm_face_recognition_128", "limite_regs_indice_facial": 500000, "total_particoes": 30, "limite_fotos_conta": 1, "url": "http://localhost:9200", "min_score_facial_cosine": 0.9485, "min_score_facial_euclidean": 0.708, "algoritmo_facial": "euclidean", "indice_facial_linha": "cm_face_linha_128", "health_check": "http://localhost:9200/_cat/health", "segundos_limite_start": 300, "usar_indice_linha": false}' | sudo tee /home/pi/caixa-magica-vars/param_elastic.json

sudo echo '{"path_base": "https://github.com/fbatimarco/"}' | sudo tee /home/pi/caixa-magica-vars/config_path_biblio_publicas.json

sudo echo '{"download_client": "curl -s https://install.zerotier.com/ | sudo bash"}' | sudo tee /home/pi/caixa-magica-vars/config_zerotier.json

sudo echo '{"debug": true, "core": {"host": "127.0.0.1", "port": 30010, "bufsize": 1024}, "recog": {"path": "/home/pi/caixa-magica-img/"}, "rec_facial": {"min_lambda": 25000, "debug_retangulo": false, "max_dist_sonar": 70, "min_dist_sonar": 30, "min_x": -1, "max_x": 9999, "max_y": 9998, "min_y": -1, "min_width_face": 1, "min_height_face": 1, "min_rate_user": 0.49, "max_rate_user": 0.65, "check_mask": false}, "rotulo_gratuidade": "", "rotulo_dinheiro": "", "timeout_health_check": 15, "limite_espaco_pct": 97, "alerta_limite_espaco_pct": 90, "num_limite_passagens_offline": 5, "num_limite_passagens": 10, "num_regs_proximidade_facial": 1, "exibe_nome_facial": false, "exibe_nome_qrcode": false, "indice_proximidade_facial_suspeita": 0.1, "timeout_catraca": 5, "dias_expurgo_journal": 3, "dias_expurgo_hist_internet": 1, "nova_tentativa_expurgo_journal_minutos": 43600, "nova_tentativa_expurgo_hist_internet": 43600, "nova_tentativa_receber_contas": 5, "nova_tentativa_atualizar_contas": 20, "nova_tentativa_desbloquear_contas": 130, "nova_tentativa_envio_cobranca": 30, "nova_tentativa_abre_offline": 90, "nova_tentativa_fecha_offline": 120, "nova_tentativa_sinc_principal": 120, "nova_tentativa_receber_operadores": 60, "bgr2gray": true, "tamanho_pagina_novas_contas": 3000, "url_shellhub": "http://177.71.253.58/install.sh?tenant_id=9781908c-31d6-4e7d-a6e1-242550cc2c69", "path_sistema": "/home/pi/caixa-magica/", "num_threads_contas": 10, "tam_pagina_contas": 500, "dif_permitida_similaridade_facial": 0.2, "limite_regs_similaridade_facial": 5, "tempo_atualizacao_recebe_favoritos": 1800, "horario_atualizacao_de_recebe_favoritos": 3, "horario_atualizacao_ate_recebe_favoritos": 4, "nova_tentativa_importa_linhas": 1200, "horario_atualizacao_de_importa_linhas": 3, "horario_atualizacao_ate_importa_linhas": 20, "path_file_check_catraca": "/home/pi/caixa-magica-operacao/catraca_em_uso.txt", "limite_envio_cobrancas": 10, "intervalo_dias_expurgo_logs_legados": 2, "intervalo_dias_expurgo_favoritos": 15, "hora_de_expurgo_favoritos": 10, "hora_ate_expurgo_favoritos": 12, "limite_temperatura_cpu_jobs": 99, "timeout_requests": 5, "camera_cv2": "rtsp://192.168.1.200/", "camera_cv2_old": 0, "expiracao_qrcode": 30, "hora_de_contingencia_contas": 4, "hora_ate_contingencia_contas": 6, "hora_de_contingencia_operadores": 3, "hora_ate_contingencia_operadores": 4, "mail_alerts_to": "validador.logsbuspay@gmail.com", "smtp_address": "smtp.gmail.com", "smtp_port": "465", "mail_alerts_from": "validador.logsbuspay@gmail.com", "mail_alerts_from_pwd": "&FaYUNnP1", "exibe_nome_catraca": true, "exibe_saldo_catraca": false, "exibe_nome_saldo_insuficiente": false, "intervalo_gera_arqs_logs": 1200, "exibe_catraca_liberada": false, "scaleFactor": 1.3, "minNeigh": 3, "intervalo_screenshot": 180, "liga_serial_placa": false, "intervalo_update_facial_linhas": 600, "intervalo_expurga_logs_integracao": 86400, "intervalo_dias_expurga_logs_integracao": 5, "intervalo_reintegra_viagens": 180, "num_retentativas_viagem": 100, "ativa_screenshot": false, "envia_notif": false, "nova_tentativa_atualizar_saldos": 10, "intervalo_delay_saldos_segundos": 120, "exibe_moldura": true, "num_tentativas_db": 3, "graus_inclinacao_direita": 5, "graus_inclinacao_esquerda": 355, "exibe_propaganda": false, "propaganda_apos_segundos": 2, "match_viagens": false, "intervalo_merge_facial_linhas": 15, "horario_utc_vacuum_logs": 5, "frase_offline_encerramento": "Equipamento OFFLINE\nAnote o ID de encerramento abaixo:", "habilita_geoloc_google_maps": false, "limite_kms_mov_viagem_fechada": 0.8, "horario_truncate_historico_geoloc": 5, "intervalo_exec_estatistica_geoloc": 1800, "vacuum_full_dias_semana": "1,4", "vacuum_full_horario_utc_exec": 7, "habilita_envio_logs_api": false, "timeout_streaming_camera": 10, "tela_x_inicio": 0, "tela_x_final": 780, "tela_y_inicio": 390, "tela_y_final": 970, "min_luminosidade_sensor": 100, "timeout_rec_facial": 40, "leitorqr_tentativa2": "/dev/ttyUSB1", "leitorqr_tentativa1": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0", "liga_prova_vida": false, "disk_check_space": "/dev/sda2", "expiracao_prova_vida": 1, "id_conta_mock_rec_facial": "", "refresh_placa_serial": 1e-09, "delay_catraca": 1.5}' | sudo tee /home/pi/caixa-magica-vars/teste.json

sudo echo '{"debug": true, "core": {"host": "127.0.0.1", "port": 30010, "bufsize": 1024}, "recog": {"path": "/home/pi/caixa-magica-img/"}, "rec_facial": {"min_lambda": 1000, "debug_retangulo": false, "max_dist_sonar": 80, "min_dist_sonar": 20, "min_x": -1, "max_x": 9999, "max_y": 9998, "min_y": -1, "min_width_face": 214, "min_height_face": 311, "min_rate_user": 0.49, "max_rate_user": 0.65, "check_mask": false}, "rotulo_gratuidade": "", "rotulo_dinheiro": "", "timeout_health_check": 15, "limite_espaco_pct": 97, "alerta_limite_espaco_pct": 90, "num_limite_passagens_offline": 5, "num_limite_passagens": 10, "num_regs_proximidade_facial": 1, "exibe_nome_facial": false, "exibe_nome_qrcode": false, "indice_proximidade_facial_suspeita": 0.1, "timeout_catraca": 5, "dias_expurgo_journal": 3, "dias_expurgo_hist_internet": 1, "nova_tentativa_expurgo_journal_minutos": 43600, "nova_tentativa_expurgo_hist_internet": 43600, "nova_tentativa_receber_contas": 5, "nova_tentativa_atualizar_contas": 20, "nova_tentativa_desbloquear_contas": 130, "nova_tentativa_envio_cobranca": 30, "nova_tentativa_abre_offline": 90, "nova_tentativa_fecha_offline": 120, "nova_tentativa_sinc_principal": 120, "nova_tentativa_receber_operadores": 60, "bgr2gray": true, "tamanho_pagina_novas_contas": 3000, "url_shellhub": "http://177.71.253.58/install.sh?tenant_id=9781908c-31d6-4e7d-a6e1-242550cc2c69", "path_sistema": "/home/pi/caixa-magica/", "num_threads_contas": 10, "tam_pagina_contas": 500, "dif_permitida_similaridade_facial": 0.2, "limite_regs_similaridade_facial": 5, "tempo_atualizacao_recebe_favoritos": 1800, "horario_atualizacao_de_recebe_favoritos": 3, "horario_atualizacao_ate_recebe_favoritos": 4, "nova_tentativa_importa_linhas": 1200, "horario_atualizacao_de_importa_linhas": 3, "horario_atualizacao_ate_importa_linhas": 20, "path_file_check_catraca": "/home/pi/caixa-magica-operacao/catraca_em_uso.txt", "limite_envio_cobrancas": 10, "intervalo_dias_expurgo_logs_legados": 2, "intervalo_dias_expurgo_favoritos": 15, "hora_de_expurgo_favoritos": 10, "hora_ate_expurgo_favoritos": 12, "limite_temperatura_cpu_jobs": 99, "timeout_requests": 5, "camera_cv2": "rtsp://192.168.1.200/", "camera_cv2_old": 0, "expiracao_qrcode": 30, "hora_de_contingencia_contas": 4, "hora_ate_contingencia_contas": 6, "hora_de_contingencia_operadores": 3, "hora_ate_contingencia_operadores": 4, "mail_alerts_to": "validador.logsbuspay@gmail.com", "smtp_address": "smtp.gmail.com", "smtp_port": "465", "mail_alerts_from": "validador.logsbuspay@gmail.com", "mail_alerts_from_pwd": "&FaYUNnP1", "exibe_nome_catraca": true, "exibe_saldo_catraca": true, "exibe_nome_saldo_insuficiente": false, "intervalo_gera_arqs_logs": 1200, "exibe_catraca_liberada": false, "scaleFactor": 1.3, "minNeigh": 3, "intervalo_screenshot": 180, "liga_serial_placa": false, "intervalo_update_facial_linhas": 600, "intervalo_expurga_logs_integracao": 86400, "intervalo_dias_expurga_logs_integracao": 5, "intervalo_reintegra_viagens": 180, "num_retentativas_viagem": 100, "ativa_screenshot": false, "envia_notif": false, "nova_tentativa_atualizar_saldos": 10, "intervalo_delay_saldos_segundos": 120, "exibe_moldura": true, "num_tentativas_db": 3, "graus_inclinacao_direita": 5, "graus_inclinacao_esquerda": 355, "exibe_propaganda": false, "propaganda_apos_segundos": 2, "match_viagens": false, "intervalo_merge_facial_linhas": 15, "horario_utc_vacuum_logs": 5, "frase_offline_encerramento": "Equipamento OFFLINE\nAnote o ID de encerramento abaixo:", "habilita_geoloc_google_maps": false, "limite_kms_mov_viagem_fechada": 0.8, "horario_truncate_historico_geoloc": 5, "intervalo_exec_estatistica_geoloc": 1800, "vacuum_full_dias_semana": "1,4", "vacuum_full_horario_utc_exec": 7, "habilita_envio_logs_api": false, "timeout_streaming_camera": 10, "tela_x_inicio": 0, "tela_x_final": 780, "tela_y_inicio": 390, "tela_y_final": 970, "min_luminosidade_sensor": 100, "timeout_rec_facial": 40, "leitorqr_tentativa2": "/dev/ttyUSB1", "leitorqr_tentativa1": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0", "liga_prova_vida": false, "disk_check_space": "/dev/sda2", "expiracao_prova_vida": 1, "id_conta_mock_rec_facial": "", "refresh_placa_serial": 0.0001, "delay_catraca": 0.5}' | sudo tee /home/pi/caixa-magica-vars/config.json

