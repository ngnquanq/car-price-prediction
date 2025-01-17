COLS_TO_CAST =[...]
COLS_TO_DROP = ['id', 'list_id', 'list_time']
CAT_COLS = ['brand', 'model', 'origin', 'type', 'gearbox', 'fuel', 'color', 'condition']
NUM_COLS = ['manufacture_date', 'seats', 'mileage_v2']
SAMPLE_DATA = {'id': 149990878, 'list_id': 109913621, 'list_time': 1694606265000, 'manufacture_date': 2020,
 'brand': 'Mercedes Benz',
 'model': 'GLC Class',
 'origin': 'Việt Nam',
 'type': 'SUV / Cross over',
 'seats': 5.0,
 'gearbox': 'AT',
 'fuel': 'petrol',
 'color': 'black',
 'mileage_v2': 71000,
 'condition': 'used', 'price':1239000000.0 }# A random sample
PARAMS={'loss_function': 'MAE',
    'iterations': 4000,
    'learning_rate': 0.2,
    'cat_features': CAT_COLS,
    'max_depth': 10,
    'verbose': 100}
 