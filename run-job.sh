#!/bin/bash
#SBATCH --mem=102400M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00
#SBATCH --mail-user=A00744368@tec.mx
#SBATCH --mail-type=ALL
cd ~/projects/def-pbranco/josecm08/datasets/dataset_splitter
module purge
module load python/3.10 scipy-stack
source ~/py10efc/bin/activate
#python ./splitter.py ../bot_iot/ nfbotiot_no_flow_id_complete.pkl 0.7 0.15 0.15 AttackLabel
#python ./splitter.py ../cic_ids_2017/ dataset_cicids2017_87_cols_no_time_no_id.pkl 0.7 0.15 0.15 Label
#python ./splitter.py ../cic_ids_2018/ cic_ids_2018_no_flow_id_no_ts_w_labels.pkl 0.7 0.15 0.15 Label
#python ./splitter.py ../cic_ids_2019/ cic_ids_2019_no_id_no_ts.pkl 0.7 0.15 0.15 Label
#python ./splitter.py ../cidds/ cidds_clean_complete.pkl 0.7 0.15 0.15 Label
#python ./splitter.py ../hikari/ hikari_no_flow_id_complete.pkl 0.7 0.15 0.15 AttackLabel
python ./splitter.py ../ins/ insdata_no_flow_id_no_ts_complete.pkl 0.7 0.15 0.15 Label
#missing python .\splitter.py ../iot_23/ ______.pkl 0.7 0.15 0.15 AttackLabel
#python ./splitter.py ../iscx_2012/ iscx2012_clean_complete.pkl 0.7 0.15 0.15 Tag
#python ./splitter.py ../litnet/ litnet_cleaned_complete.pkl 0.7 0.15 0.15 attack_t 
#python ./splitter.py ../nds1/ nds1_clean_complete.pkl 0.7 0.15 0.15 Label
#python ./splitter.py ../opcua/ opcua_no_id_complete.pkl 0.7 0.15 0.15 AttackLabel
#python ./splitter.py ../ton_iot/ nftoniot_no_flow_id_complete.pkl 0.7 0.15 0.15 AttackLabel
#python ./splitter.py ../unsw_nb_15/ nfunswnb15_no_flow_id_complete.pkl 0.7 0.15 0.15 AttackLabel
#python ./splitter.py ../usb_ids/ usb_ids_no_flow_id_no_ts_complete.pkl 0.7 0.15 0.15 Label