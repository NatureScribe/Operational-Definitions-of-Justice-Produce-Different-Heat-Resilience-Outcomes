import numpy as np
import pandas as pd



############################ Calculate tree areas based on sufficientarian theory of justice  ##############################

integrated_dataset = pd.read_excel("SA1_Integrated_Dataset_Filtered_Veg.xlsx")
integrated_dataset = np.asarray(integrated_dataset)

sufficientarian_expected_tree_area = np.empty((integrated_dataset.shape[0], 1), dtype=object)
sufficientarian_expected_tree_area[:] = np.nan

more_trees_sqm = sum(integrated_dataset[:, 2]) - sum(integrated_dataset[:, 3])
print(more_trees_sqm)

sufficientarian_percentage = np.empty((sufficientarian_expected_tree_area.shape[0], 1), dtype=object)
sufficientarian_percentage[:] = np.nan

for i in range(sufficientarian_expected_tree_area.shape[0]):
    sufficientarian_percentage[i, 0] = integrated_dataset[i, 3] / integrated_dataset[i, 1]

count = 0
while count < integrated_dataset.shape[0]:
    print(count)
    print(more_trees_sqm)
    min_value = np.min(sufficientarian_percentage)
    min_indices = np.where(sufficientarian_percentage == min_value)[0]
    # print(min_indices)
    if more_trees_sqm < 1:
        break
    next_min_value = np.min(sufficientarian_percentage[sufficientarian_percentage > min_value])
    for i in range(len(min_indices)):
        allocation = (next_min_value - min_value) * integrated_dataset[min_indices[i], 1]
        if allocation > more_trees_sqm:
            sufficientarian_percentage[min_indices[i], 0] = more_trees_sqm / integrated_dataset[min_indices[i], 1] + min_value
            break
        more_trees_sqm -= allocation
        sufficientarian_percentage[min_indices[i], 0] = next_min_value
    count += 1

for i in range(sufficientarian_expected_tree_area.shape[0]):
    sufficientarian_expected_tree_area[i, 0] = integrated_dataset[i, 1] * sufficientarian_percentage[i, 0]


additional_trees = 1
List_limited_veg_area = []
while additional_trees != 0:
    additional_trees = 0
    prio_weights = 0
    for i in range(sufficientarian_expected_tree_area.shape[0]):
        if sufficientarian_expected_tree_area[i, 0] > integrated_dataset[i, 4]:
            List_limited_veg_area.append(i)
            additional_trees += sufficientarian_expected_tree_area[i, 0] - integrated_dataset[i, 4]
            sufficientarian_expected_tree_area[i, 0] = integrated_dataset[i, 4]


    sufficientarian_percentage = np.empty((sufficientarian_expected_tree_area.shape[0], 1), dtype=object)
    sufficientarian_percentage[:] = np.nan

    for i in range(sufficientarian_expected_tree_area.shape[0]):
        if i not in List_limited_veg_area:
            sufficientarian_percentage[i, 0] = sufficientarian_expected_tree_area[i, 0] / integrated_dataset[i, 1]
        else:
            sufficientarian_percentage[i, 0] = 1

    count = 0
    while count < integrated_dataset.shape[0]:
        print(count)
        print(additional_trees)
        min_value = np.min(sufficientarian_percentage)
        min_indices = np.where(sufficientarian_percentage == min_value)[0]
        # print(min_indices)
        if additional_trees < 1:
            break
        next_min_value = np.min(sufficientarian_percentage[sufficientarian_percentage > min_value])
        for i in range(len(min_indices)):
            allocation = (next_min_value - min_value) * integrated_dataset[min_indices[i], 1]
            if allocation > additional_trees:
                sufficientarian_percentage[min_indices[i], 0] = additional_trees / integrated_dataset[
                    min_indices[i], 1] + min_value
                break
            additional_trees -= allocation
            sufficientarian_percentage[min_indices[i], 0] = next_min_value
        count += 1

    for i in range(sufficientarian_expected_tree_area.shape[0]):
        if i not in List_limited_veg_area:
            sufficientarian_expected_tree_area[i, 0] = integrated_dataset[i, 1] * sufficientarian_percentage[i, 0]



df_pred = pd.DataFrame(sufficientarian_expected_tree_area)
filepath_pred = 'Actual_SA1_Sufficientarian_TreeArea_Veg.xlsx'
df_pred.to_excel(filepath_pred, index=False)

########################################################################################################################
