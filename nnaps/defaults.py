from sklearn import preprocessing

import copy

default_scaler = preprocessing.StandardScaler
default_encoder = preprocessing.OneHotEncoder

default_model = [{'layer':'Dense', 'args':[100], 'kwargs': dict(activation='relu', name='FC_1')},
                 {'layer':'Dropout', 'args':[0.1], 'kwargs': dict(name='DO_1')},
                 {'layer':'Dense', 'args':[50], 'kwargs': dict(activation='relu', name='FC_2')},
                 {'layer':'Dropout', 'args':[0.1], 'kwargs': dict(name='DO_2')},
                 {'layer':'Dense', 'args':[25], 'kwargs': dict(activation='relu', name='FC_3')},
                 {'layer':'Dropout', 'args':[0.1], 'kwargs': dict(name='DO_3')},
                 ]

default_regressor_model = []
default_classifier_model = []

def get_processor_class(processor_name):

    if processor_name == 'OneHotEncoder':
        return preprocessing.OneHotEncoder

    elif processor_name == 'StandardScaler':
        return preprocessing.StandardScaler

    elif processor_name == 'RobustScaler':
        return preprocessing.RobustScaler

    elif processor_name == 'MinMaxScaler':
        return preprocessing.MinMaxScaler

    elif processor_name == 'MaxAbsScaler':
        return preprocessing.MaxAbsScaler

    else:
        return None

def add_defaults_to_setup(setup):

    setup = copy.deepcopy(setup)

    def convert_to_default_dict(setup_dict, key, default_dict):
        setup_dict = setup_dict.copy()

        def_key = list(default_dict.keys())[0]
        def_val = default_dict[def_key]

        if type(setup_dict[key]) is list:
            features = {}
            for f in setup_dict[key]:
                features[f] = {def_key: def_val}

            setup_dict[key] = features

        else:
            for f in setup_dict[key].keys():
                if setup_dict[key][f] is None:
                    # if there is no settings dictionary, just add the default
                    setup_dict[key][f] = default_dict
                elif def_key not in setup_dict[key][f]:
                    # if there is a settings dictionary, but it doesn't have the default, add it.
                    setup_dict[key][f][def_key] = def_val
                else:
                    # else, keep the user provided value
                    setup_dict[key][f][def_key] = get_processor_class(setup_dict[key][f][def_key])

        return setup_dict

    # check and update the preprocessors for features and regressors/classifiers
    setup = convert_to_default_dict(setup, 'features', {'processor': default_scaler})
    setup = convert_to_default_dict(setup, 'regressors', {'processor': None})
    setup = convert_to_default_dict(setup, 'classifiers', {'processor': default_encoder})

    # check and update the model setup
    if not 'model' in setup:
        setup['model'] = default_model

    if not 'regressor_model' in setup:
        setup['regressor_model'] = default_regressor_model

    if not 'classifier_model' in setup:
        setup['classifier_model'] = default_classifier_model

    setup['random_state'] = 42
    setup['train_test_split'] = 0.2

    return setup
