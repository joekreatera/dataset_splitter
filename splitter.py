import pandas
from sklearn.model_selection import train_test_split
import sys 

def stratify_division(folder, dataset, train, validation, test, field):

    print(f"dataset read -> {dataset}")
    dataset = pandas.read_pickle(folder + dataset)
    train_dataset, test_dataset = train_test_split(dataset, test_size=validation+test , random_state = 100, stratify=dataset[field])

    print(f"divided  {train} and {test+validation}")

    validation_dataset, test_dataset = train_test_split(test_dataset, test_size=test/(validation+test) , random_state = 100, stratify=test_dataset[field])
    
    print(f" valid {validation} and test divided {test}")

    train_dataset.to_pickle(folder + "train.pkl")
    validation_dataset.to_pickle(folder + "validation.pkl")
    test_dataset.to_pickle(folder + "test.pkl")
    print("generated files")

if __name__ == "__main__":
    """
    Will produce three files, training, test and validation
    Only accepts pickle files
    """
    # print(sys.argv)
    folder = sys.argv[1]
    dataset_file = sys.argv[2]
    train_amount = float(sys.argv[3])
    validation_amount = float(sys.argv[4])
    testing_amount = float(sys.argv[5])
    stratification_field = sys.argv[6]
    
    stratify_division(folder,dataset_file,train_amount,validation_amount,testing_amount,stratification_field)
    #df = pandas.read_pickle(folder+dataset_file)
    #print(df)
    #print(df[stratification_field].unique())
    #print(df.groupby(stratification_field).count())